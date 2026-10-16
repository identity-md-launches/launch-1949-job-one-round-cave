#!/usr/bin/env python3
"""Filter and decode saved receipt logs offline, retaining every input position."""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import sys

SOURCE = Path(__file__).resolve().parents[1] / 'event-lens' / 'event_lens.py'
spec = importlib.util.spec_from_file_location('receipt_event_lens', SOURCE)
events = importlib.util.module_from_spec(spec)
spec.loader.exec_module(events)
MAX_LOGS = 1024
NOTICE = ('Offline interpretation of supplied receipt and ABI only. No chain inclusion, '
          'emitter identity, finality, receipt completeness or token movement is verified. '
          'Positions are array offsets, not authenticated log indices. Duplicates are retained; '
          'no balances or aggregate amounts are inferred.')


def address(value):
    if not isinstance(value, str) or not re.fullmatch(r'0x[0-9a-fA-F]{40}', value):
        raise ValueError('emitter address must be exactly 20 bytes of 0x-prefixed hex')
    return value.lower()


def inspect(entries, reference, emitter, receipt):
    emitter = address(emitter)
    entry = events.select_event(entries, reference)
    signature, anonymous = events.event_schema(entry)
    if anonymous:
        raise ValueError('anonymous events cannot be selected by topic0; use Event Lens explicitly')
    topic = '0x' + events.abi.keccak256(signature.encode('ascii')).hex()
    if not isinstance(receipt, dict) or not isinstance(receipt.get('logs'), list):
        raise ValueError('receipt must be an object with a logs array (unwrap RPC result first)')
    logs = receipt['logs']
    if len(logs) > MAX_LOGS:
        raise ValueError('receipt exceeds the 1024-log limit')
    # Admit only standard post-Byzantium success/failure status, if supplied.
    # It is a supplied label, never an assertion about the actual transaction.
    status = receipt.get('status')
    if 'status' in receipt and status not in ('0x0', '0x1'):
        raise ValueError('receipt status, if supplied, must be 0x0 or 0x1')
    rows = []
    for position, log in enumerate(logs):
        row = {'position': position}
        try:
            if not isinstance(log, dict):
                raise ValueError('log must be an object')
            actual = address(log.get('address'))
            row['emitter'] = actual
            if actual != emitter:
                row.update(status='skipped', reason='different_emitter')
            else:
                # Validate the complete log before classifying topic mismatches.
                topics, _ = events.parse_log(log)
                if 'removed' in log and type(log['removed']) is not bool:
                    raise ValueError('removed, if supplied, must be boolean')
                if log.get('removed', False):
                    row.update(status='removed', reason='supplied_removed_flag')
                elif not topics or topics[0].hex() != topic[2:]:
                    row.update(status='skipped', reason='different_topic0')
                elif status == '0x0':
                    raise ValueError('matching log conflicts with supplied failed receipt status')
                else:
                    result = events.decode_log(entry, log)
                    row.update(status='decoded', arguments=result['arguments'])
        except ValueError as exc:
            row.update(status='invalid', reason=str(exc))
        rows.append(row)
    counts = {key: sum(row['status'] == key for row in rows)
              for key in ('decoded', 'skipped', 'removed', 'invalid')}
    return {'signature': signature, 'emitter_filter': emitter, 'topic0_filter': topic,
            'supplied_receipt_status': status, 'log_count': len(logs), 'counts': counts,
            'has_findings': bool(counts['invalid'] or counts['removed']),
            'logs': rows, 'notice': NOTICE}


def demo():
    # Reuse the existing explicitly constructed fixture, never claim an observed transfer.
    root = SOURCE.parent
    event_abi = events.read_json(root / 'transfer-abi.json')
    log = events.read_json(root / 'transfer-log.json')
    return inspect(event_abi, 'Transfer', events.ZTO,
                   {'status': '0x1', 'logs': [dict(log, address=events.ZTO),
                    dict(log, address='0xd34a99bc0f67ae1bbd63c660e6d0b0dd03e263b7')]})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--demo', action='store_true')
    parser.add_argument('--abi')
    parser.add_argument('--event')
    parser.add_argument('--emitter')
    parser.add_argument('--receipt')
    args = parser.parse_args()
    try:
        if args.demo:
            if any((args.abi, args.event, args.emitter, args.receipt)):
                raise ValueError('--demo cannot be combined with other arguments')
            result = demo()
            result['fixture'] = 'Constructed offline logs using real ZTO/IMD addresses; not observed transfers'
        else:
            if not all((args.abi, args.event, args.emitter, args.receipt)):
                raise ValueError('provide --abi, --event, --emitter and --receipt, or --demo')
            result = inspect(events.read_json(args.abi), args.event, args.emitter,
                             events.read_json(args.receipt))
    except (ValueError, OSError, RecursionError) as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 1 if result['has_findings'] else 0


if __name__ == '__main__':
    raise SystemExit(main())

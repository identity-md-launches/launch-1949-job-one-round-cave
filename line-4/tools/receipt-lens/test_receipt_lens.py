import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('receipt_lens', HERE / 'receipt_lens.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
ZTO = r.events.ZTO
IMD = '0xd34a99bc0f67ae1bbd63c660e6d0b0dd03e263b7'
TOPIC = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'


def log():
    return {'address': ZTO, 'topics': [TOPIC, '0x'+'00'*12+ZTO[2:],
            '0x'+'00'*12+IMD[2:]], 'data': '0x'+(2**255+17).to_bytes(32,'big').hex()}


class Receipts(unittest.TestCase):
    def run_receipt(self, logs, **kw):
        return r.inspect([r.events.TRANSFER], 'Transfer', ZTO, dict(logs=logs, **kw))

    def test_exact_filter_and_integer(self):
        a, b = log(), log()
        b['address'] = IMD
        out = self.run_receipt([b, a])
        self.assertEqual(out['counts'], dict(decoded=1, skipped=1, removed=0, invalid=0))
        self.assertEqual(out['logs'][1]['position'], 1)
        self.assertEqual(out['logs'][1]['arguments'][2]['value'], 2**255+17)
        self.assertFalse(out['has_findings'])

    def test_case_normalization(self):
        a=log(); a['address']='0x'+ZTO[2:].upper()
        a['topics'][0]='0x'+TOPIC[2:].upper()
        self.assertEqual(self.run_receipt([a])['counts']['decoded'], 1)

    def test_different_topic(self):
        a=log(); a['topics'][0]='0x'+'ab'*32
        self.assertEqual(self.run_receipt([a])['logs'][0]['reason'], 'different_topic0')

    def test_malformed_log_is_retained(self):
        out=self.run_receipt([None, {}, log()])
        self.assertEqual(out['counts']['invalid'], 2)
        self.assertEqual(out['logs'][2]['position'], 2)
        self.assertTrue(out['has_findings'])

    def test_removed_never_decodes(self):
        a=log(); a['removed']=True
        out=self.run_receipt([a])
        self.assertEqual(out['counts']['removed'], 1)
        self.assertTrue(out['has_findings'])

    def test_removed_requires_bool(self):
        for value in (0, 1, None, 'false'):
            a=log(); a['removed']=value
            self.assertEqual(self.run_receipt([a])['counts']['invalid'], 1)

    def test_failed_receipt_conflict(self):
        out=self.run_receipt([log()], status='0x0')
        self.assertEqual(out['counts']['invalid'], 1)
        self.assertIn('failed receipt',out['logs'][0]['reason'])

    def test_empty_and_status(self):
        self.assertEqual(self.run_receipt([], status='0x0')['log_count'], 0)
        self.assertIsNone(self.run_receipt([])['supplied_receipt_status'])
        for value in (None, True, 1, '0x01', {}, []):
            with self.assertRaises(ValueError):
                self.run_receipt([], status=value)

    def test_duplicate_not_silently_removed(self):
        out=self.run_receipt([log(), log()])
        self.assertEqual(out['counts']['decoded'], 2)
        self.assertEqual([x['position'] for x in out['logs']], [0, 1])

    def test_canonical_data(self):
        a=log(); a['data']+='00'*32
        self.assertEqual(self.run_receipt([a])['counts']['invalid'], 1)

    def test_high_address_bits(self):
        a=log(); a['topics'][1]='0x01'+a['topics'][1][4:]
        self.assertEqual(self.run_receipt([a])['counts']['invalid'], 1)

    def test_malformed_topic_not_skipped(self):
        a=log(); a['topics'][0]='0xab'
        self.assertEqual(self.run_receipt([a])['counts']['invalid'], 1)

    def test_other_emitter_not_decoded(self):
        a={'address': IMD, 'topics': 'invalid', 'data': None}
        out=self.run_receipt([a])
        self.assertEqual(out['logs'][0]['reason'], 'different_emitter')

    def test_anonymous_refused(self):
        entry=copy.deepcopy(r.events.TRANSFER); entry['anonymous']=True
        with self.assertRaisesRegex(ValueError,'anonymous'):
            r.inspect([entry], 'Transfer', ZTO, {'logs':[]})

    def test_root_limits_and_address(self):
        for value in (None, [], {'logs':None}, {'logs':[{}]*1025}):
            with self.assertRaises(ValueError):
                r.inspect([r.events.TRANSFER], 'Transfer', ZTO, value)
        for value in (None, ZTO+'00', ' '+ZTO, '0x'+'gg'*20):
            with self.assertRaises(ValueError):
                r.inspect([r.events.TRANSFER], 'Transfer', value, {'logs':[]})

    def test_cli_demo_and_error(self):
        command=[sys.executable, '-B', str(HERE/'receipt_lens.py')]
        p=subprocess.run(command+['--demo'],capture_output=True,text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)['counts']['decoded'], 1)
        p=subprocess.run(command+['--demo','--emitter',ZTO],capture_output=True,text=True)
        self.assertEqual(p.returncode, 2)
        self.assertNotIn('Traceback',p.stderr)


if __name__ == '__main__':
    unittest.main()

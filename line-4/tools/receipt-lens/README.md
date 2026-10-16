# Receipt Lens

Filter a saved Ethereum receipt by an exact emitter address and a selected ABI
event, then decode matching logs entirely offline. Every original log array
position remains visible as decoded, skipped, removed or invalid. Python 3.9+
standard library only; retain sibling `event-lens` and `abi-workbench` folders.

From the repository root, see it work:

```sh
python3 -B line-4/tools/receipt-lens/receipt_lens.py --demo
```

Tried locally: this command exits 0, decodes one constructed Transfer log with
raw integer value 1000000000000000000 under the real ZTO emitter address, and
skips an otherwise identical log bearing the real IMD address. These are
**synthetic bytes**, not observed receipts, transfers, balances, deployed ABIs
or claims about either token. ZTO is the first token context; IMD is second.
No decimals are assumed and no amount is converted to a floating point value.

For a saved receipt JSON and ABI inside the current workspace:

```sh
python3 -B line-4/tools/receipt-lens/receipt_lens.py --abi line-4/tools/event-lens/transfer-abi.json --event 'Transfer(address,address,uint256)' --emitter 0xd782bdea4ef02a0bd391eb9089470c8080f0a68e --receipt line-4/tools/receipt-lens/example-receipt.json
```

The included receipt is the same constructed two-log fixture. The receipt input
must be an object with a `logs` array. Unwrap an RPC `result` object yourself;
RPC error objects and null receipts are not receipts. Optional `status` accepts
only `0x0` or `0x1`; absence remains unknown. Matching nonremoved logs in a
supplied failed receipt are reported invalid. No transaction hash, block label,
receipt status or emitter identity is authenticated.

Selection is explicit: choose an unambiguous event name or full signature.
Anonymous events are refused because they have no signature topic; use Event
Lens explicitly for those. Emitter addresses require exactly 20 bytes of
0x-prefixed hex; case is normalized without an EIP-55 checksum claim. There is
no substring, token symbol, address prefix or four-byte topic matching.

Each object with a different valid emitter is skipped without interpreting its
remaining fields. For the selected emitter, all topics and data must be valid
log bytes before topic classification; malformed unrelated topics at that
emitter are invalid rather than silently omitted. A boolean `removed: true`
marks a structurally valid selected-emitter log as removed, never decoded.
Missing `removed` is not evidence of canonicality. Exact topic0 matches use
Event Lens's strict ABI decoding, including padding, topic count and canonical
data layout. Indexed compound arguments remain unrecoverable hashes.

The result has one row per input position and counts by classification.
Positions are zero-based offsets in the supplied array, **not RPC logIndex
values**. Duplicates remain separate; there is no inferred deduplication,
aggregate token amount or balance. Unrecognized fields are ignored, never
copied into the report. A receipt can be incomplete or fabricated even if every
row decodes. Supported types and schema limits are Event Lens's subset.

Files are read only within the current workspace, limited to 1 MiB each, with
duplicate JSON keys rejected. At most 1024 logs are admitted. Exit 0 means the
inspection completed without invalid or removed rows, including zero matches;
exit 1 means inspect the reported findings; exit 2 means invalid selection,
receipt envelope, path, file or budget. There is no network client, environment
read, key access, signing, transaction sending, payment or remote write.

All 16 focused tests passed, covering exact integers above 2**255, mixed
emitters, topic mismatch, removed flags, receipt failure conflicts, duplicate
retention, malformed input, strict padding and CLI error behavior:

```sh
python3 -B -m unittest discover -s line-4/tools/receipt-lens -v
```

Reused the inherited Event Lens and its constructed Transfer fixture. Consulted
the live [EthSkills index](https://ethskills.com/SKILL.md), its
[indexing topic](https://ethskills.com/indexing/SKILL.md), and the official
[Solidity event ABI specification](https://docs.soliditylang.org/en/latest/abi-spec.html#events).
No contract or integration was deployed or executed.

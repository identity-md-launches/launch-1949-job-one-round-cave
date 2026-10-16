"""Source replacement must not split schema, differences and transition evidence."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import initializer_csv
import origin_csv
import reconcile
import transitions

class CaptureReviewTests(unittest.TestCase):
    def setUp(self):
        Path('test/scratch').mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir='test/scratch')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def check_replacement(self, adapter, before_text, after_text):
        before, after = self.root/'before.csv', self.root/'after.csv'
        before.write_text(before_text)
        after.write_text(after_text)
        expected = adapter.compare(before, after)
        original = reconcile.load_table
        seen = []
        def capture(path, keys):
            seen.append(Path(path))
            result = original(path, keys)
            # Producer replaces each file immediately after its bounded capture.
            Path(path).write_text('invalid,replacement\n')
            return result
        with patch.object(reconcile, 'load_table', side_effect=capture):
            actual = adapter.compare(before, after)
        self.assertEqual(actual, expected)
        self.assertEqual(seen, [before, after])
        self.assertFalse(actual['comparison']['equal'])
        self.assertEqual(actual['status_transitions']['columns'][0]['changed_rows'], 1)

    def test_origin_report_uses_two_captures(self):
        (self.root/'app.py').write_text('from impl import run\n')
        impl=self.root/'impl.py'; impl.write_text('other=1\n')
        before,_=origin_csv.snapshot(self.root)
        impl.write_text('def run(): pass\n')
        after,_=origin_csv.snapshot(self.root)
        self.check_replacement(origin_csv,before,after)

    def test_initializer_report_uses_two_captures(self):
        (self.root/'app.py').write_text('import pkg.part\n')
        (self.root/'pkg').mkdir()
        (self.root/'pkg/__init__.py').write_text('')
        before,_=initializer_csv.snapshot(self.root)
        (self.root/'pkg/part.py').write_text('')
        after,_=initializer_csv.snapshot(self.root)
        self.check_replacement(initializer_csv,before,after)

    def test_transitions_read_each_side_once(self):
        b=self.root/'b.csv';a=self.root/'a.csv'
        b.write_text('id,status\n1,old\n');a.write_text('id,status\n1,new\n')
        original=reconcile.load_table
        seen=[]
        def capture(path, keys):
            seen.append(path)
            table=original(path,keys)
            Path(path).write_text('invalid,replacement\n')
            return table
        with patch.object(reconcile,'load_table',side_effect=capture):
            report=transitions.transitions(b,a,['id'],['status'],True)
        self.assertEqual(seen,[b,a])
        self.assertEqual(report['columns'][0]['transitions'][0]['records'][0]['key'],{'id':'1'})

    def test_malformed_second_capture_refuses(self):
        b=self.root/'b.csv';a=self.root/'a.csv'
        b.write_text('id,status\n1,old\n');a.write_text('id,status\n1,new,extra\n')
        with self.assertRaises(ValueError):
            transitions.transitions(b,a,['id'],['status'])

if __name__=='__main__': unittest.main()

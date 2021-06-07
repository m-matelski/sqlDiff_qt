import unittest

from sqldiff.sql.diff.compare import SequenceMatcher


class TestSequenceMatcher(unittest.TestCase):

    def test_insert(self):
        s1 = 'f1 f2 f3'.split()
        s2 = 'f1 i1 f2 f3'.split()
        sm = SequenceMatcher(s1, s2)
        cmp = sm.compare()
        expected = [
            (('f1', 'equal'), ('f1', 'equal')),
            (None, ('i1', 'insert')),
            (('f2', 'equal'), ('f2', 'equal')),
            (('f3', 'equal'), ('f3', 'equal')),
        ]
        self.assertEqual(cmp, expected)

    def test_delete(self):
        s1 = 'f1 f2 d1 f3 d2'.split()
        s2 = 'f1 f2 f3'.split()
        sm = SequenceMatcher(s1, s2)
        cmp = sm.compare()
        expected = [
            (('f1', 'equal'), ('f1', 'equal')),
            (('f2', 'equal'), ('f2', 'equal')),
            (('d1', 'delete'), None),
            (('f3', 'equal'), ('f3', 'equal')),
            (('d2', 'delete'), None),
        ]
        self.assertEqual(cmp, expected)

    def test_move(self):
        s1 = 'f1 f2 f3 f4 f5'.split()
        s2 = 'f1 f3 f2 f4 f5'.split()
        sm = SequenceMatcher(s1, s2)
        cmp = sm.compare()
        expected = [
            (('f1', 'equal'), ('f1', 'equal')),
            (('f2', 'move'), ('f3', 'move')),
            (('f3', 'move'), ('f2', 'move')),
            (('f4', 'equal'), ('f4', 'equal')),
            (('f5', 'equal'), ('f5', 'equal')),
        ]
        self.assertEqual(cmp, expected)

    def test_mixed(self):
        s1 = 'f1 f2 f3 d1 f4 d2'.split()
        s2 = 'f2 i1 f4 f3 i2 i3 i4'.split()
        sm = SequenceMatcher(s1, s2)
        cmp = sm.compare()
        expected = [
            (('f1', 'delete'), None),
            (('f2', 'equal'), ('f2', 'equal')),
            (None, ('i1', 'insert')),
            (('f3', 'move'), ('f4', 'move')),
            (('d1', 'delete'), None),
            (('f4', 'move'), ('f3', 'move')),
            (None, ('i2', 'insert')),
            (('d2', 'delete'), None),
            (None, ('i3', 'insert')),
            (None, ('i4', 'insert'))
        ]
        self.assertEqual(cmp, expected)

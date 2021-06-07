from collections import namedtuple

StringSequenceMatch = namedtuple('StringSequenceMatch', 'field tag')


def _comp_identity(a, b):
    return a == b


def _comp_string_case_insensitive(a, b):
    return a.lower() == b.lower()


def _get_item_or_last(a, i):
    try:
        elem = a[i]
    except IndexError:
        elem = a[-1]
    return elem


class SequenceMatcher:
    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2

    def _compare_string_sequences(self, cmp=lambda x, y: x == y):
        src_idx = tgt_idx = 0

        while src_idx < len(self.s1) or tgt_idx < len(self.s2):

            src_string = _get_item_or_last(self.s1, src_idx)
            tgt_string = _get_item_or_last(self.s2, tgt_idx)

            if cmp(src_string, tgt_string):
                yield StringSequenceMatch(src_string, 'equal'), StringSequenceMatch(tgt_string, 'equal')
                src_idx += 1
                tgt_idx += 1
            else:

                src_in_tgt = any(cmp(src_string, tgt_s) for tgt_s in self.s2)
                tgt_in_src = any(cmp(src_s, tgt_string) for src_s in self.s1)
                if not tgt_in_src and not tgt_idx >= len(self.s2):
                    yield None, StringSequenceMatch(tgt_string, 'insert')
                    tgt_idx += 1
                if not src_in_tgt and not src_idx >= len(self.s1):
                    yield StringSequenceMatch(src_string, 'delete'), None
                    src_idx += 1
                if src_in_tgt and tgt_in_src:
                    yield StringSequenceMatch(src_string, 'move'), StringSequenceMatch(tgt_string, 'move')
                    src_idx += 1
                    tgt_idx += 1

    def compare(self, case_sensitive=False):
        """
        Returns sequence comparison status.
        """
        if case_sensitive:
            comp = _comp_identity
        else:
            comp = _comp_string_case_insensitive

        return list(self._compare_string_sequences(comp))

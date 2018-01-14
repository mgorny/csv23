# test_init.py

from __future__ import unicode_literals

import pytest

from csv23 import open_csv, iterrows

LINE, ROW = 'Wonderful Spam,Lovely Spam\r\n', ['Wonderful Spam', 'Lovely Spam']


def test_open_csv(filepath, row=ROW):
    filename = str(filepath)

    with open_csv(filename, 'w') as writer:
        writer.writerow(row)

    with open_csv(filename, 'r') as reader:
        assert list(reader) == [row]

    with open_csv(filename) as reader:
        assert list(reader) == [row]


@pytest.mark.parametrize('mode', ['nonmode', None, object(), []])
def test_open_csv_mode_invalid(mode, filename='nonfile'):
    with pytest.raises(ValueError, match=r'invalid mode'):
        open_csv(filename, mode)


def test_iterrows(filepath, line=LINE, expected=ROW, encoding='utf-8'):
    text = ''.join('%d,%s' % (i, line) for i in range(1, 4))
    filepath.write_binary(text.encode(encoding))
    rows = iterrows(str(filepath), encoding=encoding)

    assert next(rows) == ['1'] + expected
    assert next(rows) == ['2'] + expected
    assert list(rows) == [['3'] + expected]

    with pytest.raises(StopIteration):
        next(rows)

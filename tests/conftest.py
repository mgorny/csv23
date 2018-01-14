# conftest.py - pytest configuration and shared fixtures

from __future__ import unicode_literals

import sys
import locale
import argparse

import pytest

PY2 = sys.version_info.major == 2


def pytest_configure(config):
    py2only = pytest.mark.skipif(not PY2, reason='Python 2 only')
    pytest.csv23 = argparse.Namespace(PY2=PY2, py2only=py2only)


@pytest.fixture(scope='session')
def py2():
    return PY2


@pytest.fixture(scope='session')
def none_encoding():
    return locale.getpreferredencoding()


@pytest.fixture(scope='session')
def nonclean_encoding():
    return 'u16'


@pytest.fixture
def nonclean_none_encoding(mocker, nonclean_encoding):
    mocker.patch('csv23._common.locale.getpreferredencoding', return_value=nonclean_encoding)
    yield nonclean_encoding


@pytest.fixture
def mock_open(mocker):
    yield mocker.patch('csv23._common.io.open', mocker.mock_open())


@pytest.fixture
def filepath(tmpdir):
    return tmpdir / 'spam.csv'

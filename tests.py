"""
This file contains the unit tests for bookscraper.py

Code lightly edited from https://dev.to/albertulysses/unit-testing-your-web-scraper-1aha
"""

import os
import bookscraper

pkg = './bookscraper.py'

def test_exists():
    """checks if the file exist"""

    assert os.path.isfile(pkg)


def test_price():
    """£51.77 -> 51.77 type float"""

    res = bookscraper.monetary('£51.77')
    assert res == float(51.77)

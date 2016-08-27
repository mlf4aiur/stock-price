#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import stock_price


class StockPriceTestCase(unittest.TestCase):

    def setUp(self):
        stock_price.app.config['TESTING'] = True
        self.app = stock_price.app.test_client()

    def tearDown(self):
        pass

    def test_health(self):
        rv = self.app.get('/healthz')
        assert b'ok' in rv.data

    def test_convert_to_dict(self):
        with open("fixtures/AAPL.csv") as fp:
            response = fp.read()
        expected = dict(
            symbol="AAPL",
            name="Apple Inc.",
            price="105.68")
        self.assertDictEqual(expected, stock_price.convert_to_dict("AAPL", response))


if __name__ == '__main__':
    unittest.main()

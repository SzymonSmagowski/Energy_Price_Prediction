import unittest
import pandas as pd
import backtests

class TestStringMethods(unittest.TestCase):

    def test_dates_correction(self):
        # robiłem unittesty w pracy, ale tutaj już niestety za długo pracuję i nie mam siły
        self.assertEqual(backtests.Get_dates("2019-12-12"), ('2019-12-11 23:00:00+00:00', '2019-12-12 23:00:00+00:00')) 

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
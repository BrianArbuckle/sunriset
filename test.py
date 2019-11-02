#!/usr/bin/env python

import datetime
import unittest

import sunriset

class TestSunriset(unittest.TestCase):
    def test_to_pandas(self):
        """Test conversion to the pandas data frame."""
        lat = 34.0522
        long = -118.2437
        local_tz = -8

        number_of_years = 1
        start_date = datetime.date(2019, 1, 1)

        df = sunriset.to_pandas(start_date, lat, long, local_tz, number_of_years)

        self.assertEqual(len(df.index), 365)

    def test_set_noon(self):
        lat = 34.0522
        long = -118.2437
        local_tz = -8
        start_date = datetime.date(2019, 1, 1)

        rise, sset, noon = sunriset.sunrise_set_noon(start_date, lat, long, local_tz, tz_adjust=0)

        self.assertEqual((rise, sset, noon),
                         (datetime.timedelta(seconds=25116, microseconds=873548),
                          datetime.timedelta(seconds=60871, microseconds=790164),
                          datetime.timedelta(seconds=42994, microseconds=331856)))

if __name__ == '__main__':
    unittest.main()


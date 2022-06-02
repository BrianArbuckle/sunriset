#!/usr/bin/env python

import datetime
import unittest

import sunriset
import sunriset.calc

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

class TestCalc(unittest.TestCase):
    def test_make_time(self):
        """Test conversion to the pandas data frame."""
        time_float = 35 
        d_utz = 1
        tz_adjust = 1


        result = sunriset.calc.make_time(time_float, d_utz, tz_adjust)
        result2 = sunriset.calc.make_time(time_float + .5, d_utz, tz_adjust)

    
        self.assertEqual((result), datetime.timedelta(days=36, seconds = 0))
        self.assertNotEqual((result), datetime.timedelta(days=35, seconds = 0))
        self.assertEqual((result2), datetime.timedelta(days=36, seconds=43200))
        self.assertNotEqual((result2), datetime.timedelta(days=36, seconds = 0))

    def test_julian_day(self):
        usr_date = datetime.date(2021,5,31)
        tz = -2

        result = sunriset.calc.julian_day(usr_date, tz)

        self.assertAlmostEqual((result), 2459366.0833333335)
        self.assertNotEqual((result), 2459366)

    def test_julian_century(self):
        jd_local = 2459366

        result = sunriset.calc.julian_century(jd_local)

        self.assertAlmostEqual((result), 0.21412731006160166)
        self.assertNotEqual((result), 1.24)


if __name__ == '__main__':
    unittest.main()


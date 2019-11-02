"""This module contains the main functions of 'sunriset.'

Sunriset generates Solar Position Data based on Latitude, Longitude, Date and
Time Zone.

Note: For individual, detailed calculations, run help(sunriset.calc).
"""

import datetime
from datetime import timedelta

import pandas as pd

from . import calc

def to_pandas(start_date, lat, long, local_tz, number_of_years):
    """Returns a Pandas DataFrame of all the calculations for various solar projects.
    With a datetime.date for starting date, local latitude, lat, local Longitude, long
    and local Time Zone as a positive or negative integer. """

    # this will evelntially be the daylight savings output:
    tz_adjust = 0
    year = int(start_date.year)
    # Number of days claculation
    total_days = 0
    for _y in range(1, number_of_years + 1):
        if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            total_days += 366
        else:
            total_days += 365

    dict_for_df = {}
    for i in range(0, total_days):
        # Our arguments are passed as positional maybe not best practice?
        yr = start_date + datetime.timedelta(days=i)
        julian_day = calc.julian_day(yr, local_tz)
        julian_cent = calc.julian_century(julian_day)
        sgml = calc.solar_geometric_mean_longitude(julian_cent)
        sgma = calc.solar_geometric_mean_anomaly(julian_cent)
        eceo = calc.eccentricity_earth_orbit(julian_cent)
        seoc = calc.solar_equation_of_center(julian_cent, sgma)
        stlg = calc.solar_true_longitude(sgml, seoc)
        stan = calc.solar_true_anomaly(sgma, seoc)
        svau = calc.solar_radius_vector_aus(eceo, stan)
        salg = calc.solar_apparent_longitude(stlg, julian_cent)
        mobe = calc.mean_obliquity_ecliptic(julian_cent)
        ocor = calc.obliquity_correction_deg(mobe, julian_cent)
        asce = calc.solar_accent_return(salg, ocor)
        sdec = calc.solar_decline(ocor, salg)
        vary = calc.var_y(ocor)
        eqtm = calc.equation_of_time(vary, sgml, eceo, sgma)
        hans = calc.hour_angle_sunrise(lat, sdec)
        soln = calc.solar_noon_float(eqtm, long, local_tz)
        srif = calc.sunrise_float(soln, hans)
        setf = calc.sunset_float(soln, hans)
        noon = calc.make_time(soln, yr, tz_adjust)
        rise = calc.make_time(srif, yr, tz_adjust)
        sset = calc.make_time(setf, yr, tz_adjust)
        sdur = calc.sunlight_duration(hans)
        trst = calc.true_solar_time_min(eqtm, long, local_tz)
        hand = calc.hour_angle_deg(trst)
        szen = calc.solar_zenith_angle(lat, sdec, hand)
        sela = calc.solar_elevation_angle(szen)
        aprx = calc.approx_atmospheric_refraction(sela)
        atmr = calc.solar_elevation_corrected_atm_refraction(aprx, sela)
        azmt = calc.solar_azimuth(hand, lat, szen, sdec)
        dict_for_df[yr] = [
            julian_day, julian_cent, sgml, sgma, eceo, seoc, stlg,
            stan, svau, salg, mobe, ocor, asce, sdec, vary, eqtm,
            hans, soln, srif, setf, noon, rise, sset, sdur, trst,
            hand, szen, sela, aprx, atmr, azmt,
        ]
    df = pd.DataFrame.from_dict(
        dict_for_df,
        orient="index",
        columns=[
            "Julian Day",
            "Julian Century",
            "Solar Geometric Mean Longitude",
            "Solar Geometric Mean Anomaly",
            "Eccentricity Earth Orbit",
            "Solar Equation of Center",
            "Solar True Longitude",
            "Solar True Anomaly",
            "Solar Radius Vector AUs",
            "Solar Apparent Longitude",
            "Mean Obliquity of Ecliptic",
            "Obliquity Correction Degrees",
            "Solar Accent Return",
            "Solar Decline",
            "Var Y",
            "Equation Of Time Min",
            "Hour Angle Sunrise",
            "Solar Noon (float)",
            "Sunrise (float)",
            "Sunset (float)",
            "Solar Noon",
            "Sunrise",
            "Sunset",
            "Sunlight Durration (minutes)",
            "Ture Solar Time",
            "Hour Angle Deg",
            "Solar Zenith Angle (degrees)",
            "Solar Elevation Angle (degrees)",
            "Approximate Atmospheric Refraction (degrees)",
            "Solar Elevation Corrected ATM Refraction (degrees)",
            "Solar Azimuth Angle (degrees cw from North)",
        ],
    )
    return df


def to_dict(start_date, lat, long, local_tz, number_of_years):
    """Returns a Pandas DataFrame of all the calculations for various solar projects.
    With a datetime.date for starting date, Latitude, lat, local Longitude, long
    and local Time Zone as a positive or negative integer. """

    # this will evelntially be the daylight savings output:
    tz_adjust = 0
    year = int(start_date.year)
    # Number of days claculation
    total_days = 0
    for _y in range(1, number_of_years + 1):
        if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            total_days += 366
        else:
            total_days += 365

    dict_for_df = {}
    for i in range(0, total_days):
        # Our arguments are passed as positional maybe not best practice?
        yr = start_date + datetime.timedelta(days=i)
        julian_day = calc.julian_day(yr, local_tz)
        julian_cent = calc.julian_century(julian_day)
        sgml = calc.solar_geometric_mean_longitude(julian_cent)
        sgma = calc.solar_geometric_mean_anomaly(julian_cent)
        eceo = calc.eccentricity_earth_orbit(julian_cent)
        seoc = calc.solar_equation_of_center(julian_cent, sgma)
        stlg = calc.solar_true_longitude(sgml, seoc)
        stan = calc.solar_true_anomaly(sgma, seoc)
        svau = calc.solar_radius_vector_aus(eceo, stan)
        salg = calc.solar_apparent_longitude(stlg, julian_cent)
        mobe = calc.mean_obliquity_ecliptic(julian_cent)
        ocor = calc.obliquity_correction_deg(mobe, julian_cent)
        asce = calc.solar_accent_return(salg, ocor)
        sdec = calc.solar_decline(ocor, salg)
        vary = calc.var_y(ocor)
        eqtm = calc.equation_of_time(vary, sgml, eceo, sgma)
        hans = calc.hour_angle_sunrise(lat, sdec)
        soln = calc.solar_noon_float(eqtm, long, local_tz)
        srif = calc.sunrise_float(soln, hans)
        setf = calc.sunset_float(soln, hans)
        noon = calc.make_time(soln, yr, tz_adjust)
        rise = calc.make_time(srif, yr, tz_adjust)
        sset = calc.make_time(setf, yr, tz_adjust)
        sdur = calc.sunlight_duration(hans)
        trst = calc.true_solar_time_min(eqtm, long, local_tz)
        hand = calc.hour_angle_deg(trst)
        szen = calc.solar_zenith_angle(lat, sdec, hand)
        sela = calc.solar_elevation_angle(szen)
        aprx = calc.approx_atmospheric_refraction(sela)
        atmr = calc.solar_elevation_corrected_atm_refraction(aprx, sela)
        azmt = calc.solar_azimuth(hand, lat, szen, sdec)
        dict_for_df[yr] = [
            julian_day, julian_cent, sgml, sgma, eceo, seoc, stlg,
            stan, svau, salg, mobe, ocor, asce, sdec, vary, eqtm,
            hans, soln, srif, setf, noon, rise, sset, sdur, trst,
            hand, szen, sela, aprx, atmr, azmt,
        ]
    return dict_for_df


def sunrise_set_noon(date, lat, long, local_tz, tz_adjust=0):
    julian_day = calc.julian_day(date, local_tz)
    julian_cent = calc.julian_century(julian_day)
    sgml = calc.solar_geometric_mean_longitude(julian_cent)
    sgma = calc.solar_geometric_mean_anomaly(julian_cent)
    eceo = calc.eccentricity_earth_orbit(julian_cent)
    seoc = calc.solar_equation_of_center(julian_cent, sgma)
    stlg = calc.solar_true_longitude(sgml, seoc)
    #stan = calc.solar_true_anomaly(sgma, seoc)
    #svau = calc.solar_radius_vector_aus(eceo, stan)
    salg = calc.solar_apparent_longitude(stlg, julian_cent)
    mobe = calc.mean_obliquity_ecliptic(julian_cent)
    ocor = calc.obliquity_correction_deg(mobe, julian_cent)
    #asce = calc.solar_accent_return(salg, ocor)
    sdec = calc.solar_decline(ocor, salg)
    vary = calc.var_y(ocor)
    eqtm = calc.equation_of_time(vary, sgml, eceo, sgma)
    hans = calc.hour_angle_sunrise(lat, sdec)
    soln = calc.solar_noon_float(eqtm, long, local_tz)
    srif = calc.sunrise_float(soln, hans)
    setf = calc.sunset_float(soln, hans)
    noon = calc.make_time(soln, date, tz_adjust)
    rise = calc.make_time(srif, date, tz_adjust)
    sset = calc.make_time(setf, date, tz_adjust)
    return (rise, sset, noon)

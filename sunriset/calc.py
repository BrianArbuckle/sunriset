# This file is released under the MIT License OSI Approved.

import datetime
from datetime import timedelta
import math
import pytz

ordinal_adj = 1721424.5
days_century = 2451545  # this is Saturday, A.D. 2000 Jan 1  in the Julian Calendar
day_per_century = 36525


def make_time(time_float, d_utz, tz_adjust):
    """This function converts time_float to time of day"""
    time = datetime.timedelta(time_float + tz_adjust)
    return time


def make_date_time(time_float, d_utz, tz_adjust):
    """This function converts time_float to local datetime"""
    local_dt_midnight = datetime.datetime.combine(d_utz, datetime.time())
    date_time = datetime.timedelta(time_float + tz_adjust)
    dt = local_dt_midnight + date_time
    dt = local_pytz.localize(dt)
    return dt


def julian_day(usr_date, tz=0):
    """Returns a local Julian Day float with datetime object 'date', 
    which defaults to today, and time zone, tz as a positive or negative integer.
    
    The Julian Calendar start day Monday, January 1, 4713 12:00 Noon BCE.
    """
    ordinal_adj = 1721424.5
    if isinstance(usr_date, datetime.date) == True:
        usr_date = usr_date.toordinal() + ordinal_adj
    else:
        usr_date = usr_date.date().toordinal() + ordinal_adj
    jd_local = usr_date + 0.5 - tz / 24
    return jd_local


def julian_century(jd_local):
    """Returns the Julian Century with Julian Day, julian_local."""
    days_century = 2451545  # this is Saturday, AD 2000 Jan 1 in the Julian Calendar
    day_per_century = 36525
    for i in range(2451545, 0, -36525):
        if jd_local < i:
            days_century = i - day_per_century
        else:
            break
    julian_cent = (jd_local - days_century) / day_per_century
    return julian_cent


def solar_geometric_mean_longitude(julian_century):
    """Returns the Solar Geometric Mean with Julian Century, julian_century."""
    solar_geometric_mean_longitude = (
        280.46646 + julian_century * (36000.76983 + julian_century * 0.0003032)
    ) % 360
    return solar_geometric_mean_longitude


def solar_geometric_mean_anomaly(julian_century):
    """Returns the Anomaly of Solar Geometric Mean with Julian Century, julian_century."""
    solar_geometric_mean_anomaly = 357.52911 + julian_century * (
        35999.05029 - 0.0001537 * julian_century
    )
    return solar_geometric_mean_anomaly


def eccentricity_earth_orbit(julian_century):
    """Returns the Eccentricity or Earth Orbit with Julian Century, julian_century."""
    ecc_earth_orb = 0.016708634 - julian_century * (
        0.000042037 + 0.0000001267 * julian_century
    )
    return ecc_earth_orb


def solar_equation_of_center(julian_century, solar_geometric_mean_anomaly):
    """Returns the Solar Equation of Center with Julian Century, julian_century and 
    Solar Geometric Mean Anomaly, solar_geometric_mean_anomaly."""
    solar_equation_of_center = (
        math.sin(math.radians(solar_geometric_mean_anomaly))
        * (1.914602 - julian_century * (0.004817 + 0.000014 * julian_century))
        + math.sin(math.radians(2 * solar_geometric_mean_anomaly))
        * (0.019993 - 0.000101 * julian_century)
        + math.sin(math.radians(3 * solar_geometric_mean_anomaly)) * 0.000289
    )
    return solar_equation_of_center


def solar_true_longitude(solar_geometric_mean_longitude, solar_equation_of_center):
    """Returns the Solar True Longitude with Solar Geometric Mean Longitude, 
    solar_geometric_mean_longitude, and Solar Equation of Center,
    solar_equation_of_center."""
    solar_true_longitude = solar_geometric_mean_longitude + solar_equation_of_center
    return solar_true_longitude


def solar_true_anomaly(solar_geometric_mean_anomaly, solar_equation_of_center):
    """Returns the Solar True Anomaly with Solar Geometric Mean Anomaly, 
    solar_geometric_mean_anomaly, and Solar Equation of Center,
    solar_equation_of_center."""
    solar_true_anomaly = solar_geometric_mean_anomaly + solar_equation_of_center
    return solar_true_anomaly


def solar_radius_vector_aus(eccentricity_earth_orbit, solar_true_anomaly):
    """Returns the Solar Radius Vector.
    Measured as distance in Astronomical Units, (AUs). 
    With Eccentricity of Earth's Orbit, eccentricity_earth_orbit, and Solar 
    True Anomaly, solar_true_anomaly.
    """
    solar_rad_vector_aus = (1.000001018 * (1 - eccentricity_earth_orbit ** 2)) / (
        1 + eccentricity_earth_orbit * math.cos(math.radians(solar_true_anomaly))
    )
    return solar_rad_vector_aus


def solar_apparent_longitude(solar_true_longitude, julian_century):
    """Returns the SolarApparentLongitude with Solar True Longitude, 
    solar_true_longitude, and Julian Century, julian_century."""
    solar_apparent_longitude = (
        solar_true_longitude
        - 0.00569
        - 0.00478 * math.sin(math.radians(125.04 - 1934.136 * julian_century))
    )
    return solar_apparent_longitude


def mean_obliquity_ecliptic(julian_century):
    """Returns the Mean Obliquity of Ecliptic in Degrees with Julian Century, 
    julian_century."""
    mean_obliquity_of_ecliptic = (
        23
        + (
            26
            + (
                (
                    21.448
                    - julian_century
                    * (46.815 + julian_century * (0.00059 - julian_century * 0.001813))
                )
            )
            / 60
        )
        / 60
    )
    return mean_obliquity_of_ecliptic


def obliquity_correction_deg(mean_obliquity_of_ecliptic_deg, julian_century):
    """Returns Obliquity Correction in Degrees with Mean Obliquity Ecliptic, 
    mean_obliquity_of_ecliptic_deg and Julian Century, julian_century."""
    obliquity_correction = mean_obliquity_of_ecliptic_deg + 0.00256 * math.cos(
        math.radians(125.04 - 1934.136 * julian_century)
    )
    return obliquity_correction


def solar_accent_return(solar_apparent_longitude, obliquity_correction):
    """Returns SolarAccentReturn with Solar Apparent Longitude, 
    solar_apparent_longitude and Obliquity Correction , obliquity_correction"""
    solar_return_ascent = math.degrees(
        math.atan2(
            math.cos(math.radians(solar_apparent_longitude)),
            math.cos(math.radians(obliquity_correction))
            * math.sin(math.radians(solar_apparent_longitude)),
        )
    )
    return solar_return_ascent


def solar_decline(obliquity_correction, solar_apparent_longitude):
    """Returns Solar Decline in degrees, with Obliquity Correction, obliquity_correction
    Solar Apparent Longitude, solar_apparent_longitude"""
    solar_decline = math.degrees(
        math.asin(
            math.sin(math.radians(obliquity_correction))
            * math.sin(math.radians(solar_apparent_longitude))
        )
    )
    return solar_decline


def var_y(obliquity_correction):
    """Returns Var Y with Obliquity Correction, obliquity_correction"""
    var_y = math.tan(math.radians(obliquity_correction / 2)) * math.tan(
        math.radians(obliquity_correction / 2)
    )
    return var_y


def equation_of_time(
    var_y,
    solar_geometric_mean_longitude,
    eccentricity_earth_orbit,
    solar_geometric_mean_anomaly,
):
    """Returns Equation Of Time, in minutes, with Var Y, var_y, 
    Solar Geometric Mean Longitude, solar_geometric_mean_longitude, 
    Eccentricity Earth Orbit, eccentricity_earth_orbit, Solar Geometric 
    Mean Anomaly, solar_geometric_mean_anomaly.
    """
    equation_of_time = 4 * math.degrees(
        var_y * math.sin(2 * math.radians(solar_geometric_mean_longitude))
        - 2
        * eccentricity_earth_orbit
        * math.sin(math.radians(solar_geometric_mean_anomaly))
        + 4
        * eccentricity_earth_orbit
        * var_y
        * math.sin(math.radians(solar_geometric_mean_anomaly))
        * math.cos(2 * math.radians(solar_geometric_mean_longitude))
        - 0.5
        * var_y
        * var_y
        * math.sin(4 * math.radians(solar_geometric_mean_longitude))
        - 1.25
        * eccentricity_earth_orbit
        * eccentricity_earth_orbit
        * math.sin(2 * math.radians(solar_geometric_mean_anomaly))
    )
    return equation_of_time


def hour_angle_sunrise(lat, solar_decline):
    """Returns Hour Angle, in degrees, with Latitude, lat and Solar Decline Deg, solar_decline"""
    hour_angle_sunrise = math.degrees(
        math.acos(
            math.cos(math.radians(90.833))
            / (math.cos(math.radians(lat)) * math.cos(math.radians(solar_decline)))
            - math.tan(math.radians(lat)) * math.tan(math.radians(solar_decline))
        )
    )
    return hour_angle_sunrise


def solar_noon_float(equation_of_time, long, local_tz):
    """Returns Solar Noon as a float with the Equation Of Time, equation_of_time"""
    solar_noon_float = (720 - 4 * long - equation_of_time + local_tz * 60) / 1440
    # Original caculation contained needs work:
    # solar_noon_lst_float = (720 - 4 * long - equation_of_time + local_tz_dst * 60) / 1440
    return solar_noon_float


def sunrise_float(solar_noon_float, hour_angle_sunrise):
    """Returns Sunrise as float with Solar Noon Float, solar_noon_float
    and Hour Angle Deg, hour_angle_deg"""
    sunrise_float = (solar_noon_float * 1440 - hour_angle_sunrise * 4) / 1440
    return sunrise_float


def sunset_float(solar_noon_float, hour_angle_sunrise):
    """Returns Sunset as float with Solar Noon Float, solar_noon_float
    and Hour Angle Deg, hour_angle_deg"""
    sunset_float = (solar_noon_float * 1440 + hour_angle_sunrise * 4) / 1440
    return sunset_float


def sunlight_duration(hour_angle_sunrise):
    """Returns the duration of Sunlight, in minutes, with Hour Angle in degrees, 
    hour_angle."""
    sunlight_durration = 8 * hour_angle_sunrise  # this seems like the wrong output
    return sunlight_durration


def true_solar_time_min(equation_of_time, long, local_tz):
    """Returns True Solar time in minutes, with Equation of Time, equation_of_time, 
    Longitude, long and Local Time Zone, local tz."""
    true_solar_time = (0.5 * 1440 + equation_of_time + 4 * long - 60 * local_tz) % 1440
    return true_solar_time


def hour_angle_deg(true_solar_time):
    """Returns Hour Angle in Degrees, with True Solar Time, true_solar_time."""
    if true_solar_time / 4 < 0:
        hour_angle_deg = true_solar_time / 4 + 180
    else:
        hour_angle_deg = true_solar_time / 4 - 180
    return hour_angle_deg


def solar_zenith_angle(lat, solar_decline, hour_angle):
    """Returns Solar Zenith Angle in Degrees, with Latitude, lat, Solar Decline (Degrees), 
    solar_decline, Hour Angle (Degrees), hour_angle."""
    solar_zenith_angle = math.degrees(
        math.acos(
            math.sin(math.radians(lat)) * math.sin(math.radians(solar_decline))
            + math.cos(math.radians(lat))
            * math.cos(math.radians(solar_decline))
            * math.cos(math.radians(hour_angle))
        )
    )
    return solar_zenith_angle


def solar_elevation_angle(solar_zenith_angle):
    """Returns Solar Angle in Degrees, with Solar Zenith Angle, solar_zenith_angle."""
    solar_elevation_angle = 90 - solar_zenith_angle
    return solar_elevation_angle


def approx_atmospheric_refraction(solar_elevation_angle):
    """Returns Approximate Atmospheric Refraction in degrees with Solar Elevation 
    Angle, solar_elevation_angle."""
    if solar_elevation_angle > 85:
        approx_atmospheric_refraction = 0
    elif solar_elevation_angle > 5:
        approx_atmospheric_refraction = (
            58.1 / math.tan(math.radians(solar_elevation_angle))
            - 0.07 / pow(math.tan(math.radians(solar_elevation_angle)), 3)
            + 0.000086 / pow(math.tan(math.radians(solar_elevation_angle)), 5)
        ) / 3600
    elif solar_elevation_angle > -0.575:
        approx_atmospheric_refraction = (
            1735
            + solar_elevation_angle
            * (
                -518.2
                + solar_elevation_angle
                * (
                    103.4
                    + solar_elevation_angle * (-12.79 + solar_elevation_angle * 0.711)
                )
            )
        ) / 3600
    else:
        approx_atmospheric_refraction = (
            -20.772 / math.tan(math.radians(solar_elevation_angle))
        ) / 3600
    return approx_atmospheric_refraction


def solar_elevation_corrected_atm_refraction(
    approx_atmospheric_refraction, solar_elevation_angle
):
    """Returns the Solar Elevation Corrected Atmospheric Refraction, with the 
    Approximate Atmospheric Refraction, approx_atmospheric_refraction and Solar 
    Elevation Angle, solar_elevation_angle."""
    solar_elevation_corrected_atm_refraction = (
        approx_atmospheric_refraction + solar_elevation_angle
    )
    return solar_elevation_corrected_atm_refraction


def solar_azimuth(hour_angle, lat, solar_zenith_angle, solar_decline):
    """Returns Solar Azimuth Angle Degrees Clockwise from North, with Latitude, lat and 
    Solar Zenith Angle, solar_zenith_angle and Solar Decline, solar_decline."""
    if hour_angle > 0:
        solar_azimuth_angle_deg_cw_from_n = (
            math.degrees(
                math.acos(
                    (
                        (
                            math.sin(math.radians(lat))
                            * math.cos(math.radians(solar_zenith_angle))
                        )
                        - math.sin(math.radians(solar_decline))
                    )
                    / (
                        math.cos(math.radians(lat))
                        * math.sin(math.radians(solar_zenith_angle))
                    )
                )
            )
            + 180
        ) % 360
    else:
        solar_azimuth_angle_deg_cw_from_n = (
            540
            - math.degrees(
                math.acos(
                    (
                        (
                            math.sin(math.radians(lat))
                            * math.cos(math.radians(solar_zenith_angle))
                        )
                        - math.sin(math.radians(solar_decline))
                    )
                    / (
                        math.cos(math.radians(lat))
                        * math.sin(math.radians(solar_zenith_angle))
                    )
                )
            )
        ) % 360
    return solar_azimuth_angle_deg_cw_from_n




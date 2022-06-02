# This file is released under the MIT License OSI Approved.

import datetime
import math
from datetime import timedelta

import pytz

ordinal_adj = 1721424.5
days_century = 2451545  # this is Saturday, A.D. 2000 Jan 1  in the Julian Calendar
day_per_century = 36525


def make_time(time_float: float, d_utz, tz_adjust: float) -> datetime.timedelta:
    """This function converts time_float to datetime.timedelta and is used
    for internal calculations.

    Args:
        time_float (float): In Days, where the whole number 10, for example,
        would be ten days. While 10.5 would be 10 and a half days.
        tz_adjust (float): Temporary daylight savings tool.
        d_utz (): placeholder for inheritance

    Returns:
        datetime.timedelta: a timedelta is in days and seconds.
    """
    return datetime.timedelta(time_float + tz_adjust)


def make_date_time(time_float, d_utz, tz_adjust):
    """This function converts time_float to local datetime"""
    local_dt_midnight = datetime.datetime.combine(d_utz, datetime.time())
    date_time = datetime.timedelta(time_float + tz_adjust)
    dt = local_dt_midnight + date_time
    dt = local_pytz.localize(dt)
    return dt


def julian_day(usr_date: datetime.date, tz: float = 0) -> float:
    """Returns a local Julian Day float with datetime object 'date',
    which defaults to today, and time zone, tz as a positive or negative integer.

    The Julian Calendar start day Monday, January 1, 4713 12:00 Noon BCE.
    """
    ordinal_adj = 1721424.5
    if isinstance(usr_date, datetime.date):
        usr_date = usr_date.toordinal() + ordinal_adj
    else:
        usr_date = usr_date.date().toordinal() + ordinal_adj
    return usr_date + 0.5 - tz / 24


def julian_century(jd_local: float) -> float:
    """Returns the Julian Century with Julian Day, julian_local."""
    days_century = 2451545  # this is Saturday, AD 2000 Jan 1 in the Julian Calendar
    day_per_century = 36525
    for i in range(2451545, 0, -36525):
        if jd_local < i:
            days_century = i - day_per_century
        else:
            break
    return (jd_local - days_century) / day_per_century


def solar_geometric_mean_longitude(julian_century: float) -> float:
    """Returns the Solar Geometric Mean with Julian Century, julian_century."""
    return (
        280.46646 + julian_century * (36000.76983 + julian_century * 0.0003032)
    ) % 360


def solar_geometric_mean_anomaly(julian_century: float) -> float:
    """Returns the Anomaly of Solar Geometric Mean with Julian Century, julian_century."""
    return 357.52911 + julian_century * (35999.05029 - 0.0001537 * julian_century)


def eccentricity_earth_orbit(julian_century: float) -> float:
    """Returns the Eccentricity or Earth Orbit with Julian Century, julian_century."""
    return 0.016708634 - julian_century * (0.000042037 + 0.0000001267 * julian_century)


def solar_equation_of_center(julian_century, solar_geometric_mean_anomaly):
    """Returns the Solar Equation of Center with Julian Century, julian_century and
    Solar Geometric Mean Anomaly, solar_geometric_mean_anomaly."""
    return (
        math.sin(math.radians(solar_geometric_mean_anomaly))
        * (1.914602 - julian_century * (0.004817 + 0.000014 * julian_century))
        + math.sin(math.radians(2 * solar_geometric_mean_anomaly))
        * (0.019993 - 0.000101 * julian_century)
        + math.sin(math.radians(3 * solar_geometric_mean_anomaly)) * 0.000289
    )


def solar_true_longitude(solar_geometric_mean_longitude, solar_equation_of_center):
    """Returns the Solar True Longitude with Solar Geometric Mean Longitude,
    solar_geometric_mean_longitude, and Solar Equation of Center,
    solar_equation_of_center."""
    return solar_geometric_mean_longitude + solar_equation_of_center


def solar_true_anomaly(solar_geometric_mean_anomaly, solar_equation_of_center):
    """Returns the Solar True Anomaly with Solar Geometric Mean Anomaly,
    solar_geometric_mean_anomaly, and Solar Equation of Center,
    solar_equation_of_center."""
    return solar_geometric_mean_anomaly + solar_equation_of_center


def solar_radius_vector_aus(eccentricity_earth_orbit, solar_true_anomaly):
    """Returns the Solar Radius Vector.
    Measured as distance in Astronomical Units, (AUs).
    With Eccentricity of Earth's Orbit, eccentricity_earth_orbit, and Solar
    True Anomaly, solar_true_anomaly.
    """
    return (1.000001018 * (1 - eccentricity_earth_orbit**2)) / (
        1 + eccentricity_earth_orbit * math.cos(math.radians(solar_true_anomaly))
    )


def solar_apparent_longitude(solar_true_longitude, julian_century):
    """Returns the SolarApparentLongitude with Solar True Longitude,
    solar_true_longitude, and Julian Century, julian_century."""
    return (
        solar_true_longitude
        - 0.00569
        - 0.00478 * math.sin(math.radians(125.04 - 1934.136 * julian_century))
    )


def mean_obliquity_ecliptic(julian_century):
    """Returns the Mean Obliquity of Ecliptic in Degrees with Julian Century,
    julian_century."""
    return (
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


def obliquity_correction_deg(mean_obliquity_of_ecliptic_deg, julian_century):
    """Returns Obliquity Correction in Degrees with Mean Obliquity Ecliptic,
    mean_obliquity_of_ecliptic_deg and Julian Century, julian_century."""
    return mean_obliquity_of_ecliptic_deg + 0.00256 * math.cos(
        math.radians(125.04 - 1934.136 * julian_century)
    )


def solar_accent_return(solar_apparent_longitude, obliquity_correction):
    """Returns SolarAccentReturn with Solar Apparent Longitude,
    solar_apparent_longitude and Obliquity Correction , obliquity_correction"""
    return math.degrees(
        math.atan2(
            math.cos(math.radians(solar_apparent_longitude)),
            math.cos(math.radians(obliquity_correction))
            * math.sin(math.radians(solar_apparent_longitude)),
        )
    )


def solar_decline(obliquity_correction, solar_apparent_longitude):
    """Returns Solar Decline in degrees, with Obliquity Correction, obliquity_correction
    Solar Apparent Longitude, solar_apparent_longitude"""
    return math.degrees(
        math.asin(
            math.sin(math.radians(obliquity_correction))
            * math.sin(math.radians(solar_apparent_longitude))
        )
    )


def var_y(obliquity_correction):
    """Returns Var Y with Obliquity Correction, obliquity_correction"""
    return math.tan(math.radians(obliquity_correction / 2)) * math.tan(
        math.radians(obliquity_correction / 2)
    )


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
    return 4 * math.degrees(
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


def hour_angle_sunrise(lat, solar_decline):
    """Returns Hour Angle, in degrees, with Latitude, lat and Solar Decline Deg, solar_decline"""
    return math.degrees(
        math.acos(
            math.cos(math.radians(90.833))
            / (math.cos(math.radians(lat)) * math.cos(math.radians(solar_decline)))
            - math.tan(math.radians(lat)) * math.tan(math.radians(solar_decline))
        )
    )


def solar_noon_float(equation_of_time, long, local_tz):
    """Returns Solar Noon as a float with the Equation Of Time, equation_of_time"""
    # Original caculation contained needs work:
    # solar_noon_lst_float = (720 - 4 * long - equation_of_time + local_tz_dst * 60) / 1440
    return (720 - 4 * long - equation_of_time + local_tz * 60) / 1440


def sunrise_float(solar_noon_float: float, hour_angle_sunrise: float) -> float:
    """Returns Sunrise as float with Solar Noon Float, solar_noon_float
    and Hour Angle Deg, hour_angle_deg"""
    return (solar_noon_float * 1440 - hour_angle_sunrise * 4) / 1440


def sunset_float(solar_noon_float, hour_angle_sunrise):
    """Returns Sunset as float with Solar Noon Float, solar_noon_float
    and Hour Angle Deg, hour_angle_deg"""
    return (solar_noon_float * 1440 + hour_angle_sunrise * 4) / 1440


def sunlight_duration(hour_angle_sunrise):
    """Returns the duration of Sunlight, in minutes, with Hour Angle in degrees,
    hour_angle."""
    return 8 * hour_angle_sunrise


def true_solar_time_min(equation_of_time, long, local_tz):
    """Returns True Solar time in minutes, with Equation of Time, equation_of_time,
    Longitude, long and Local Time Zone, local tz."""
    return (0.5 * 1440 + equation_of_time + 4 * long - 60 * local_tz) % 1440


def hour_angle_deg(true_solar_time):
    """Returns Hour Angle in Degrees, with True Solar Time, true_solar_time."""
    return (
        true_solar_time / 4 + 180 if true_solar_time < 0 else true_solar_time / 4 - 180
    )


def solar_zenith_angle(lat: float, solar_decline: float, hour_angle: float) -> float:
    """Returns Solar Zenith Angle in Degrees, with Latitude, lat, Solar Decline (Degrees),
    solar_decline, Hour Angle (Degrees), hour_angle."""
    return math.degrees(
        math.acos(
            math.sin(math.radians(lat)) * math.sin(math.radians(solar_decline))
            + math.cos(math.radians(lat))
            * math.cos(math.radians(solar_decline))
            * math.cos(math.radians(hour_angle))
        )
    )


def solar_elevation_angle(solar_zenith_angle: float) -> float:
    """Returns Solar Angle in Degrees, with Solar Zenith Angle, solar_zenith_angle."""
    return 90 - solar_zenith_angle


def approx_atmospheric_refraction(solar_elevation_angle: float) -> float:
    """Returns Approximate Atmospheric Refraction in degrees with Solar Elevation
    Angle, solar_elevation_angle."""
    if solar_elevation_angle > 85:
        return 0
    elif solar_elevation_angle > 5:
        return (
            58.1 / math.tan(math.radians(solar_elevation_angle))
            - 0.07 / pow(math.tan(math.radians(solar_elevation_angle)), 3)
            + 0.000086 / pow(math.tan(math.radians(solar_elevation_angle)), 5)
        ) / 3600

    elif solar_elevation_angle > -0.575:
        return (
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
        return (-20.772 / math.tan(math.radians(solar_elevation_angle))) / 3600


def solar_elevation_corrected_atm_refraction(
    approx_atmospheric_refraction: float, solar_elevation_angle: float
) -> float:
    """Returns the Solar Elevation Corrected Atmospheric Refraction, with the
    Approximate Atmospheric Refraction, approx_atmospheric_refraction and Solar
    Elevation Angle, solar_elevation_angle."""
    return approx_atmospheric_refraction + solar_elevation_angle


def solar_azimuth(
    hour_angle: float, lat: float, solar_zenith_angle: float, solar_decline: float
) -> float:
    """Returns Solar Azimuth Angle Degrees Clockwise from North, with Latitude, lat and
    Solar Zenith Angle, solar_zenith_angle and Solar Decline, solar_decline."""
    return (
        (
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
        )
        % 360
        if hour_angle > 0
        else (
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
        )
        % 360
    )

Sunshine
==========

Solar Calculator
==========

This packege generates **Solar Posistion Data** based on Latitiude, Logitude, Date and Time Zone.  
*Future updates will include elevation data.* 

The initial goal was to create a *simple* function that produced the daily sunrise and sunset for any given location. These calculations create a large amount of usefull data that can be used for other solar related calculations and are based on the caculations from [NOAA (National Oceanic & Atmospheric Administration)](https://www.esrl.noaa.gov/gmd/grad/solcalc/).  The calaculations can be used in various projects, including but not limited to, Solar Panel Placement, Sun Exposure for Building Construction, Photography and Circadian Rhythm based IOT projects and Timers. 

Get It Now
==========

    $ pip install sunshine


Documentation
=============

The built in outputs include:

Pandas Dataframe of all built in calculations. 

Daily Sunrise, Sunset & Solar Noon time. - In Progress

Solar Plots

Solar Window

Sunrise and Sunset Location


Requirements
============

datetime

datetime - timedelta

math

pytz (still in progress)

pandas

Additional Requirements
============ 
Matplotlib 

-----

***Disclaimer Data for Litigation***
The sunshine Solar Calculator is for research and recreational use only. The authors cannot certify or authenticate sunrise, sunset or solar position data. We do not collect observations of astronomical data, and due to atmospheric conditions our calculated results may vary significantly from actual observed values.

For further information, please see the U.S. Naval Observatory's page Astronomical Data Used for Litigation.

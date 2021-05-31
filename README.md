# sqlalchemy-challenge

I've decided to treat myself to a long holiday vacation in Honolulu, Hawaii! To help with my trip planning, I need to do some climate analysis on the area. The following outlines what I did.

I used SQLAlchemy ORM queries, pandas and matplotlib to do some basic climate analysis and data exploration of the sqlite climate database.

Precipitation Analysis

Designed a query to retrieve the last 12 months of precipitation data. Selecting only the `date` and `prcp` values, loaded the query results into a Pandas DataFrame and plotted the results.

Stations Analysis

Designed a query to calculate the total number of stations and then a query to find the most active stations. Plotted a histogram of temperature versus frequency for the stations with the most observations.

results_2  = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').\
filter(measurement.date > (last_date_dt  - dt.timedelta(days=366))).all()

Other Analyses

Identified the average temperature in June and December at all stations across all available years in the dataset. Used the paired t-test to determine whether the difference in the means, if any, is statistically significant. Query to obtain June temps:

june_temps = session.query(*sel).filter(func.strftime("%m", measurement.date) == "06").\
group_by(measurement.station).group_by(func.strftime("%Y", measurement.date)).all()

The two datasets were of different lengths and so a unique key (year + station name) was created to accurately pair and eliminate any non-paired observations. The June mean is 74.8F and the December mean is 71.2F. scipy.stats was used to calculate the p-value 8.6e-13 indicating the null hypothesis of equal averages can be rejected and that December and June temperatures ARE statistically different (the histogram seems to support this).

Flask API

Designed a Flask API based on some of the queries above.

John Russell
May 31, 2021




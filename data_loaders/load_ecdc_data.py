import pandas as pd
import os.path
import sys
import logging

log = logging.getLogger(
    "ECDC Data Loader")
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

# Read in the European Centre for Disease Prevention and Control Data into a dataframe.

log.info("Loading European Centre for Disease Prevention and Control timeseries data from opendata.ecdc.europa.eu")
df = pd.read_csv(
    "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv")
log.info(f"Loaded {len(df)} records; now transforming data")

# Use internal data to create dates; only keep `date` column
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
df.drop(['dateRep', 'day', 'month', 'year'], inplace=True, axis=1)

# Just to be safe, let's sort by name and date. Probably not 
# necessary but better safe than sorry!.
df = df.sort_values(['countriesAndTerritories', 'date'])

# Each data set has a unique name. Let's create groups.
g = df.groupby('countriesAndTerritories')

# The parameter 'day' is the number of days since the first 
# day of data collection for the group.
df['day'] = g['date'].transform(lambda x: (x - min(x))).apply(lambda x: x.days)


# We'll 'rename' some of the columns to be consistent
# with the parameters file.

df['new_positives'] = df.cases
df['new_death'] = df.deaths
df['population'] = df.popData2018
df.drop(['cases', 'deaths', 'popData2018'], inplace=True, axis=1)


# And save it to the data directory.

here = os.path.abspath(os.path.dirname(__file__))
data_home = os.path.join(here, "../data")
if not os.path.exists(data_home):
    log.info(f"Creating data directory {data_home}")
    os.makedirs(data_home)
path = os.path.join(data_home, "ecdc.csv")
log.info(f"Saving to {path}")
df.to_csv(path)
log.info(f"Script complete")
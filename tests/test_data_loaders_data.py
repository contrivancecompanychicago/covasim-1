'''
Quick validation of data scraper and covid-tracking-project csv data
'''

import os
import pandas as pd
import unittest

here = os.path.abspath(os.path.dirname(__file__))
data_loaders = os.path.join(here, "../data_loaders")
data_home = os.path.join(here, "../data")


def run_data_loaders():
    for filename in os.listdir(data_loaders):
        if filename.endswith(".py"):
            with open(os.path.join(data_loaders, filename)) as f:
                code = compile(f.read(), os.path.join(data_loaders, filename), 'exec')
                exec(code, globals(), globals())


# @unittest.skip("Only run if want to test data_loaders")
class TestDataLoadersData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Run load covid data scripts if don't exist
        filelist = ['corona_data_scraper.csv', 'covid-tracking-project-data.csv', 'ecdp_data.csv']
        for f in filelist:
            if not os.path.exists(os.path.join(data_home, f)):
                run_data_loaders()

    def setUp(self):
        self.datadir = data_home
        self.date = "2020-03-08"

    def test_datascraper_get_tawain_stats(self):
        data_csv = os.path.join(self.datadir, "corona_data_scraper.csv")

        df = pd.read_csv(data_csv, dtype='unicode')
        pd_df = pd.DataFrame(df)

        # filter by country and 1 date
        country = 'Taiwan'
        taiwan_date = pd_df[(pd_df['country'] == country) & (pd_df['date'] == self.date)]
        # validate date's positive value is 45
        self.assertEqual(taiwan_date['positives'].values[0], "45.0")

    def test_covid_tracking_project_data(self):
        data_csv = os.path.join(self.datadir, "covid-tracking-project-data.csv")

        df = pd.read_csv(data_csv, dtype='unicode')
        pd_df = pd.DataFrame(df)

        # filter for 1 date
        particular_date = pd_df['date'] == self.date
        date_data = df[particular_date]
        # validate date's first row negative value is 12
        self.assertTrue(date_data['negative'].values[0] == "14.0")

    def test_ecdp_data(self):
        data_csv = os.path.join(self.datadir, "ecdp_data.csv")

        df = pd.read_csv(data_csv, dtype='unicode')
        pd_df = pd.DataFrame(df)

        # filter by country and 1 date
        country = 'Afghanistan'
        afg_date = pd_df[(pd_df['countriesAndTerritories'] == country) & (pd_df['date'] == self.date)]
        self.assertEqual(afg_date['population'].values[0], "37172386.0")

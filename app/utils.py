import os
import numpy as np
import pandas as pd

import datetime as dt
import matplotlib.dates as mdates


class Data:
    def __init__(self, company, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.company = company
        self.dataset_path = '.\dataset'

    def getPath(self):
        return os.path.join(self.dataset_path, self.company) + '.csv'

    def getModifedDataset(self):
        company_data = pd.read_csv(self.getPath(), parse_dates = ['Date'])
        return company_data[(company_data["Date"] > self.start_date) & (company_data["Date"] < self.end_date)].reset_index().drop(['index'], axis = 1)
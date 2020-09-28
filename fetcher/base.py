from datetime import datetime
from typing import List
import os
import pytz
from pandas import DataFrame
import pandas as pd
from requests_html import HTMLSession
from .Keyword import Keyword
import urllib.request


class BaseFetcher:
    data: DataFrame

    def __init__(self):
        # Output name
        self.name = "base"
        self.session = HTMLSession()
        self.data = None

    def fetch(self):
        self.download()
        cur_data = self.__fetch__()
        rows = [c.get_row_data() for c in cur_data]
        columns = Keyword.get_column_name()
        df = DataFrame(rows, columns=columns)
        if self.data is not None:
            self.data = self.data.append(df, ignore_index=True)
        else:
            self.data = df
        return self

    @staticmethod
    def get_cur_time() -> datetime:
        d = datetime.now()
        timezone = pytz.timezone("Asia/Hong_Kong")
        now = timezone.localize(d)
        return now

    def __fetch__(self) -> List[Keyword]:
        """
        Fetch keywords
        :arg
        """
        raise NotImplementedError

    def __get_output_name__(self):
        return f'{self.name}.csv'

    def download(self):
        """
        Download and load local csv
        :arg
        """
        if os.path.exists(self.__get_output_name__()):
            df = pd.read_csv(self.__get_output_name__())
            self.data = df
        return self

    def write_to_local(self):
        output: DataFrame
        if self.data is not None:
            self.data.to_csv(self.__get_output_name__(), index=True)
        else:
            raise Exception("Data is None")

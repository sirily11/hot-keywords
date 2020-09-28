from datetime import datetime
from typing import List
import os
import pytz
from pandas import DataFrame
import pandas as pd
from requests_html import HTMLSession
from .Keyword import Keyword
from tzlocal import get_localzone


class BaseFetcher:
    data: DataFrame

    def __init__(self):
        # Output name
        self.name = "base"
        self.session = HTMLSession()
        self.data = None

    def fetch(self):
        self.open_local()
        cur_data = self.__fetch__()
        rows = [c.get_row_data() for c in cur_data]
        columns = Keyword.get_column_name()
        df = DataFrame(rows, columns=columns)
        if self.data is not None:
            self.data = pd.concat([self.data, df], ignore_index=True)
        else:
            self.data = df
        return self

    @staticmethod
    def get_cur_time() -> datetime:
        local_tz = get_localzone()
        d = datetime.now()
        to_tz = pytz.timezone("Asia/Hong_Kong")
        local_now = local_tz.localize(d)
        now = local_now.astimezone(to_tz)
        return now

    def __fetch__(self) -> List[Keyword]:
        """
        Fetch keywords
        :arg
        """
        raise NotImplementedError

    def __get_output_name__(self):
        return f'{self.name}.csv'

    def open_local(self):
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
            self.data.to_csv(self.__get_output_name__(), index=False)
        else:
            raise Exception("Data is None")

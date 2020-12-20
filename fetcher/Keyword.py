"""
Author: Qiwei Li
"""
from datetime import datetime
from typing import List


class BaseData:
    def get_row_data(self) -> List[str]:
        """:arg
        Get list of row's contents
        """
        raise NotImplementedError

    @staticmethod
    def get_column_name() -> List[str]:
        raise NotImplementedError


class Keyword(BaseData):
    def __init__(self, rank: int, keyword: str, numbers: int, cur_time=datetime.now(), link=""):
        self.time = cur_time
        self.keyword = keyword
        self.numbers = numbers
        self.rank = rank
        self.link = link

    def get_row_data(self) -> List[str]:
        return [self.time, self.keyword, self.numbers, self.rank]

    @staticmethod
    def get_column_name() -> List[str]:
        return ['time', 'keyword', 'numbers', 'rank']

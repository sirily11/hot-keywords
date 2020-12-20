"""
Author: Qiwei Li
"""
from typing import List

from fetcher.Keyword import BaseData


class Post(BaseData):
    def get_row_data(self) -> List[str]:
        return [self.keyword, self.content]

    @staticmethod
    def get_column_name() -> List[str]:
        return ['keyword', 'content']

    def __init__(self, keyword: str, content: str):
        self.keyword = keyword
        self.content = content

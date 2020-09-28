from datetime import datetime
from typing import List


class Keyword:
    def __init__(self, rank: int, keyword: str, numbers: int, cur_time=datetime.now(), ):
        self.time = cur_time
        self.keyword = keyword
        self.numbers = numbers
        self.rank = rank

    def get_row_data(self) -> List[str]:
        return [self.time, self.keyword, self.numbers, self.rank]

    @staticmethod
    def get_column_name() -> List[str]:
        return ['time', 'keyword', 'numbers', 'rank']

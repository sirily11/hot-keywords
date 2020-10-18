from datetime import datetime
from typing import List
import os
import pytz
from pandas import DataFrame
import pandas as pd
from requests_html import HTMLSession
from .Keyword import Keyword
from tzlocal import get_localzone
from .Post import Post
from tqdm import tqdm

class BaseFetcher:
    keywords: DataFrame
    posts: DataFrame

    def __init__(self):
        # Output name
        self.name = "base"
        self.session = HTMLSession()
        self.keywords = None
        self.posts = None

    def fetch(self):
        self.open_local()
        cur_keywords = self.__fetch__()
        cur_posts = []
        for keyword in tqdm(cur_keywords):
            try:
                post = self.__fetch_content__(keyword)
                cur_posts += post
            except Exception as e:
                print(f"{keyword.keyword}: {e}")

        keywords_rows = [c.get_row_data() for c in cur_keywords]
        keywords_columns = Keyword.get_column_name()
        posts_rows = [c.get_row_data() for c in cur_posts]
        posts_columns = Post.get_column_name()

        posts_df = DataFrame(posts_rows, columns=posts_columns)
        keywords_df = DataFrame(keywords_rows, columns=keywords_columns)
        if self.keywords is not None:
            self.keywords = pd.concat([self.keywords, keywords_df], ignore_index=True)
        else:
            self.keywords = keywords_df

        if self.posts is not None:
            self.posts = pd.concat([self.posts, posts_df], ignore_index=True)
        else:
            self.posts = posts_df
        return self

    @staticmethod
    def get_cur_time() -> datetime:
        local_tz = get_localzone()
        d = datetime.now()
        to_tz = pytz.timezone("Asia/Hong_Kong")
        local_now = local_tz.localize(d)
        now = local_now.astimezone(to_tz)
        return now

    def __fetch_content__(self, keyword: Keyword) -> [Post]:
        """
        Fetch contents based on keyword
        :arg
        """
        raise NotImplementedError

    def __fetch__(self) -> List[Keyword]:
        """
        Fetch keywords
        :arg
        """
        raise NotImplementedError

    def __get_output_name__(self):
        return f'{self.name}.csv', f'{self.name}-posts.csv'

    def open_local(self):
        """
        Download and load local csv-
        :arg
        """
        if os.path.exists(self.__get_output_name__()[0]):
            df = pd.read_csv(self.__get_output_name__()[0])
            self.keywords = df
        if os.path.exists(self.__get_output_name__()[1]):
            df = pd.read_csv(self.__get_output_name__()[1])
            self.posts = df
        return self

    def write_to_local(self):
        output: DataFrame
        if self.keywords is not None:
            self.keywords.to_csv(self.__get_output_name__()[0], index=False)
            self.posts.to_csv(self.__get_output_name__()[1], index=False)
        else:
            raise Exception("Data is None")

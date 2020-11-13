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
    keywords: List[Keyword]
    posts: List[Post]

    def __init__(self):
        # Output name
        self.name = "base"
        self.session = HTMLSession()
        self.keywords = []
        self.posts = []
        self.username = os.getenv('username')
        self.password = os.getenv('password')
        self.endpoint = os.getenv('endpoint')

    def fetch(self):
        cur_keywords = self.__fetch__()
        cur_posts = []
        for keyword in tqdm(cur_keywords):
            try:
                post = self.__fetch_content__(keyword)
                cur_posts += post

            except Exception as e:
                print(f"{keyword.keyword}: {e}")

        self.posts = cur_posts
        self.keywords = cur_keywords
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

    def upload_to_db(self):
        """
        Upload keywords and posts to db
        :return:
        """
        raise NotImplementedError

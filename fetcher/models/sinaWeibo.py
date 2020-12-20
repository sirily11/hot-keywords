"""
Author: Qiwei Li
"""

import time
from datetime import datetime
from typing import List
from fetcher.Post import Post
from fetcher.Keyword import Keyword
from fetcher.base import BaseFetcher
from psycopg2.extras import execute_values
import psycopg2
from tqdm import tqdm
import urllib.parse


class SinaWeibo(BaseFetcher):

    def upload_to_db(self):
        print("Uploading...")
        conn = psycopg2.connect(user=self.username,
                                password=self.password,
                                host=self.endpoint,
                                port='5432',
                                database="dataset")

        cursor = conn.cursor()
        for keyword in tqdm(self.keywords):
            sql = """
            insert into dataset_app_sinakeyword (time, keyword, numbers, rank) values (%s, %s, %s, %s) returning id;
            """
            cursor.execute(sql, keyword.get_row_data())
            keyword_id = cursor.fetchone()[0]
            related_posts = [[keyword_id, p.content] for p in self.posts if p.keyword == keyword.keyword]
            for post in related_posts:
                cursor.execute(
                    """insert into dataset_app_sinapost (keyword_id, content) values (%s, %s) """,
                    post)

            conn.commit()

    def __init__(self):
        super().__init__()
        self.name = 'SinaWeibo'

    def __fetch__(self) -> List[Keyword]:
        r = self.session.get('https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6')
        keywords = r.html.find('tr')
        keyword_text: List[Keyword] = []
        index = 0
        for i, keyword in enumerate(keywords):
            link = keyword.find('a', first=True)
            number = keyword.find('span', first=True)
            cur_time = self.get_cur_time()
            if link and number:
                keyword_text.append(Keyword(keyword=link.text, numbers=int(number.text), cur_time=cur_time, rank=index))
                index += 1

        return keyword_text

    def __fetch_content__(self, keyword: Keyword) -> List[Post]:
        url = f"https://s.weibo.com/weibo?q={keyword.keyword}"
        r = self.session.get(url)
        posts = []
        contents = r.html.find(".txt")
        for i, c in enumerate(contents):
            posts.append(Post(keyword=keyword.keyword, content=c.text))
        return posts


def main():
    sina = SinaWeibo()
    sina.fetch().upload_to_db()

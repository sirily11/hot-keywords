import time
from datetime import datetime
from typing import List
from fetcher.Post import Post
from fetcher.Keyword import Keyword
from fetcher.base import BaseFetcher
import urllib.request


class SinaWeibo(BaseFetcher):

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
        url = "https://s.weibo.com/weibo?q=%E8%A7%A3%E6%95%A3&Refer=top"
        r = self.session.get(url)
        posts = []
        contents = r.html.find(".txt")
        for i, c in enumerate(contents):
            if i > 10:
                break
            posts.append(Post(keyword=keyword.keyword, content=c.text))
        return posts


def main():
    sina = SinaWeibo()
    sina.open_local().fetch().write_to_local()

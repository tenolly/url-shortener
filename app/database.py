import string
from random import choices
from typing import List

from pymongo import MongoClient


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=Singleton):
    client = MongoClient("mongodb+srv://guest:guest@cluster0.fbnmfae.mongodb.net/?retryWrites=true&w=majority")
    collection = client.url_shortener.links
    
    def get_all_links(self) -> List[dict]:
        return list(self.collection.find())

    def link_exists(self, link: str) -> bool: 
        return bool(self.collection.find_one({"link": link}))

    def short_url_exists(self, url: str) -> bool:
        return bool(self.collection.find_one({"short_url": url}))

    def get_link(self, url: str) -> str:
        return self.collection.find_one({"short_url": url})["link"]

    def get_short_url(self, link: str) -> str:
        return self.collection.find_one({"link": link})["short_url"]

    def quantity_increment(self, url: str) -> None:
        self.collection.find_one_and_update({"short_url": url}, {"$inc": {"quantity": 1}})

    def create_short_url(self, link: str) -> str:
        short_url = "".join(choices(string.ascii_letters + string.digits, k=6))

        if self.short_url_exists(short_url):
            return self.create_short_url(link)

        self.collection.insert_one({
            "link": link,
            "short_url": short_url,
            "quantity": 0
        })

        return short_url

    def receive_short_url(self, link: str) -> str:
        if self.link_exists(link):
            return self.get_short_url(link)

        return self.create_short_url(link)

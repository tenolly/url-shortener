import string
from random import choices
from typing import List

from pymongo import MongoClient


client = MongoClient("mongodb+srv://Good5263:1234@cluster0.e79t8.mongodb.net/links?retryWrites=true&w=majority")
links = client.links.links

def get_all_links() -> List[dict]:
    return [link for link in links.find({})]


def link_exists(link: str) -> bool: 
    return bool(links.find_one({"link": link}))


def short_url_exists(url: str) -> bool:
    return bool(links.find_one({"short_url": url}))


def get_link(url: str) -> str:
    return links.find_one({"short_url": url})["link"]


def get_short_url(link: str) -> str:
    return links.find_one({"link": link})["short_url"]


def quantity_increment(url: str) -> None:
    updated_link = links.find_one({"short_url": url})
    links.update(updated_link, {"$set": {"quantity": updated_link["quantity"] + 1}})


def create_short_url(link: str) -> str:
    short_url = "".join(choices(string.ascii_letters + string.digits, k=6))

    if short_url_exists(short_url):
        return create_short_url(link)

    links.insert_one({
        "link": link,
        "short_url": short_url,
        "quantity": 0
    })

    return short_url


def receive_short_url(link: str) -> str:
    if link_exists(link):
        return get_short_url(link)

    return create_short_url(link)

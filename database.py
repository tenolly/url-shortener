from random import choices
from pymongo import MongoClient


client = MongoClient("mongodb+srv://Good5263:1234@cluster0.e79t8.mongodb.net/URLs?retryWrites=true&w=majority")
links = client.URLs.urls


def new_url_exists(url):
    return bool(links.find_one({"new_url": url}))


def link_exists(link): 
    return bool(links.find_one({"link": link}))


def get_new_url(link):
    return links.find_one({"link": link})["new_url"]


def get_link(url):
    return links.find_one({"new_url": url})["link"]


def create_new_url(link):
    new_url = "".join(choices("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890", k=6))
    if new_url_exists(new_url):
        return create_new_url(link)

    links.insert_one({
        "link": link,
        "new_url": new_url,
        "quantity": 0
    })

    return new_url


def receive_new_url(link):
    if link_exists(link):
        return get_new_url(link)
    else:
        return create_new_url(link)

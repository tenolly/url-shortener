import os
import sqlite3
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


def get_all_dicts():
    return [link for link in links.find({})]


def quantity_increment(url):
    updated_link = links.find_one({"new_url": url})
    links.update(updated_link, {"$set": {"quantity": updated_link["quantity"] + 1}})


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


def create_db_backup(folder_for_save="db_backups"):
    if len(os.listdir(folder_for_save)) > 0:
        count = max(map(lambda file: int(file.split("_")[1].split(".")[0]), os.listdir(folder_for_save)))
    else:
        count = -1

    connection = sqlite3.connect(f"{folder_for_save}/backup_" + str(count + 1) + ".sqlite")
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE links (_id TEXT, link TEXT, new_url TEXT, quantity INT)")
    connection.commit()

    for link in get_all_dicts():
        cursor.execute("INSERT INTO links VALUES(?, ?, ?, ?)", (str(link["_id"]), link["link"], link["new_url"], link["quantity"]))
        connection.commit()
    
    connection.close()
    
    if len(os.listdir(folder_for_save)) > 5:
        os.remove(os.path.join(folder_for_save, os.listdir(folder_for_save)[0]))

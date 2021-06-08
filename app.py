import re
from math import ceil

import waitress
from flask import Flask, render_template, abort, request, jsonify, redirect

from database import Database


app = Flask(__name__)
db = Database()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<url>")
def redirect_to_url(url):
    if not db.short_url_exists(url):
        return abort(404)

    db.quantity_increment(url)
    return redirect(db.get_link(url))


@app.route("/all_links/<int:page_number>")
def show_all_links(page_number=1):
    links_in_page = 20
    all_links = db.get_all_links()
    count_pages = ceil(len(all_links) / links_in_page)

    if count_pages < page_number:
        show_dicts = []
    elif count_pages == page_number:
        show_dicts = all_links[(page_number-1)*links_in_page:]
    else:
        show_dicts = all_links[(page_number-1)*links_in_page:page_number*links_in_page]

    return render_template("links.html", current_page_number=page_number, count_pages=count_pages, links=show_dicts)


@app.route("/new", methods=["POST"])
def get_new_link():
    response = {
        "success": True,
        "error": None,
        "link": "ok"
    }

    pattern = re.compile(r"((ftp|http|https):\/\/)?(www\.)?([A-Za-zА-Яа-я0-9]{1}[A-Za-zА-Яа-я0-9\-]*\.?)*\.{1}[A-Za-zА-Яа-я0-9-]{2,8}(\/([\w#!:.?+=&%@!\-\/])*)?")
    if not re.match(pattern, request.json["link"]):
        response["success"] = False
        response["error"] = "Provided link is not a URL"
    else:
        short_url = db.receive_short_url(request.json["link"])
        response["link"] = request.url_root + short_url

    return jsonify(response)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404


if __name__ == "__main__":
    waitress.serve(app)

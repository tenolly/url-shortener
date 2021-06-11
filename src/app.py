import re
import logging
from math import ceil

import waitress
from flask import Flask, render_template, abort, request, jsonify, redirect
from werkzeug.exceptions import HTTPException

from logger import Logger
from database import Database


logger = Logger()
logger.add_logger("debug", "logs/debug.log", logging.WARNING, "[%(asctime)s] %(levelname)s\n%(message)s")
logger.add_logger("requests", "logs/requests.log", logging.INFO)

app = Flask(__name__)
db = Database()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<url>")
def redirect_to_url(url):
    if not db.short_url_exists(url):
        return abort(404)
    
    logger.requests.info(f"[302] [Successfully redirected from /{url}]")

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
    response = {}

    pattern = re.compile(r"((ftp|http|https):\/\/)?(www\.)?([A-Za-zА-Яа-я0-9]{1}[A-Za-zА-Яа-я0-9\-]*\.?)*\.{1}[A-Za-zА-Яа-я0-9-]{2,8}(\/([\w#!:.?+=&%@!\-\/])*)?")
    response["success"] = bool(re.match(pattern, request.json["link"]))

    if response["success"]:
        short_url = db.receive_short_url(request.json["link"])
        response["link"] = request.url_root + short_url
        logger.requests.info(f"[200] [Received short url ({short_url}) for link ({request.json['link']})]")
    else:
        response["error"] = "Provided link is not a URL"

    return jsonify(response)


@app.errorhandler(Exception)
def handle_error(error):
    status_codes = {
        404: "Page not found",
        500: "Server dead inside"
    }

    code = 500
    if isinstance(error, HTTPException):
        logger.requests.info(f"[{error.code}] [{error.description}]")
        code = error.code
    else:
        logger.debug.exception(error)
    
    code_value = status_codes.get(code, "Unknown error")

    return render_template("error.html", code=code, value=code_value), code


if __name__ == "__main__":
    #waitress.serve(app)
    app.run()

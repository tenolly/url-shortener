import re
import logging
import logging.config
from math import ceil

import yaml
import waitress
from paste.translogger import TransLogger
from flask import Flask, render_template, abort, request, jsonify, redirect
from werkzeug.exceptions import HTTPException

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


@app.route("/links")
@app.route("/links/<int:page_number>")
def show_all_links(page_number=1):
    links_in_page = 15
    all_links = db.get_all_links()
    pages_count = ceil(len(all_links) / links_in_page)

    show_links = []
    start_link_index = (page_number - 1) * links_in_page

    if page_number == pages_count:
        show_links.extend(all_links[start_link_index:])
    elif page_number < pages_count:
        show_links.extend(all_links[start_link_index:start_link_index+links_in_page])

    return render_template("links.html", current_page_number=page_number, count_pages=pages_count, links=show_links)


@app.route("/new_link", methods=["POST"])
def get_new_link():
    response = {}

    pattern = re.compile(r"((ftp|http|https):\/\/)?(www\.)?([A-Za-zА-Яа-я0-9]{1}[A-Za-zА-Яа-я0-9\-]*\.?)*\.{1}[A-Za-zА-Яа-я0-9-]{2,8}(\/([\w#!:.?+=&%@!\-\/])*)?")
    response["success"] = bool(re.match(pattern, request.json["link"]))

    if response["success"]:
        short_url = db.receive_short_url(request.json["link"])
        response["link"] = request.url_root + short_url
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
        code = error.code
    else:
        logger = logging.getLogger("errors")
        logger.exception(error)
    
    code_value = status_codes.get(code, "Unknown error")

    return render_template("error.html", code=code, value=code_value), code


if __name__ == "__main__":
    logging.config.dictConfig(yaml.safe_load(open("logging.yaml")))
    waitress.serve(TransLogger(app, setup_console_handler=False))

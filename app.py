import re
import threading

import schedule
import waitress
from flask import Flask, render_template, abort, request, jsonify, redirect

import database


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def hello_world():
        return render_template("index.html")

    @app.route("/<url>")
    def redirect_to_url(url):
        if not database.new_url_exists(url):
            return abort(404)
        else:
            database.quantity_increment(url)
            return redirect(database.get_link(url))

    @app.route("/new", methods=['POST'])
    def get_link():
        json_ = request.get_json(force=True)
        response = {
            "success": True,
            "error": None,
            "link": "ok"
        }

        pattern = re.compile(
            r"((ftp|http|https):\/\/)?(www\.)?([A-Za-zА-Яа-я0-9]{1}[A-Za-zА-Яа-я0-9\-]*\.?)*\.{1}[A-Za-zА-Яа-я0-9-]{2,8}(\/([\w#!:.?+=&%@!\-\/])*)?")
        if not re.match(pattern, json_["link"]):
            response['success'] = False
            response["error"] = "Provided link is not a URL"
        else:
            new_url = database.receive_new_url(json_["link"])
            response["link"] = request.url_root + new_url

        return jsonify(response)
    
    @app.route("/all_links")
    def show_all_links():
        return render_template("links.html", links=database.get_all_dicts())

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("page_not_found.html"), 404

    return app


def start_creating_db_backups():
    def create_backups():
        schedule.every(3).days.do(database.create_db_backup)
        while True:
            schedule.run_pending()

    thread = threading.Thread(target=create_backups, daemon=True)
    thread.start()


if __name__ == "__main__":
    start_creating_db_backups()
    app = create_app()
    waitress.serve(app)

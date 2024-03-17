from bottle import Bottle

from htmx_tutorial_todo import db
from htmx_tutorial_todo.api import Api

storage = db.DatabaseTaskStorage("db.json")


if __name__ == "__main__":
    api = Api(Bottle(), storage)
    api.run(host="localhost", port=8080)
    api.shutdown()

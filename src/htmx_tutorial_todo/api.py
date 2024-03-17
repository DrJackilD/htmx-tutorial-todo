from pathlib import Path

from bottle import TEMPLATE_PATH, Bottle, request, response, template

from htmx_tutorial_todo import tasks

TEMPLATE_FOLDER = Path(__file__).parent.parent / "templates"


class Api:
    def __init__(self, app: Bottle, storage: tasks.Storage):
        self.app = app
        self.init_routes()

        self.storage = storage

    def init_routes(self):
        self.app.route("/", "GET")(self.index)
        self.app.route("/tasks", "POST")(self.add)
        self.app.route("/tasks/<task_id:int>", "DELETE")(self.delete_task)
        self.app.route("/tasks/<task_id:int>", "PUT")(self.set_task_status)
        TEMPLATE_PATH.append(TEMPLATE_FOLDER)

    def run(self, **kwargs):
        self.app.run(**kwargs)

    def shutdown(self):
        self.storage.shutdown()
        self.app.close()

    def index(self):
        """Return the index page with the list of tasks"""
        tsks = tasks.list_tasks(self.storage)
        completed, total = tasks.count_tasks(self.storage)
        return template("index", tasks=tsks, completed=completed, total=total)

    def add(self):
        """Add one task, and redirect to the index"""
        if title := request.forms.get("title"):
            task = tasks.set_task(self.storage, tasks.Task(title=title, done=False))
            response.set_header("HX-Trigger-After-Settle", "update-counter")
            return template("_task", task=task)
        return ""

    def set_task_status(self, task_id: int):
        """Update the status of one task and redirect to the template"""
        status = request.forms.get("task")
        tasks.update_task(self.storage, task_id, {"done": bool(status)})
        response.set_header("HX-Trigger-After-Settle", "update-counter")
        return template("_task", task=tasks.get_task(self.storage, task_id))

    def delete_task(self, task_id: int):
        """Delete one task and redirect to the template"""
        tasks.delete_task(self.storage, task_id)
        response.set_header("HX-Trigger-After-Settle", "update-counter")
        return ""

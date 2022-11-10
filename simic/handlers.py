import os
import json

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join

import tornado
from tornado.web import StaticFileHandler
# from .detreefy import Detreefy


class RouteHandler(APIHandler):
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code_list = []
        # self.detreefy = Detreefy()

    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        self.finish(json.dumps({"data": "This is /simic/sending it to FE!"}))
# using this function for now
    @tornado.web.authenticated
    def post(self):
        # input_data is a dictionary with a key "sanpshot"
        input_data = self.get_json_body()
        snap = "{}".format(input_data["snapshot"])
        tmp = snap.split("!@#$%")
        snap = tmp[0]
        fileCount = tmp[1]
        snapCount = tmp[2]

        if snapCount == 2:
            self.code_list.pop(0)

        self.code_list.append(snap)
        # self.detreefy.test_1()
        data = {"code": snap, "fileCount": fileCount, "snapCount": snapCount}
        self.finish(json.dumps(data))


def setup_handlers(web_app, url_path):
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]

    # Prepend the base_url so that it works in a JupyterHub setting
    route_pattern = url_path_join(base_url, url_path, "code")
    handlers = [(route_pattern, RouteHandler)]
    web_app.add_handlers(host_pattern, handlers)

    # Prepend the base_url so that it works in a JupyterHub setting
    doc_url = url_path_join(base_url, url_path, "public")
    doc_dir = os.getenv(
        "JLAB_SERVER_EXAMPLE_STATIC_DIR",
        os.path.join(os.path.dirname(__file__), "public"),
    )
    handlers = [("{}/(.*)".format(doc_url), StaticFileHandler, {"path": doc_dir})]
    web_app.add_handlers(".*$", handlers)
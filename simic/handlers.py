import os
import json
import shutil

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join

import tornado
from tornado.web import StaticFileHandler

#flush the cache at the beginning of the session
def clear_code_cache(file_list,dir_name):
    
    for filename in file_list:
        file_path = os.path.join(dir_name, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    # [contract] 2 code text files -> edit script
def execute_gumtree():
    # TO DO: add a command for gumtree
    return


class RouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        self.finish(json.dumps({"data": "This is /simic/sending it to FE!"}))
# using this function for now
    @tornado.web.authenticated
    def post(self):
        
        dir_name = './code_cache'
        
        
        # input_data is a dictionary with a key "sanpshot"
        input_data = self.get_json_body()
        snap = "{}".format(input_data["snapshot"])
        tmp = snap.split("!@#$%")
        snap = tmp[0]
        fileCount = tmp[1]
        snapCount = tmp[2]
        if snapCount == '1':
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
            os.mkdir(dir_name)
    
        file_list = None
        new_filename = 'code_cache/' + str(snapCount) + '.txt'
        
        with open(new_filename, "w") as f:
            f.write(snap)

        if int(fileCount) >= 3:
            file_list = os.listdir(dir_name)
            names = []
            for filename in file_list:
                names.append(int(filename.split('.')[0]))
            
            os.remove('code_cache/' + str(min(names)) + '.txt')
    
            
        data = {"code": file_list, 'fileCount': fileCount, 'snapCount': snapCount}
        execute_gumtree(dir_name+str(int(snapCount)-1)+'.txt',dir_name+snapCount+'.txt')
        
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



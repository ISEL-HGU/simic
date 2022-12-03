import os
import json
import shutil
import socket
import sys
import subprocess

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join

import tornado
from tornado.web import StaticFileHandler

def connect_to_pool(is_request: int, *args, **kwargs):
    host = "127.0.0.1"          # Get local machine name
    port = 64555                        # Change these according to your environment
    conn = socket.socket()                   # Create a socket object

    conn.connect((host, port))

    if is_request == 0:
        intosend = kwargs.get('change_vector', None)
    elif is_request == 1:
        intosend = 'GET'
    conn.sendall(bytes(intosend, 'utf-8'))

    data = conn.recv(10000)

    conn.close()                                    # Close the socket when done


    return data


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
def execute_gumtree(path1: str, path2: str):
    # TO DO: add a command for gumtree
    srcPath = os.getcwd()+path1
    dstPath = os.getcwd()+path2
    process = subprocess.Popen(['make','-C' ,os.path.dirname(__file__)+'/simic_subprocesses', 'es_run','src='+srcPath, 'dst='+dstPath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = [line for line in process.stdout]
    es = str(output[-1]).replace('b\'','').replace('\\n\'','')    
    if 'Leaving directory' in es:
        es = str(output[-2]).replace('b\'','').replace('\\n\'','')
    return es 


class RouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        data = connect_to_pool(1)
        print(data)
        self.finish(json.dumps({"code": data.decode('utf-8')}))

# using this function for now
    @tornado.web.authenticated
    def post(self):
        
        dir_name = './code_cache'

        # input_data is a dictionary with a key "sanpshot"
        input_data = self.get_json_body()
        snap = "{}".format(input_data["snapshot"])
        if snap == 'flush':
            clear_code_cache(os.listdir(dir_name),dir_name)
            return
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
        change_vector = None
        if int(fileCount) == 2 or int(fileCount) == 3:
            change_vector = execute_gumtree('/code_cache/'+str(int(snapCount)-1)+'.txt','/code_cache/'+snapCount+'.txt')
            if change_vector == 'null':
                data = {"code": 'error#1'}
            else:
                connect_to_pool(0, change_vector=change_vector+'!@#$%'+snap)

        
        data = {"code": change_vector}
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



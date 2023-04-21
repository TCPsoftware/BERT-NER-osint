import os
import sys
import json
import time
from os.path import join


def check_dir(dir_name):
    if os.path.exists(dir_name):
        print("已存在文件夹。")
        # exit(0)
    else:
        os.mkdir(dir_name)

def get_sub_dirs(path):
    dir_list2 = []
    if os.path.exists(path):
        #获取该目录下的所有文件或文件夹目录
        files = os.listdir(path)
        for file in files:
            #得到该文件下所有目录的路径
            m = os.path.join(path, file)
            #判断该路径下是否是文件夹
            if os.path.isdir(m):
                dir_list2.append(file)
        return dir_list2

def change_file_dir():
    # 切到py文件目录
    base_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    os.chdir(base_path)

def get_json(json_filename):
    # 检查json文件有没有
    if os.path.exists(json_filename):
        with open(json_filename, "r", encoding="utf8") as f:
            json_obj = json.load(f)
    else:
        print("json文件不存在：", json_filename)
        exit(0)
    return json_obj

def write_obj_to_json(obj, out_json_filename, indent=4, end=""):
    # 输出到文件
    with open(out_json_filename, "w", encoding="utf8") as f:
        json.dump(obj, f, indent=indent, ensure_ascii=False)
        f.write(end)

def append_obj_to_json(obj, out_json_filename, indent=4, end=""):
    # 添加到文件
    with open(out_json_filename, "a", encoding="utf8") as f:
        json.dump(obj, f, indent=indent, ensure_ascii=False)
        f.write(end)

os.system(" ")
ERROR_LOG = "none"
def log(*args):
    global ERROR_LOG
    # assert "ERROR_LOG" in locals().keys()
    assert "ERROR_LOG" != "none"
    text = ""
    for i in args:
        text += str(i)+" "
    print("\033[91m" + text + "\033[m")
    with open(ERROR_LOG, "a", encoding="utf8") as lo:
        lo.write(text + "\n")

def set_error_log_path(error_log_name):
    global ERROR_LOG
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    ERROR_LOG = join(os.path.dirname(os.path.realpath(sys.argv[0])), "error_log", error_log_name+"-"+timestamp+".log")
    return ERROR_LOG
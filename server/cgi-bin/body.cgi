#!/usr/bin/python
# coding=utf-8
"""Generate HTML parts."""
import os.path
import sys
import json
import traceback
import cgitb
cgitb.enable()

sys.path = ([sys.path[0]]
            + [os.path.join(os.path.dirname(__file__), "../../lib")]
            + sys.path[1:])
import dataprocessor as dp
import handler
from dataprocessor.exception import DataProcessorError
sys.path = [sys.path[0]] + sys.path[2:]


def projects(req):
    """Generate a part of HTML about Project List."""
    with open("cfg.json") as f:
        cfg = json.load(f)
    data_path = cfg["data_path"]

    res_data = {
        "keys": ["name", "comment", "tags", "path"]
        }

    tbl = []
    with dp.io.DataHandler(data_path, silent=True) as dh:
        node_list = dh.get()
        for node in node_list:
            if node["type"] != "project":
                continue
            if "tags" not in node:
                node["tags"] = []
            if "comment" not in node:
                node["comment"] = ""
            tbl.append({
                "path": node["path"],
                "name": node["name"],
                "tags": node["tags"],
                "comment": node["comment"],
                })

    def mycmp(x, y):
        return cmp(x["name"], y["name"])
    tbl.sort(mycmp)
    res_data["table"] = tbl

    res = handler.Response("json")
    res.set_body(json.dumps(res_data))
    print(res)


def widgets(req):
    """
    Generate some parts of HTML about widgets such as table and figure.

    Notes
    -----
    Generating figure part is not implemented yet.

    """
    path = req.get("path")
    table_type = req.get("table_type")

    with open("cfg.json") as f:
        cfg = json.load(f)
    data_path = cfg["data_path"]

    with dp.io.DataHandler(data_path, silent=True) as dh:
        node_list = dh.get()
        groups = [
            {'items': ['comment', 'tags'], 'name': 'node'},
            {'dict_path': ['configure']},
        ]
        tbl = dp.table.Table(path, node_list, table_type, groups)
        html_str = tbl.render()

    res = handler.Response("json")
    res.set_body(json.dumps([html_str, ]))
    print(res)


def switch():
    req = handler.Request()
    types = {"Projects": projects, "Widgets": widgets}
    t = req.get("type")
    if t not in types:
        raise DataProcessorError("'type' must be in the followings: "
                                 + (" ".join(types.keys())))
    types[t](req)


if __name__ == "__main__":
    try:
        switch()
    except KeyError as key:
        handler.operation_fail("Request must include '%s'" % key)
    except ValueError:
        handler.operation_fail("JSON is invalid")
    except DataProcessorError as e:
        handler.operation_fail(e.msg)
    except Exception:
        with open("error.log", 'a+') as f:
            f.write(traceback.format_exc())
        handler.operation_fail("unknown error")

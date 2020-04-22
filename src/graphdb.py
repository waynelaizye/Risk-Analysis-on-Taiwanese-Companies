# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 18:09:12 2020

@author: Wayne
"""

import client_gdb as client
import ast
import json

#Establish connection to the rest server

GRAPHDB_HOST = "http://34.69.133.92" # host ip
GRAPHDB_PORT = "8012" # port
grest_host = GRAPHDB_HOST + ":" + GRAPHDB_PORT
g = client.gc(host=grest_host) # initialize the graphdb obj
print(g.set_current_graph("ComputerIndustry"))

def get_competitor(comp_name):
    json_str = {
        "vertices": [{"id": comp_name, "label": "公司"}],
        "depth": 1,
        "edge_direction": "out"
    }
    request_body = {"param": json.dumps(json_str).replace('\\"', '"')}
    res = g.run_analytics(analytic_name="bfs", request_body=request_body)
    data = ast.literal_eval(res.decode("UTF-8"))
    products = [v for v in data['data']['vertices'] if v['id']!=comp_name]
    comp_list = set()
    for p in products:
        json_str = {
            "vertices": [{"id": p['id'], "label": p['label']}],
            "depth": 1,
            "edge_direction": "in"
        }
        request_body = {"param": json.dumps(json_str).replace('\\"', '"')}
        res = g.run_analytics(analytic_name="bfs", request_body=request_body)
        data = ast.literal_eval(res.decode("UTF-8"))
        for v in data['data']['vertices']:
            if v['label'] == '公司':
                comp_list.add(v['id'])
    return list(comp_list)

#json_str = {
#    "vertices": [{"id": "華碩", "label": "公司"}],
#    "depth": 1,
#    "edge_direction": "out"
#}
#
#request_body = dict()
#request_body["param"] = json.dumps(json_str).replace('\\"', '"')
#
#res = g.run_analytics(analytic_name="bfs", request_body=request_body)
#
##
##res = g.get_egonet(vertex_id="華碩", vertex_label="公司", depth = 1)
#data = ast.literal_eval(res.decode("UTF-8"))
#p = get_competitor(g, '華碩')




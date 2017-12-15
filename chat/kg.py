#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py2neo import Graph, Node, Relationship, NodeSelector

graph = Graph("http://localhost:7474/db/data", password="train")

def get_property_taste(format_string="%s的味道是%s", info=None):
    assert isinstance(info, str), "The info must be a string."
    data = graph.run("MATCH (n) WHERE n.name='" + info + "' RETURN n.taste as pr").data()
    try:
        pr = data[0]['pr']
    except:
        pr = "...不好意思还在学习中"
    answer = format_string % (str(info), str(pr))
    return answer

def get_dish_ingredients(format_string="%s的食材是:\n%s", info=None):
    assert isinstance(info, str), "The info must be a string."
    data = graph.run("MATCH (n:DISH)-[r:Ingredients]->(p:IG) WHERE n.name='" + info + "' RETURN r, p").data()
    try:
        ingredients = ''.join(["%s：%sg，" % (item['p']['name'], str(item['r']['w'])) for item in data])
    except:
        ingredients = "...不好意思还在学习中"
    answer = format_string % (str(info), str(ingredients))
    return answer
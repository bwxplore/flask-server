from flask import Flask
import os
from flask import Flask, render_template, request
from flask_restful import Resource, Api
from flask_cors import CORS
import math
from aco import *

app=Flask(__name__)

# init object flask restfull
api = Api(app)

# init cors
CORS(app)

def distance(city1: dict, city2: dict):
    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)

@app.route('/')
def gas():
    return 'mantap'

@app.route('/calculate', methods=["POST"])
def main():
    cities = []
    points = []

    value = request.form['value']
    
    _value = value.splitlines()
    
    for i in range(len(_value)):
      city = _value[i].split(' ')
      cities.append(dict(index=int(city[0]), x=float(city[1]), y=float(city[2])))
      points.append((float(city[1]), float(city[2])))

    cost_matrix = []
    rank = len(cities)
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(distance(cities[i], cities[j]))
        cost_matrix.append(row)
    aco = ACO(10, 100, 1.0, 10.0, 0.5, 10, 2)
    graph = Graph(cost_matrix, rank)
    print(graph.matrix)
    path, cost = aco.solve(graph)
    print('cost: {}, path: {}'.format(cost, path))
    for i in range (len(path)):
        path[i]+=1
    results = [cost*142,path]
    return results

if __name__=="__main__":
    app.run(host='0.0.0.0')
import logging
import json
from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/magiccauldrons', methods=['POST'])
def magiccauldrons():
    res = []
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    for i in data:
        part1 = i.get("part1")
        part2 = i.get("part2")
        part3 = i.get("part3")
        part4 = i.get("part4")
        res.append(process(part1,part2, part3, part4))
    # for i in input:
    #     p1 = i["part1"]
    #     p2 = i["part2"]
    #     p3 = i["part3"]
    #     p4 = i["part4"]
    #     res.append(process(p1,p2,p3,p4))
    print(res)
    return json.dumps(res)

def process(p1,p2,p3,p4):
    result = {}
    result["part1"] = round(float(p1["flow_rate"]*p1["time"]), 2)
    # result["part2"] = int((p2["amount_of_soup"]*2+1)/2//p2["flow_rate"])
    result["part2"] = int(p2["amount_of_soup"]/p2["flow_rate"]+0.5)
    result["part3"] = round(float(p3["flow_rate"]*p3["time"]), 2)
    result["part4"] = int(p4["amount_of_soup"]/p4["flow_rate"]+0.5)
    return result
input = [{
    "part1": {
      "flow_rate": 2.153,
      "time": 3,
      "row_number": 0,
      "col_number": 0
    },
    "part2": {
      "flow_rate": 10,
      "amount_of_soup": 10.00,
      "row_number": 0,
      "col_number": 0
    },
    "part3": {
      "flow_rate": 30,
      "time": 2,
      "row_number": 0,
      "col_number": 0
    },
    "part4": {
      "flow_rate": 50,
      "amount_of_soup": 100.00,
      "row_number": 0,
      "col_number": 0
    }
  },
  {
    "part1": {
      "flow_rate": 23,
      "time": 1,
      "row_number": 0,
      "col_number": 0
    },
    "part2": {
      "flow_rate": 17,
      "amount_of_soup": 34.00,
      "row_number": 0,
      "col_number": 0
    },
    "part3": {
      "flow_rate": 36,
      "time": 1,
      "row_number": 0,
      "col_number": 0
    },
    "part4": {
      "flow_rate": 5,
      "amount_of_soup": 20.00,
      "row_number": 0,
      "col_number": 0
    }
  }]


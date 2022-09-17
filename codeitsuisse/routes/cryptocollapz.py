import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/cryptocollapz', methods=['POST'])
def cryptocollapz():
    data = request.get_json()
    #得到一个list
    result=process(data[0])
    logging.info("data sent for evaluation {}".format(data))
    logging.info("My result :{}".format(result))
    l = []
    l.append(result)
    return json.dumps(l)


def process(data):

    dic = {}
    for i in range(len(data)):
        dic[i] = []
        dic[i].append(data[i])
    n = []
    for i in dic:
        n.append(cal(dic[i]))
    return n

def cal(list):
    p = list[0]
    m=list[0]
    if p%2==0:
        p //= 2
    else:
        p = p *3 +1
    while p not in list:
        list.append(p)
        if p%2==0:
            p //= 2
        else:
            p = p *3 +1
        m=max(list)
    return m

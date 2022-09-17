import logging
import json
from pprint import pp

from flask import request, jsonify,Response

from codeitsuisse import app

logger = logging.getLogger(__name__)
headers = {'Content-type': 'text/plain'}
@app.route('/travelling-suisse-robot', methods=['POST'] )
def travelling():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    prodata = data.split("\n")
    l = len(prodata)-1
    w = len(prodata[0])

    charList = [[] for i in range(26)]
    for m in range(l):
        for n in range(w):
            if prodata[m][n] != " ":
                print(prodata[m][n])
                charList[ord(prodata[m][n]) - 65].append([m, n])
    orig = charList[ord("X") - 65][0]
    goal = "CODEITSUISSE"
    ppath = []
    status = ["up"]

    for i in goal:
        pos_point = charList[ord(i) - 65]
        min = 0
        print(orig,"to",pos_point, i)
        # minsum = abs(pos_point[0][0] - orig[0]) + abs(pos_point[0][1] - orig[1])
        if len(pos_point)== 1:
            x_d = pos_point[0][0] - orig[0]
            y_d = pos_point[0][1] - orig[1]
            total_d = abs(x_d)+abs(y_d)
            min = total_d
            target = pos_point[0]
        else:
            min = 2*max(len(prodata),len(prodata[0]))
            for i in range(len(pos_point)):
                point = pos_point[i]
                x_ds = point[0] - orig[0]
                y_ds = point[1] - orig[1]
                total_ds = abs(x_ds)+abs(y_ds)
                if total_ds < min:
                    min = total_ds
                    target = pos_point[i]
            x_d = target[0]-orig[0]
            y_d = target[1]-orig[1]
        orig = list(target)
        if status[0]=="up":
            s = ""
            if x_d < 0:
                s+="S"*abs(x_d)
                if y_d > 0:
                    s+="R"+"S"*abs(y_d)
                    status.append("right")
                if y_d < 0:
                    s+="L"+"S"*abs(y_d)
                    status.append("left")
            if x_d > 0:
                if y_d > 0:
                    s+="R"+"S"*abs(y_d)
                    s+="R"+"S"*abs(x_d)
                if y_d < 0:
                    s+="L"+"S"*abs(y_d)
                    s+="L"+"S"*abs(x_d)
                status.append("down")
            else:
                if y_d > 0:
                    s+="R"+"S"*abs(y_d)
                    status.append("right")
                if y_d < 0:
                    s+="L"+"S"*abs(y_d)
                    status.append("left")
                ppath.append(s+"P")
        elif status[0]=="right":
            s = ""
            if y_d > 0:
                s+="S"*abs(y_d)
                if x_d > 0:
                    s+="R"+"S"*abs(x_d)
                    status.append("down")
                if x_d < 0:
                    s+="L"+"S"*abs(x_d)
                    status.append("up")
            if y_d < 0:
                if x_d > 0:
                    s+="R"+"S"*abs(x_d)
                    s+="R"+"S"*abs(y_d)
                if x_d < 0:
                    s+="L"+"S"*abs(x_d)
                    s+="L"+"S"*abs(y_d)
                status.append("left")
            else:
                if x_d > 0:
                    s+="R"+"S"*abs(x_d)
                    status.append("down")
                if x_d < 0:
                    s+="L"+"S"*abs(x_d)
                    status.append("up")
            ppath.append(s+"P")
        elif status[0]=="down":
            s = ""
            if x_d > 0:
                s+="S"*abs(x_d)
                if y_d > 0:
                    s+="L"+"S"*abs(y_d)
                    status.append("right")
                if y_d < 0:
                    s+="R"+"S"*abs(y_d)
                    status.append("left")
            if x_d < 0:
                if y_d > 0:
                    s+="L"+"S"*abs(y_d)
                    s+="L"+"S"*abs(x_d)
                if y_d < 0:
                    s+="R"+"S"*abs(y_d)
                    s+="R"+"S"*abs(x_d)
                status.append("up")
            else:
                if y_d > 0:
                    s+="L"+"S"*abs(y_d)
                    status.append("right")
                if y_d < 0:
                    s+="R"+"S"*abs(y_d)
                    status.append("left")
            ppath.append(s+"P")
        elif status[0]=="left":
            s = ""
            if y_d < 0:
                s+="S"*abs(y_d)
                if x_d < 0:
                    s+="R"+"S"*abs(x_d)
                    status.append("up")
                if x_d > 0:
                    s+="L"+"S"*abs(x_d)
                    status.append("down")
            if y_d > 0:
                if x_d < 0:
                    s+="R"+"S"*abs(x_d)
                    s+="R"+"S"*abs(y_d)
                if x_d > 0:
                    s+="L"+"S"*abs(x_d)
                    s+="L"+"S"*abs(y_d)
                status.append("right")
            else:
                if x_d < 0:
                    s+="R"+"S"*abs(x_d)
                    status.append("up")
                if x_d > 0:
                    s+="L"+"S"*abs(x_d)
                    status.append("down")
            ppath.append(s+"P")
        if len(status) == 2:
            del status[0]
        print(status)
        min = pos_point.index(target)
        del (pos_point[min])
    str1 = ""
    for i in ppath:
        str1 += i
    logging.info("My result :{}".format(str1))

    return json.dumps(str1)
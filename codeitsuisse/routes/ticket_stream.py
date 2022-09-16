import logging
import json

from flask import request, jsonify
from decimal import Decimal
from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route("/tickerStreamPart1", methods=["POST"])
def tickerStreamPart1():

    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    # a list of "timestamp,ticker,quantity,price"
    stream = data.get("stream")
    # ["timestamp","ticker","quantity","price"]
    stream_data = [_.split(",") for _ in stream]
    # create a dictionary of list, where each list contains dicts
    tickers = {}
    new_data = [[get_time(d[0]), d[1], int(d[2]), Decimal(d[-1])*int(d[-2])] for d in stream_data]
    new_data.sort(key=lambda x: x[0])
    for ticker in new_data:
        key = ticker[0]
        if key in tickers:
            check(ticker[1:], tickers[key])
            tickers[key].sort(key=lambda x: x[0])
        else:
            if len(tickers) == 0:
                tickers[key] = []
                tickers[key].append(ticker[1:])
            else:
                tickers[key] = []
                for li in tickers[previous][:]:
                    tickers[key].append(li[:])
                check(ticker[1:], tickers[key])
            previous = key
    output = []
    for key in tickers:
        time = ":".join(str(_).zfill(2) for _ in [key//60, key%60])
        list = [time]
        for item in tickers[key]:
            list += [str(_) for _ in item]
        output.append(",".join(list))
    return json.dumps(output)

def get_time(time):
    return int(time.split(":")[0])*60+int(time.split(":")[1])

def check(ticker, exist):
    # adding ticker to exist list
    for ele in exist:
        if ticker[0] == ele[0]:
            ele[1], ele[2] = ele[1]+ticker[1], ele[2]+ticker[2]
            return
    exist.append(ticker)

@app.route("/tickerStreamPart2", methods=["POST"])
def tickerStreamPart2():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    stream = data.get("stream")
    quantityBlock = data.get("quantityBlock")

    stream_data = [_.split(",") for _ in stream]
    t = stream_data[:]
    # create a dictionary of list, where each list contains dicts
    tickers = {}
    new_data = [[get_time(d[0]), d[1], int(d[2]), Decimal(d[-1])*int(d[-2])] for d in stream_data]
    new_data.sort(key=lambda x: x[0])
    tickers = {}
    t.sort(key=lambda x: x[0])
    output = []
    ans = []
    for ticker in new_data:
        key = ticker[0]
        out = [":".join(str(_).zfill(2) for _ in [key//60, key%60])]
        if key in tickers:
            check(ticker[1:], tickers[key], quantityBlock, out, ans)
            tickers[key].sort(key=lambda x: x[0])
        else:
            if len(tickers) == 0:
                tickers[key] = []
                tickers[key].append(ticker[1:])
            else:
                tickers[key] = []
                for li in tickers[previous][:]:
                    tickers[key].append(li[:])
                
                check(ticker[1:], tickers[key], quantityBlock, out, ans)                  
            previous = key
        if len(out) != 1:
            output.append(",".join([str(_) for _ in out]))
    return json.dumps(output)

def get_time(time):
    return int(time.split(":")[0])*60+int(time.split(":")[1])

def check(ticker, exist, quantityBlock, out, ans):
    # adding ticker to exist list
    for ele in exist:
        if ticker[0] == ele[0]:
            if ele[1]+ticker[1] >= quantityBlock and ticker[0] not in ans:
                p_t = ticker[2] / ticker[1]
                out += [ticker[0], quantityBlock, ele[2]+p_t*(quantityBlock-ele[1])]
                ans += ticker[0]
            ele[1], ele[2] = ele[1]+ticker[1], ele[2]+ticker[2]
            return
    if ticker[1] >= quantityBlock and ticker[0] not in ans:
        p_t = ticker[2] / ticker[1]
        out += [ticker[0], quantityBlock, quantityBlock*p_t]
        ans += [ticker[0]]
    exist.append(ticker)

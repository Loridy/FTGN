import logging
import json

from flask import request, jsonify
from datetime import datetime
from collections import OrderedDict
from multiprocessing import current_process
from tabnanny import check

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/calendarDays', methods=['POST'])
def calendar():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    stream = data.get("numbers")
    input = stream[:]
    res= {}
    year = input[0]
    date=[]
    months = {}
    for day in input[1:]:
        if year%4==0 and 367>day>0 and convert(year, day) not in date:
            date.append(convert(year, day))
        elif year%4!=0 and 366>day>0 and convert(year, day) not in date:
            date.append(convert(year, day))
    date.sort()
    print(date)
    for day in date:
        if day[1] in months:
            print(datetime(day[0], day[1], day[2]).weekday())
            if datetime(day[0], day[1], day[2]).weekday() not in months[day[1]]:
                months[day[1]].append(datetime(day[0], day[1], day[2]).weekday())
        else:
            months[day[1]] = []
            months[day[1]].append(datetime(day[0], day[1], day[2]).weekday())
        months[day[1]].sort()
    print(months,"months")
    part1 = []
    for month in range(1, 13):
        status = ""
        li = [' ', ' ', ' ', ' ', ' ', ' ', ' ']
        if month not in months:
            part1.append("       ")
        elif len(months[month]) == 7: 
            li = "alldays"
            part1.append(li)
        # elif all(ele in [0,1,2,3,4] for ele in months[month]):
        elif months[month].sort() == [0, 1, 2, 3, 4]:
            li = "weekday"
            part1.append(li)
        # elif all(ele in [5,6] for ele in months[month]):
        elif months[month].sort() == [5,6]:
            li = "weekend"
            part1.append(li)
        else:
            for day in months[month]:
                li[day] = check_date(day)
            part1.append("".join(li))
    print(part1)

    p1 = ",".join(part1)+","
    # res["part2"] = func(p1)
    p2 = p1[:-1].split(",")
    # e = enumerate(p2)
    # map(func, p1)
    # print(p1, list(map(func, )))
    # return jsonify(res)
    # "part2":func(p1)
    return json.dumps({"part1": p1, "part2":[]})

# def func(data):
#     # month, par1 = data
#     print(month)
#     print(par1)
#     part1 = par1
#     print(part1)
#     # return part2("".join(part1).find(" ")%7+2001, part1)
#     return "hello"

def convert(year, number):
    months = {}
    for month in range(1,13):
        if month in [1,3,5,7,8,10,12]:
            months[month] = 31
        elif month in [4,6,9,11]:
            months[month] = 30
        else:
            if year%4==0:
                months[2] = 29
            else:
                months[2] = 28
    current_month = 1
    while number > months[current_month]:
        number -= months[current_month]
        current_month += 1
    return [year, current_month, number]

# def part2(year, part1):
#     months = {}
#     print(part1)
#     print(len(part1),"1")
#     # for i in range(len(part1)):
#     #     print(i)
#     #     if part1[i] == "alldays":
#     #         months[i+1] = [0,1,2,3,4,5,6]
#     #     elif part1[i] == "weekday":
#     #         months[i+1] = [0]
#     #     elif part1[i] == "weekend":
#     #         print("hi")
#     #         months[i+1] = [5]
#     #     elif part1[i] != "       ":
#     #         for j in range(7):
#     #             months[i+1] = []
#     #             if part1[i][j] != " ":
#     #                 months[i+1].append([j])
#     if part1[i] == "alldays":
#         months[i+1] = [0,1,2,3,4,5,6]
#     elif part1[i] == "weekday":
#         months[i+1] = [0]
#     elif part1[i] == "weekend":
#         print("hi")
#         months[i+1] = [5]
#     elif part1[i] != "       ":
#         for j in range(7):
#             months[i+1] = []
#             if part1[i][j] != " ":
#                 months[i+1].append([j])
    
#     result = [year]
#     for month in months:
#         result += get_month(year, month, months[month])
#     return result

def check_date(day):
    if day==0: return 'm'
    if day==1: return 't'
    if day==2: return 'w'
    if day==3: return 't'
    if day==4: return 'f'
    if day==5: return 's'
    if day==6: return 's'

def get_month(year, month, day):
    list = []
    months = {}
    for mon in range(1,13):
        if mon in [1,3,5,7,8,10,12]:
            months[mon] = 31
        elif mon in [4,6,9,11]:
            months[mon] = 30
        else:
            if year%4==0:
                months[2] = 29
            else:
                months[2] = 28
    sum = 0
    m=1
    list = []
    while m<month:
        sum += months[m]
        m += 1
    for i in range(1,1+months[month]):
        if len(day) == 0:
            return list
        d = datetime(year, month, i).weekday()
        if d in day:
            sum += i
            day.remove(d)
            list.append(sum)


# input = [2022, -1, 0, 1, 2, 60, 38, 40, 39,71, 42, 41, 91, 334, 444, 999]
# print(sorted(input))
# calendar(input)
####creat json file####

import csv
import json
import numpy as np
import random
import datetime
from faker import Faker

# products with individual select probability
productid = range(1, 33)
weights = [15 / 281, 15 / 281, 15 / 281, 10 / 281, 10 / 281, 10 / 281, 10 / 281, 10 / 281, 5 / 281, 5 / 281, 5 / 281,
           5 / 281, 5 / 281, 10 / 281, 10 / 281, 10 / 281, 10 / 281, 10 / 281, 10 / 281, 10 / 281, 10 / 281, 10 / 281,
           10 / 281, 10 / 281, 10 / 281, 5 / 281, 10 / 281, 10 / 281, 5 / 281, 5 / 281, 1 / 281, 5 / 281]

# quantity purchased shown in csv
quantity = range(1, 11)
weights_q = [1000 / 1046, 15 / 1046, 9 / 1046, 6 / 1046, 3 / 1046, 3 / 1046, 3 / 1046, 3 / 1046, 3 / 1046, 1 / 1046]

# flat rate of shipping per bike
SHIPPING_COST = 30

# start date and end date
STARTDATE = "01/01/2005"
ENDDATE = "31/12/2020"
start = datetime.datetime.strptime(STARTDATE, '%d/%m/%Y')
end = datetime.datetime.strptime(ENDDATE, '%d/%m/%Y')

# function for generating usernames, input is the number of user to generate
def usermaker(num):
    fake = Faker()
    Faker.seed(10)
    count = 0
    users = []
    while count < num:
        users.append(fake.profile()["username"])
        count += 1
    return users

# function output is a list of normal distributed numbers
# mean and standard deviation of the normal distribution are first two inputs
# num is the length of the output list
# each element in the list is how many sale events a day will have
def eventsperday(mean, sd, num):
    eventlimit = [int(np.random.normal(mean, sd)) for i in range(num)]
    return eventlimit

# input list and a factor, output is elements in the list is multiplied by the factor
def multiplylist(mylist, factor):
    newlist = [i * factor for i in mylist]
    return newlist

# generate 8000 fake users
userlist = usermaker(8000)

# generate 100 random number of total sales event per day with mean of 5 and sd of 1
whilelimit = eventsperday(5, 1, 100)

# create dictionary (later will use this to make JSON file)
jsondict = {"all": 0}

historyid = {}
datelist = []
daycount = 0
rows = []

# created a list in the loop to include those already hovered
# those already hovered have 10% chance to come back and read
# using normal distribution to generate DURATION
# select productid based on the probability
while start <= end:
    temp1 = {}
    temp1["date"] = str(start.strftime("%d/%m/%Y"))
    temp1["events"] = []
    chosenlimit = random.choice(whilelimit)
    n2 = 0
    while n2 < chosenlimit:
        temp2 = {}
        csvrow = {}
        if len(historyid) == 0:
            id = random.choice(userlist)
            temp2["id"] = id
            temp2["hover"] = random.choices(productid, weights)[0]
            temp2["duration"] = int(np.random.normal(18.8, 3.9))
            historyid[id] = temp2["hover"]
        # if user already purchased, then "read" and delete the user's hover
        # history so he may hover next time
        # 10% chance to go back to read, then 56% chance make purchase
        else:
            if random.random() <= 0.1:
                read_id_and_product = random.choice(list(historyid.items()))
                temp2["id"] = read_id_and_product[0]
                temp2["read"] = read_id_and_product[1]
                temp2["duration"] = int(np.random.normal(367, 174))
                historyid.pop(temp2["id"])
                if random.random() <= 0.56:
                    csvrow["Id"] = temp2["id"]
                    csvrow["Product"] = temp2["read"]
                    csvrow["Quantity"] = random.choices(quantity, weights_q)[0]
                    csvrow["Date"] = temp1["date"]
                    csvrow["Shipping"] = SHIPPING_COST * csvrow["Quantity"]
                    rows.append(csvrow)
            else:
                id = random.choice(userlist)
                temp2["id"] = id
                temp2["hover"] = random.choices(productid, weights)[0]
                temp2["duration"] = int(np.random.normal(18.8, 3.9))
                historyid[id] = temp2["hover"]
        n2 += 1
        temp1["events"].append(temp2)
    datelist.append(temp1)
    step = datetime.timedelta(days=1)
    start += step
    daycount += 1
    # every year increase 5% customer base
    # when covid hits (from day 5590), sales increase 50% every month
    if daycount <= 5560 and daycount % 365 == 0:
        whilelimit = multiplylist(whilelimit, np.random.normal(1.05, 0.02))
    elif daycount >= 5560 and (daycount - 5560) % 30 == 0:
        whilelimit = multiplylist(whilelimit, np.random.normal(1.2, 0.02))
jsondict["all"] = datelist  # final dictionary ready to convert to json

# convert to json file
with open("web.json", "w", encoding="utf-8") as f:
    json.dump(jsondict, f, ensure_ascii=False, indent=4)

# CSV
fieldnames = ["Id", "Product", "Quantity", "Date", "Shipping"]
with open("Purchase.csv", "w", encoding="utf-8", newline="") as csvf:
    csvwriter = csv.DictWriter(csvf, fieldnames=fieldnames)
    csvwriter.writeheader()
    csvwriter.writerows(rows)

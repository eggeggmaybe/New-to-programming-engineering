from collections import defaultdict
import pandas as pd
import json
from bs4 import BeautifulSoup
import statistics

# open file
f = open("web.json", "r")
web_info = json.load(f)
f.close()

purchase_df = pd.read_csv("Purchase.csv")  # import purchase information

with open('index.html', encoding = 'utf-8') as f_bs:
    soup = BeautifulSoup(f_bs, "html.parser")

# Get price info
def get_all_price():
    all_price = soup.find_all('span', attrs={"class": "price"})
    price_list_temp = []  # Contains price for each product
    for price in all_price:
        price_with_sign = price.text
        num_price = ""
        for i in price_with_sign:
            if i.isnumeric() or i == '.':
                num_price += i
        price_list_temp.append(float(num_price))
    return price_list_temp


# Get description info in description_list
def get_all_description():
    all_descriptions = soup.find_all('span', attrs={"class": "info"})
    description_list_temp = []  # Contains description for each product
    description_len_lst_temp = []  # Contains length of description for each product
    for description in all_descriptions:
        description_txt = description.text
        description_list_temp.append(description_txt)
        description_len_lst_temp.append(len(description_txt.split()))
    return description_list_temp, description_len_lst_temp


# create a product price dictionary
def get_price_info(price_list_temp):
    price_info_dict = {}
    for n in range(len(price_list_temp)):
        price_info_dict[n + 1] = price_list_temp[n]
    return price_info_dict


def get_sale_info(purchase_df_temp, price_info_temp):
    sale_info_temp = {}  # create a dictionary containing quantity of sale, shipping cost and profit for each product
    for product_id in range(1, 33):
        quantity = 0
        shipping_cost = 0
        for number in range(len(purchase_df_temp['Product'])):
            if purchase_df_temp['Product'][number] == product_id:
                quantity += purchase_df_temp['Quantity'][number]
                shipping_cost += purchase_df_temp['Shipping'][number]
        profit = quantity * price_info_temp[product_id] - shipping_cost
        sale_info_temp[product_id] = [quantity, shipping_cost, profit]
    return sale_info_temp


price_list = get_all_price()
description_list, description_len_lst = get_all_description()
price_info = get_price_info(price_list)
sale_info = get_sale_info(purchase_df, price_info)

# q1
max_price = max(price_list)
item_list = []
for item in price_info.keys():
    if price_info[item] == max_price:
        item_list.append(item)
if len(item_list) == 1:
    print('{} {:.1f}'.format(item_list[0], max_price))
else:
    print('{} {:.1f}'.format(item_list, max_price))

# q2
print('{:.1f}'.format(statistics.mean(description_len_lst)))


# q3-4 the product that has the most hover/read time, giving the product id and the total number of seconds;
def get_hover_read_time():
    item_hover_dict_temp = defaultdict(int)
    item_read_dict_temp = defaultdict(int)
    data = web_info["all"]
    for item_temp in data:
        events_lst = item_temp["events"]
        for event in events_lst:
            if "hover" in event.keys():
                item_id_temp = event["hover"]
                hover_time = int(event["duration"])
                item_hover_dict_temp[item_id_temp] += hover_time
            elif "read" in event.keys():
                item_id_temp = event["read"]
                read_time = int(event["duration"])
                item_read_dict_temp[item_id_temp] += read_time
    return item_hover_dict_temp, item_read_dict_temp


item_hover_dict, item_read_dict = get_hover_read_time()
max_hover_time = max(item_hover_dict.values())  # maximum value
max_hover_item = [k for k, v in item_hover_dict.items() if v == max_hover_time]
if len(max_hover_item) == 1:
    print(max_hover_item[0], max_hover_time)
else:
    print(max_hover_item, max_hover_time)
max_read_time = max(item_read_dict.values())  # maximum value
max_read_item = [k for k, v in item_read_dict.items() if v == max_read_time]
if len(max_read_item) == 1:
    print(max_read_item[0], max_read_time)
else:
    print(max_read_item, max_read_time)

# q5-6
most_sale_quantity = 0
most_sc = 0
for product in sale_info.keys():
    if sale_info[product][0] > most_sale_quantity:
        most_sale_quantity = sale_info[product][0]
    if sale_info[product][1] > most_sc:
        most_sc = sale_info[product][1]

most_sale_products = []
most_sc_products = []
for item in sale_info.keys():
    if sale_info[item][0] == most_sale_quantity:
        most_sale_products.append(item)
    if sale_info[item][1] == most_sc:
        most_sc_products.append(item)

if len(most_sale_products) == 1:
    print('{} {}'.format(most_sale_products[0], most_sale_quantity))
else:
    print('{} {}'.format(most_sale_products, most_sale_quantity))

if len(most_sale_products) == 1:
    print('{} {}'.format(most_sc_products[0], most_sc))
else:
    print('{} {}'.format(most_sc_products, most_sc))


# q7-8
# initialise values for max and min profits
most_profit = 0
lowest_profit = sale_info[1][2]
for product in sale_info.keys():
    if sale_info[product][2] > most_profit:
        most_profit = sale_info[product][2]
    if sale_info[product][2] < lowest_profit:
        lowest_profit = sale_info[product][2]

# find corresponding item_id
most_profit_products = []
lowest_profit_products = []
for item in sale_info.keys():
    if sale_info[item][2] == most_profit:
        most_profit_products.append(item)
    if sale_info[item][2] == lowest_profit:
        lowest_profit_products.append(item)


if len(most_profit_products) == 1:
    print('{} {:.1f}'.format(most_profit_products[0], most_profit))
else:
    print('{} {:.1f}'.format(most_profit_products, most_profit))

if len(lowest_profit_products) == 1:
    print('{} {:.1f}'.format(lowest_profit_products[0], lowest_profit))
else:
    print('{} {:.1f}'.format(lowest_profit_products, lowest_profit))

# q9-10 the product with the lowest/highest hover-to-profit ratio, giving the product and ratio;
hover_profit_ratio_lst = {}
for item_id in range(1, 33):
    hover_profit_ratio_lst[item_id] = item_hover_dict[item_id] / sale_info[item_id][2]
max_hover_to_profit_ratio = max(hover_profit_ratio_lst.values())  # maximum value
max_hover_to_profit_item = [k for k, v in hover_profit_ratio_lst.items() if v == max_hover_to_profit_ratio]
min_hover_to_profit_ratio = min(hover_profit_ratio_lst.values())  # minimum value
min_hover_to_profit_item = [k for k, v in hover_profit_ratio_lst.items() if v == min_hover_to_profit_ratio]
if len(min_hover_to_profit_item) == 1:
    print(min_hover_to_profit_item[0], f"{min_hover_to_profit_ratio:.1f}")
else:
    print(min_hover_to_profit_item, f"{min_hover_to_profit_ratio:.1f}")
if len(max_hover_to_profit_item) == 1:
    print(max_hover_to_profit_item[0], f"{max_hover_to_profit_ratio:.1f}")
else:
    print(max_hover_to_profit_item, f"{max_hover_to_profit_ratio:.1f}")

# q11-12 the product with the highest/lowest read-to-profit ratio, giving the product and ratio;
read_profit_ratio_dict = {}
for item_id in range(1, 33):
    read_profit_ratio_dict[item_id] = item_read_dict[item_id] / sale_info[item_id][2]
max_read_to_profit_ratio = max(read_profit_ratio_dict.values())  # maximum value
max_read_to_profit_item = [k for k, v in read_profit_ratio_dict.items() if v == max_read_to_profit_ratio]
min_read_to_profit_ratio = min(read_profit_ratio_dict.values())  # minimum value
min_read_to_profit_item = [k for k, v in read_profit_ratio_dict.items() if v == min_read_to_profit_ratio]
if len(max_read_to_profit_item) == 1:
    print(max_read_to_profit_item[0], f"{max_read_to_profit_ratio:.1f}")
else:
    print(max_read_to_profit_item, f"{max_read_to_profit_ratio:.1f}")
if len(min_read_to_profit_item) == 1:
    print(min_read_to_profit_item[0], f"{min_read_to_profit_ratio:.1f}")
else:
    print(min_read_to_profit_item, f"{min_read_to_profit_ratio:.1f}")

# q13-14
info_profit_ratio_dict = {}
for item_id in range(1, 33):
    info_profit_ratio_dict[item_id] = description_len_lst[item_id - 1] / sale_info[item_id][2]
max_info_to_profit_ratio = max(info_profit_ratio_dict.values())  # maximum value
max_info_to_profit_item = [k for k, v in info_profit_ratio_dict.items() if v == max_info_to_profit_ratio]
min_info_to_profit_ratio = min(info_profit_ratio_dict.values())  # minimum value
min_info_to_profit_item = [k for k, v in info_profit_ratio_dict.items() if v == min_info_to_profit_ratio]
if len(max_info_to_profit_item) == 1:
    print(max_info_to_profit_item[0], f"{max_info_to_profit_ratio:.1f}")
else:
    print(max_info_to_profit_item, f"{max_info_to_profit_ratio:.1f}")
if len(min_info_to_profit_item) == 1:
    print(min_info_to_profit_item[0], f"{min_info_to_profit_ratio:.1f}")
else:
    print(min_info_to_profit_item, f"{min_info_to_profit_ratio:.1f}")

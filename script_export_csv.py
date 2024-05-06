import time

import pymongo
import csv

mongodb_uri = "mongodb+srv://longdosi2:19djAtqP7Loh0xoz@prd-market-insight-pl-0-lb.ssakj.mongodb.net/MIM?tls=true&tlsAllowInvalidHostnames=true&tlsAllowInvalidCertificates=true&maxIdleTimeMS=60000&retryWrites=true&w=majority&authSource=admin&authMechanism=SCRAM-SHA-1"
client = pymongo.MongoClient(mongodb_uri)
database = client.get_database("MIM2")

with open('data/datasets_sku_color_size.csv', 'a') as csvfile:
    fieldnames = ['name', 'code', 'color', 'size']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    #writer.writeheader()

    list_data = []
    count_index = 0

    for item in database["mapped_products"].find({"spider_name": "mustit.co.kr"}):
        if item["crawled_size"] in item['crawled_product_name'] and len(item["crawled_size"]) > 1 and " " in item["crawled_size"]:
            data_row = {
                'name': item['crawled_product_name'],
                'code': item['crawled_product_code'],
                'color': item['crawled_color'],
                'size': item['crawled_size']
            }
            print(item["crawled_size"] + " -- " + item['crawled_product_name'] + " ___ " + str(count_index))
            count_index += 1
            writer.writerows([
                data_row
            ])


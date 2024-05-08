import pymongo
import csv

mongodb_uri = "mongodb+srv://longdosi2:19djAtqP7Loh0xoz@prd-market-insight-pl-0-lb.ssakj.mongodb.net/MIM?tls=true&tlsAllowInvalidHostnames=true&tlsAllowInvalidCertificates=true&maxIdleTimeMS=60000&retryWrites=true&w=majority&authSource=admin&authMechanism=SCRAM-SHA-1"
client = pymongo.MongoClient(mongodb_uri)
database = client.get_database("MIM2")

with open('data/list_name.txt', 'r', encoding='utf8') as file:
    content = file.read()
    array_name = content.split("\n")

    list_product = database["mapped_products"].find({
        "crawled_product_name": {"$in": array_name},
        "spider_name": "mustit.co.kr"
    })

    array_name_to_url = {}
    for product in list_product:
        array_name_to_url[product["crawled_product_name"]] = product["crawled_product_url"]
        print(product["crawled_product_name"] + "___________" + product["crawled_product_url"])

    print(array_name_to_url)

    # list_data_row = []
    #
    # with open('data/datasets_sku_color_size_clone.csv', 'r') as csvfile:
    #     csv_reader = csv.reader(csvfile)
    #
    #     for row in csv_reader:
    #         list_data_row.append({
    #             'name': row[0] if row[0] != '""' else "",
    #             'code': row[1] if row[1] != '""' else "",
    #             'color': row[2] if row[2] != '""' else "",
    #             'size': row[3] if row[3] != '""' else ""
    #         })
    #
    # with open('data/datasets_sku_color_size_clone_with_link.csv', 'a') as csvfile:
    #     fieldnames = ['name', 'code', 'color', 'size', 'product_link']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writeheader()
    #
    #     for data_row in list_data_row:
    #         if data_row['name'] in array_name_to_url:
    #             data_row['product_link'] = array_name_to_url[data_row['name']]
    #         else:
    #             data_row['product_link'] = ""
    #
    #         writer.writerows([
    #             data_row
    #         ])

database.client.close()
print("DONE")

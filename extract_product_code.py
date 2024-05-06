import os
import re
from datetime import datetime
from bson import ObjectId
from pymongo import UpdateOne
import pymongo

crawled_brand_id = '662488b1fc2b3ff766b1e0e5'
minimum_code_length = 6
sub_code_length = 3
korean_pattern = re.compile(r'[가-힣]')
def remove_korean_chars(text):
    return korean_pattern.sub('', text)
if __name__ == "__main__":

    db_connection = None
    message_connector = None
    connection_string = "mongodb+srv://longdosi2:19djAtqP7Loh0xoz@prd-market-insight-pl-0-lb.ssakj.mongodb.net/MIM?tls=true&tlsAllowInvalidHostnames=true&tlsAllowInvalidCertificates=true&maxIdleTimeMS=60000&retryWrites=true&w=majority&authSource=admin&authMechanism=SCRAM-SHA-1",
    try:
        db_connection = pymongo.MongoClient(connection_string)
        crawled_product_coll = db_connection.database["products"]

        for product in crawled_product_coll.find(
                {'brand_id': ObjectId(crawled_brand_id), 'status': 'active'} if crawled_brand_id else {'status': 'active'}):
            name = remove_korean_chars(product['good_nm'])
            # not bool(re.match(r"^[a-zA-Z]+$", self.special_char_remover.convert(element)))
            name_spilt = name.split(' ')
            potential_product_code = []
            is_product_code_run_started = False
            for part in name_spilt:
                # remove special characters in this word
                no_special = "".join(e for e in str(part) if e.isalnum())
                if not bool(re.match(r"^[a-zA-Z]+$", no_special)):
                    if len(no_special) >= minimum_code_length:
                        is_product_code_run_started = True
                    # this word contains both a-z and digit or only digit
                    if is_product_code_run_started and len(no_special) >= sub_code_length:
                        potential_product_code.append(no_special)
            if potential_product_code:
                print(' '.join(potential_product_code), '<=', product['good_nm'])
            else:
                print('no product code found', product['good_nm'])


        db_connection.close()
    except Exception as error:
        print(error)
        if db_connection:
            db_connection.close()

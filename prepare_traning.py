import pandas as pd
import json
import re

results = []


def tokenize_text(text):
    # t = WhitespaceTokenSplitter()
    # for token, start, end in t("플루크 남여공용 맨투맨티셔츠 FMT3113-RED"):
    #     print(token, start, end)
    # """Tokenizes the input text into a list of tokens."""
    return re.findall(r'\w+(?:[_]\w+)*|\S', text)
def prepare_traning_sku_color():
    pre_data = pd.read_csv('data/datasets_sku_color_size_clone.csv').values
    #pre_data = pd.read_csv('data/test/sheet_test.csv').values

    data_filtered = []
    sku_pushed = {}
    for data in pre_data:
        name = str(data[0])
        color = str(data[2])
        size = str(data[3])
        sku = str(data[1])

        unknow_string = "Non-existent"

        if color in [unknow_string, "No Color"]:
            color = ""
        if size == unknow_string:
            size = ""
        if sku == unknow_string:
            sku = ""

        data_filtered.append({'name': name, 'color': color, 'sku': sku, 'size': size})
        # print(name,sku)
        # if sku and sku not in sku_pushed:
        #     sku_pushed[sku] = 1
        #     data_filtered.append({'name': name, 'colors': [color], 'sku': sku, 'size': [size]})
    # print(data_filtered)
    # pd.DataFrame(data_filtered).to_csv('data/data_training.csv', index=False)
    result = []

    for data in data_filtered:
        tokens = tokenize_text(data['name'])
        tmp = {
            "tokenized_text": tokens,
            "ner": [],
        }
        start_index_sku = None
        end_index_sku = None
        start_index_size = None
        end_index_size = None

        start_index_color = None
        end_index_color = None

        for index, token in enumerate(tokens):
            color = data["color"]

            if " " in color:
                index_color = 0

                for color_split in color.split(" "):
                    if token == color_split:
                        if start_index_color is None:
                            start_index_color = index

                        if index_color == len(color.split(" ")) - 1:
                            end_index_color = index

                    index_color += 1
            else:
                if token == color:
                    tmp['ner'].append([index, index, 'Color'])

            if " " in data['sku']:
                index_sku = 0

                for sku in data['sku'].split(" "):
                    if token == sku:
                        if start_index_sku is None:
                            start_index_sku = index

                        if index_sku == len(data['sku'].split(" ")) - 1:
                            end_index_sku = index
                    index_sku += 1
            else:
                if token == data['sku']:
                    tmp['ner'].append([index, index, 'SKU'])

            if " " in data['size']:
                index_size = 0

                for sku in data['size'].split(" "):
                    if token == sku:
                        if start_index_size is None:
                            start_index_size = index

                        if index_size == len(data['size'].split(" ")) - 1:
                            end_index_size = index
                    index_size += 1
            else:
                if token == data['size']:
                    tmp['ner'].append([index, index, 'SIZE'])

        if start_index_color is not None and end_index_color is not None:
            tmp['ner'].append([start_index_color, end_index_color, 'Color'])

        if start_index_sku is not None and end_index_sku is not None:
            tmp['ner'].append([start_index_sku, end_index_sku, 'SKU'])

        if start_index_size is not None and end_index_size is not None:
            tmp['ner'].append([start_index_size, end_index_size, 'SIZE'])

        if len(tmp['ner']):
            result.append(tmp)
            results.append(tmp)

    with open('data/training_sku_color_size.json', 'w', encoding='utf8') as f:
        json.dump(result, f, ensure_ascii=False)
# def prepare_traning_color():
#     pre_data = pd.read_csv('data/pre_data_color.csv').values
#
#     data_filtered = []
#     sku_pushed = {}
#     for data in pre_data:
#         colors = data[0].split('_')
#         name = data[1]
#         sku_tmp = name.split(' / ')
#         sku = ''
#         if len(sku_tmp) == 2:
#             sku = sku_tmp[1]
#         if sku and sku not in sku_pushed:
#             sku_pushed[sku] = 1
#             data_filtered.append({'name': name, 'colors': colors,'sku':sku})
#
#     # pd.DataFrame(data_filtered).to_csv('data/data_training.csv', index=False)
#     result = []
#     for data in data_filtered:
#         tokens = tokenize_text(data['name'])
#         tmp = {
#             "tokenized_text": tokens,
#             "ner": [],
#         }
#         for index, token in enumerate(tokens):
#             for color in data['colors']:
#                 if token == color:
#                     tmp['ner'].append([index, index, 'Color'])
#             if token == data['sku']:
#                 tmp['ner'].append([index, index, 'SKU'])
#         if len(tmp['ner']):
#             result.append(tmp)
#             results.append(tmp)
#
#     with open('data/training_color.json', 'w', encoding='utf8') as f:
#         json.dump(result, f, ensure_ascii=False)
# def prepare_traning_sku():
#     pre_data = pd.read_csv('data/MIM_musinsa_products.csv').values
#
#     data_filtered = []
#     sku_pushed = {}
#     remove_colors = [
#         '(GRAY)',
#         '(DARKGRAY)',
#         '(SKY)',
#         '(WHTIE)',
#         '(WHITE)',
#         '(BLACK)',
#         '(NAVY)',
#         '(BLUE)',
#         '-GRAY',
#         '(RED)',
#         '(GREEN)',
#         '(GRAY',
#         '(KHAKI)',
#         '(DARKKHAKI)',
#         '(MINT)',
#         # '(RED)',
#     ]
#     for data in pre_data:
#         arr = data[0].split(';')
#         name = arr[0]
#         color = arr[1]
#         sku = arr[2]
#         if color != 'Nonexistent':
#             continue
#
#         color = ''
#         for remove_color in remove_colors:
#             if remove_color in sku:
#                 sku = sku.replace(remove_color, '')
#                 color = remove_color.replace('(', '')
#                 color = color.replace(')', '')
#                 color = color.replace('-', '')
#         if sku in name and sku not in sku_pushed and ' ' not in sku:
#             sku_pushed[sku] = 1
#             data_filtered.append({'name': name, 'sku': sku, 'color': color})
#
#     pd.DataFrame(data_filtered).to_csv('data/data_training.csv', index=False)
#     result = []
#     for data in data_filtered:
#         tokens = tokenize_text(data['name'])
#         tmp = {
#             "tokenized_text": tokens,
#             "ner": [],
#         }
#         for index, token in enumerate(tokens):
#             if token == data['sku']:
#                 tmp['ner'].append([index, index, 'SKU'])
#             if token == data['color']:
#                 tmp['ner'].append([index, index, 'Color'])
#         if len(tmp['ner']):
#             result.append(tmp)
#             results.append(tmp)
#
#     with open('data/training_sku.json', 'w', encoding='utf8') as f:
#         json.dump(result, f, ensure_ascii=False)

# prepare_traning_sku()
# prepare_traning_color()
prepare_traning_sku_color()



# with open('data/training.json', 'w', encoding='utf8') as f:
#     json.dump(results, f, ensure_ascii=False)

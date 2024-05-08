import csv

with open('data/datasets_sku_color_size_link.csv', 'r') as csvfile:
    csv_reader = csv.reader(csvfile)

    for row in csv_reader:
        if len(row[1]) > 0 and row[1][0][:1] == "C":
            print(row[1])


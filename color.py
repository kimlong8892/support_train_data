with open('data/list_color.txt', 'r', encoding='utf8') as file:
    content = file.read()
    array_color = content.split("\n")
    array_color = set(array_color)
    array_color_real = []

    for color in array_color:
        if color != "Non-existent" and color != '""':
            array_color_real.append(color)

    for color in array_color_real:
        print(color)
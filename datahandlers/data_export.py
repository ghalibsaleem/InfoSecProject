

def save_file(root_location, list_data, name, initials):
    str_data = "Files,"
    count = 0
    for item in list_data:
        for inner in item:
            str_data += str(inner)+","
        str_data = str_data[:-1]
        str_data += "\n"
        if count < 54:
            str_data += list_data[0][count] + ","
            count += 1

    with open(root_location + "/output/" + initials + str(name) + ".xlsx", "w") as all_data_file:
        all_data_file.write(str_data)


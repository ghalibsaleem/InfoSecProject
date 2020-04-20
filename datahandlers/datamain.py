import os
import concurrent.futures as fut
import xlrd as pd
from models.user_info import UserInfo
from models.user_data import UserData
import pickle
from datetime import datetime
from helper.progress_bar import print_progress


data_path = ""

all_data = UserData()


def copy_data_to_obj(root_path):
    """
    This method is used to read data from excel then save it to obj file in file system and location in which the obj file is saved is "saved_obj" folder in project directory. In case obj files is already present in file system then it will read data from there instead of excel file.

    Note: excel file location should be "input" folder in project directory and This method uses parallelization to speedup the process.
    :param root_path: absolute path of project directory
    :return: No return value
    """

    global data_path
    global all_data
    data_path = root_path + "/input/"

    flag = True
    for i in range(54):
        temp_list_path = root_path + "/saved_obj/" + str(i) + ".obj"
        if not os.path.isfile(temp_list_path):
            flag = False

    if flag:
        print("Start: Object reading from file system")
        print_progress(0, 54, prefix='Obj read Progress:', suffix='Completed', bar_length=50)
        for i in range(54):
            temp_list_path = root_path + "/saved_obj/" + str(i) + ".obj"
            with open(temp_list_path, "rb") as all_data_file:
                all_data.all_user_data.append(pickle.load(all_data_file))
            print_progress(i+1, 54, prefix='Obj read Progress:', suffix='Completed', bar_length=50)
        print("End: Object reading from file system")

    file_list = os.listdir(data_path)
    if ".idea" in file_list:
        file_list.remove(".idea")
    all_data.file_list = file_list
    if len(all_data.all_user_data) == 54:
        print("Check: All 54 User is loaded properly ")
        # endpoint_date_print(all_data.all_user_data)
        return

    print("Start: Reading data from excel")
    with fut.ProcessPoolExecutor() as executor:
        results = executor.map(excel_operation, file_list)
        count = 0
        print_progress(count, 54, prefix='Excel read Progress:', suffix='Completed', bar_length=50)
        for res in results:
            if res is None or isinstance(res, str):
                all_data.all_user_data.append([])
            else:
                all_data.all_user_data.append(res)
            count += 1
            print_progress(count, 54, prefix='Excel read Progress:', suffix='Completed', bar_length=50)
            # print("Length of object: " + str(len(all_data.all_user_data)))

    # results = [executor.submit(excel_operation, file_item, data_path) for file_item in file_list]
    # for item in fut.as_completed(results):
    #     print(item.result() + " Completed")
    print("End: Reading data from excel")

    endpoint_date_print(all_data.all_user_data)

    print("Start: copy_data_to_obj")
    for i in range(len(all_data.all_user_data)):
        temp_list_path = root_path + "/saved_obj/" + str(i) + ".obj"
        with open(temp_list_path, "wb") as all_data_file:
            pickle.dump(all_data.all_user_data[i], all_data_file, pickle.HIGHEST_PROTOCOL)
    print("End: copy_data_to_obj")


def excel_operation(file_item):
    """
    This function is called for each excel file in parallel.
    :param file_item: File name
    :return: data of the excel file
    """
    global data_path

    excel_file = pd.open_workbook(data_path + file_item)
    excel_sheet = excel_file.sheet_by_index(0)

    data = [excel_sheet.row_values(i) for i in range(excel_sheet.nrows)]
    labels = data[0]
    data = data[1:]
    data.sort(key=lambda x: x[5])
    excel_file.release_resources()

    list_data = []
    monday_found = False
    # skip_flag = False
    special_flag = False
    no_rows = len(data)
    start_date = 0
    diff = datetime.fromtimestamp(data[no_rows - 1][5] / 1000) - datetime.fromtimestamp(data[0][5] / 1000)
    beginning = True
    if file_item == "ajdqnf.xlsx":
        special_flag = True

    for index in range(no_rows):
        if index != 0 and data[index][9] != 0:
            temp_info = UserInfo(data[index])
            if start_date != 0 and (temp_info.rfp.date() - start_date.date()).days >= 14:
                break

            if diff.days <= 14 and check_date_range(temp_info.rfp):
                list_data.append(temp_info)
            else:
                if beginning and temp_info.rfp.weekday() >= 5 or special_flag:
                    monday_found = True
                if diff.days >= 19 - temp_info.rfp.weekday():
                    if monday_found is False and temp_info.rfp.weekday() == 0:
                        monday_found = True
                    if check_date_range(temp_info.rfp) and monday_found:
                        if start_date == 0:
                            start_date = temp_info.rfp
                        list_data.append(temp_info)
                else:
                    if check_date_range(temp_info.rfp):
                        list_data.append(temp_info)
            if beginning:
                beginning = False

    if len(list_data) == 0:
        # print(file_item + " is empty")
        return file_item
    # print("Reading Done : " + file_item)
    return list_data


def check_date_range(obj_date):
    """
    This function is used to check if given date is in specified date interval for the project
    :param obj_date: date to check
    :return: True if it is in range else false
    """
    if obj_date.weekday() <= 4 and 8 <= obj_date.hour < 17:
        return True
    else:
        return False


def endpoint_date_print(obj_list):
    """
    prints  the first and last packet date of each user
    :param obj_list: data list of all user
    """
    count = 0
    print("****************************************************************************")
    for item in obj_list:
        length = len(item)
        count += 1
        if length > 0:
            print("User " + str(count) + " File: " + all_data.file_list[count - 1] + " -----> Start date : " + str(item[0].rfp) + " and End date : " + str(item[length - 1].rfp))
        else:
            print("User " + str(count) + " File: " + all_data.file_list[count - 1] + " is empty")

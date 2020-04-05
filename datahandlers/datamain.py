import os
import multiprocessing
import concurrent.futures as fut
import xlrd as pd
from models.user_info import UserInfo
from models.user_data import UserData
import pickle
from datetime import datetime


data_path = ""

all_data = UserData()


def copy_data_to_obj(root_path):
    global data_path
    global all_data
    data_path = root_path + "/input/"
    obj_path = root_path + "/saved_obj/all_data.obj"

    for i in range(54):
        temp_list_path = root_path + "/saved_obj/" + str(i) + ".obj"
        if os.path.isfile(temp_list_path):
            with open(temp_list_path, "rb") as all_data_file:
                all_data.all_user_data.append( pickle.load(all_data_file))

    if len(all_data.all_user_data) == 54:
        print("Reading object from file system Done")
        return

    file_list = os.listdir(data_path)

    with fut.ProcessPoolExecutor() as executor:
        args = ((file_item, data_path) for (file_item) in file_list)
        results = executor.map(excel_operation, file_list)

        for res in results:
            if res is None or isinstance(res, str):
                all_data.all_user_data.append([])
            else:
                all_data.all_user_data.append(res)
            # print("Length of object: " + str(len(all_data.all_user_data)))

    # results = [executor.submit(excel_operation, file_item, data_path) for file_item in file_list]
    # for item in fut.as_completed(results):
    #     print(item.result() + " Completed")

    endpoint_date_print(all_data.all_user_data)

    for i in range(len(all_data.all_user_data)):
        temp_list_path = root_path + "/saved_obj/" + str(i) + ".obj"
        with open(temp_list_path, "wb") as all_data_file:
            pickle.dump(all_data.all_user_data[i], all_data_file, pickle.HIGHEST_PROTOCOL)
    print("End: copy_data_to_db")


def excel_operation(file_item):
    global data_path

    excel_file = pd.open_workbook(data_path + file_item)
    excel_sheet = excel_file.sheet_by_index(0)
    list_data = []
    monday_found = False
    skip_flag = False
    no_rows = excel_sheet.nrows
    start_date = 0
    diff = datetime.fromtimestamp(excel_sheet.cell_value(no_rows - 1, 0)) - datetime.fromtimestamp(excel_sheet.cell_value(1, 0))

    for index in range(no_rows):
        if index != 0 and excel_sheet.cell_value(index, 9) != 0:
            temp_info = UserInfo(excel_sheet.row_values(index))
            if start_date != 0 and (temp_info.rfp - start_date).days >= 14:
                break

            if diff.days <= 14 and check_date_range(temp_info.rfp):
                list_data.append(temp_info)
            else:
                if index == 1 and temp_info.rfp.weekday() >= 5:
                    monday_found = True
                if diff.days >= 19 - temp_info.rfp.weekday():
                    if index == 1 and temp_info.rfp.weekday() == 0 and 8 <= temp_info.rfp.hour < 17 and monday_found is False:
                        skip_flag = True
                    if skip_flag and index > 1 and temp_info.rfp.weekday() > 0:
                        skip_flag = False
                    if not skip_flag:
                        if monday_found is False and temp_info.rfp.weekday() == 0:
                            monday_found = True
                        if check_date_range(temp_info.rfp) and monday_found:
                            if start_date == 0:
                                start_date = temp_info.rfp
                            list_data.append(temp_info)
                else:
                    if check_date_range(temp_info.rfp):
                        list_data.append(temp_info)

    excel_file.release_resources()
    if len(list_data) == 0:
        print(file_item + " is empty")
        return file_item
    # print("Reading Done : " + file_item)
    return list_data


def check_date_range(obj_date):
    if obj_date.weekday() <= 4 and 8 <= obj_date.hour < 17:
        return True
    else:
        return False


def endpoint_date_print(obj_list):
    count = 0
    print("****************************************************************************")
    for item in obj_list:
        length = len(item)
        count += 1
        if length > 0:
            print("User " + str(count) + " -----> Start date : " + str(item[0].rfp) + " and End date : " + str(item[length - 1].rfp))
        else:
            print("User " + str(count) + " is empty")

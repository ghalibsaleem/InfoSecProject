import os
from datahandlers.datamain import copy_data_to_obj
from helper.helper_operations import create_split

time_intervals = [[10, False], [227, False], [300, False]]  # In seconds


def main():
    copy_data_to_obj(os.curdir)
    print("-------------------------------------------------------------------------------------------------")
    for time_int in time_intervals:
        time_int[1] = create_split(time_int[0])
    print("************* End of the program **************")


if __name__ == '__main__':
    main()

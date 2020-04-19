import os
from datahandlers.datamain import copy_data_to_obj
from datahandlers.data_export import save_file
from helper.helper_operations import create_split, mark_anomaly
from helper.spearman_correlation import calculate_spearman
from helper.calc_funtions import z_functions, p_functions

time_intervals = [[10, False], [227, False], [300, False]]  # In seconds


def main():
    print("************* Start of the program **************")
    copy_data_to_obj(os.curdir)
    mark_anomaly()
    print("-------------------------------------------------------------------------------------------------")
    p_relation_list = []
    for time_int in time_intervals:
        time_int[1] = create_split(time_int[0])
        if time_int[1] is True:
            relation = calculate_spearman()
            z_array = z_functions(relation)
            p_array = p_functions(z_array)
            save_file(os.curdir, p_array, time_int[0])
            p_relation_list.append(p_array)
        print("Done processing for Interval : " + str(time_int[0]))
    print("************* End of the program **************")


if __name__ == '__main__':
    main()




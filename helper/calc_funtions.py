import math
from datahandlers.datamain import all_data


def z_functions(relation):
    z_array = []
    for outer_index in range(54):
        if outer_index in all_data.anomaly_list:
            z_array.append([])
            continue
        relation_line = relation[outer_index]
        z_array_item = []
        for inner_index in range(54):
            if inner_index in all_data.anomaly_list or relation_line is None or relation_line[inner_index] is None:
                z_array_item.append(None)
                continue
            if inner_index != outer_index:
                rm_sq = math.pow(relation_line[outer_index], 2) + math.pow((relation_line[inner_index])[0], 2)
                rm_sq /= 2

                f_value = 1 - (relation_line[inner_index])[1]
                f_value /= 2 * (1 - rm_sq)

                h_value = 1 - (f_value * rm_sq)
                h_value /= 1 - rm_sq

                z_1a_2a = (math.log10((1 + relation_line[outer_index])/(1 - relation_line[outer_index]))) / 2
                z_1a_2b = (math.log10((1 + (relation_line[inner_index])[0]) / (1 - (relation_line[inner_index])[0]))) / 2

                z_final = z_1a_2a - z_1a_2b
                z_final *= math.sqrt(all_data.list_split_data[outer_index].total_windows_count - 3)
                if (relation_line[inner_index])[1] == 1:
                    (relation_line[inner_index])[1] = 0.99
                z_final /= 2 * h_value * (1 - (relation_line[inner_index])[1])
                z_array_item.append(z_final)
            else:
                z_array_item.append(0)
        z_array.append(z_array_item)
    return z_array


def p_functions(z_array):
    p_array = [all_data.file_list]
    p = 0.3275911
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429

    for outer_index in range(54):
        z_line = z_array[outer_index]
        p_array_item = []
        if outer_index in all_data.anomaly_list:
            p_array.append([])
            continue
        for inner_index in range(54):
            if inner_index in all_data.anomaly_list or z_line is None or z_line[inner_index] is None:
                p_array_item.append(None)
                continue
            if inner_index != outer_index:
                sign = None
                if z_line[inner_index] < 0:
                    sign = -1
                else:
                    sign = 1
                x = math.fabs(z_line[inner_index]) / math.sqrt(2)
                t = 1 / (1 + p * x)
                erf = 1 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
                rslt = 0.5 * (1 + sign * erf)
                p_array_item.append(rslt)
            else:
                p_array_item.append(0)
        p_array.append(p_array_item)
    return p_array


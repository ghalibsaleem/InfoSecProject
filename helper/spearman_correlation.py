from datahandlers.datamain import all_data
from scipy.stats import spearmanr


def calculate_spearman():
    relation = []
    for outer_index in range(54):
        if outer_index in all_data.anomaly_list:
            relation.append([])
            continue
        list_item = []

        user1_week1 = [x.sp_ratio for x in all_data.list_split_data[outer_index].list_week1]
        user1_week2 = [x.sp_ratio for x in all_data.list_split_data[outer_index].list_week2]
        if all_data.list_split_data[outer_index].week2_count == 0:
            relation.append(None)
            continue
        for inner_index in range(54):
            if inner_index in all_data.anomaly_list:
                list_item.append(None)
                continue
            # print("(" + str(outer_index) + ", " + str(inner_index) + ")")
            if outer_index == inner_index:
                if all_data.list_split_data[outer_index].week2_count == 0:
                    list_item.append(None)
                    continue
                result_same = spearmanr(user1_week1, user1_week2)
                list_item.append([result_same.correlation.__float__(), 1])
            else:
                user2_week2 = [x.sp_ratio for x in all_data.list_split_data[inner_index].list_week2]
                if all_data.list_split_data[inner_index].week2_count == 0:
                    list_item.append(None)
                    continue
                resl1 = spearmanr(user1_week1, user2_week2)
                resl2 = spearmanr(user1_week2, user2_week2)
                list_item.append([resl1.correlation.__float__(), resl2.correlation.__float__()])
        relation.append(list_item)

    # all_data.list_split_data.clear()

    return relation

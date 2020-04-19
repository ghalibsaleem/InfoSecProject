from datahandlers.datamain import all_data
import concurrent.futures as futr
from models.split_data import SplitData
from datetime import timedelta
from helper.progress_bar import print_progress


def create_split(time_interval):
    """
    This perform the split operation according to the time interval for all User.

    Note: This method utilises the multi core parallelization
    :param time_interval: window time
    :return:
    """
    # temp = handle_user_split([0, time_interval])
    all_data.list_split_data.clear()
    with futr.ProcessPoolExecutor() as executor:
        args = [(item, time_interval) for item in range(54)]
        results = executor.map(handle_user_split, args)
        count = 0
        print("Start: Splitting")
        print_progress(0, 54, prefix='Obj read Progress:', suffix='Completed', bar_length=50)
        for result in results:
            # print(count)
            count += 1
            all_data.list_split_data.append(result)
            print_progress(count, 54, prefix='Splitting Progress:', suffix='Completed', bar_length=50)
        print("End: Splitting")

    print("End of Create Split for time interval " + str(time_interval))
    if len(all_data.list_split_data) > 0:
        all_data.is_splitted = True
        return True
    return False


def handle_user_split(args):
    """
    This perform split for individual User
    :param args: Object which contain user index and window time
    :return: splited data
    """
    index = args[0]
    interval = args[1]
    if len(all_data.all_user_data[index]) == 0:
        return SplitData(interval)
    start_day = (all_data.all_user_data[index])[0].rfp
    start_day = start_day.replace(hour=8, minute=0, second=0, microsecond=0)

    prev_datetime = None
    split_data = SplitData(interval)
    split_data.week_start = (all_data.all_user_data[index])[0].rfp.weekday()
    flow_index = 0
    for i in range(2):
        if i == 0:
            list_to_work = split_data.list_week1
        else:
            list_to_work = split_data.list_week2
            prev_datetime = start_day + timedelta(days=7)

        for item in list_to_work:
            # item = SplitItem()
            if prev_datetime is None:
                item.sp_time = (all_data.all_user_data[index])[0].rfp
                item.sp_time = item.sp_time.replace(hour=8, minute=0, second=0, microsecond=0)
            else:
                temp_time = prev_datetime + timedelta(seconds=interval)
                if temp_time.hour >= 17:
                    item.sp_time = prev_datetime + timedelta(days=1)
                    item.sp_time = item.sp_time.replace(hour=8, minute=0, second=0, microsecond=0)
                else:
                    item.sp_time = temp_time
                if temp_time.weekday() >= 5:
                    item.sp_time = temp_time + timedelta(days=2)

            end_date = item.sp_time + timedelta(seconds=interval)

            # sub_list = list(filter(lambda x: item.sp_time <= x.rfp < end_date, all_data.all_user_data[index]))

            sub_list = []
            if flow_index < len(all_data.all_user_data[index]):
                while True:
                    if flow_index >= len(all_data.all_user_data[index]):
                        break
                    if item.sp_time <= all_data.all_user_data[index][flow_index].rfp < end_date:
                        sub_list.append(all_data.all_user_data[index][flow_index])
                        flow_index += 1
                    elif all_data.all_user_data[index][flow_index].rfp >= end_date:
                        break
                    else:
                        flow_index += 1

            duration = 0
            octate = 0
            ratio = 0

            if len(sub_list) > 0:
                if i == 0:
                    split_data.week1_count += 1
                else:
                    split_data.week2_count += 1
                for flow_item in sub_list:
                    """if flow_item.rfp + timedelta(seconds=flow_item.duration) > end_date:
                        extra_dur = end_date.timestamp() - flow_item.rfp.timestamp()
                        duration += extra_dur
                        octate += flow_item.doctate * extra_dur / flow_item.duration
                    else:
                        duration += flow_item.duration
                        octate += flow_item.doctate"""
                    ratio += flow_item.oct_duration
                """if duration != 0:
                    item.sp_ratio = octate / duration"""
                item.sp_ratio = ratio / len(sub_list)
            prev_datetime = item.sp_time
            sub_list.clear()
        """if i == 0:
            split_data.list_week1 = list_to_work
        else:
            split_data.list_week2 = list_to_work"""
        prev_datetime = start_day + timedelta(days=7)

    return split_data


def mark_anomaly():
    for item in range(54):
        if len(all_data.all_user_data[item]) == 0:
            all_data.anomaly_list.append(item)

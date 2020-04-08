from datahandlers.datamain import all_data
import concurrent.futures as futr
from models.split_data import SplitData
from models.split_item import SplitItem
from datetime import timedelta
import multiprocessing


def create_split(time_interval):
    # temp = handle_user_split([0,time_interval])

    with futr.ProcessPoolExecutor() as executor:
        args = [(item, time_interval) for item in range(54)]
        results = executor.map(handle_user_split, args)
        for result in results:
            all_data.list_split_data.append(result)

    print("End of Create Split for time interval " + str(time_interval))
    if len(all_data.list_split_data) > 0:
        all_data.is_splitted = True
        return True
    return False


def handle_user_split(args):
    index = args[0]
    interval = args[1]
    if len(all_data.all_user_data[index]) == 0:
        return SplitData()
    start_weekday = (all_data.all_user_data[index])[0].rfp.weekday()
    start_day = (all_data.all_user_data[index])[0].rfp.day
    week_count = 0
    interval_wall = (all_data.all_user_data[index])[0].rfp
    interval_wall += timedelta(seconds=interval)
    octate = 0
    duration = 0
    div_duration = 0
    prev_datetime = None
    split_data = SplitData()
    sp_item = SplitItem()

    for item in all_data.all_user_data[index]:
        if item.rfp.day != start_day and item.rfp.weekday() == start_weekday:
            start_day = item.rfp.day
            week_count += 1
        if week_count >= 2:
            break
        if sp_item.sp_time == 0:
            sp_item.sp_time = item.rfp
        if item.rfp > interval_wall and prev_datetime is None:
            print("More")
        if prev_datetime is not None:

            temp_delta = item.rfp.timestamp() - prev_datetime.timestamp()

            if interval > duration + temp_delta:
                octate += item.doctate
                duration += temp_delta
                div_duration += item.duration
            else:
                extra_dur = item.rfp.timestamp() - interval_wall.timestamp()
                div_duration += item.duration
                octate += item.doctate * (temp_delta - extra_dur) / temp_delta

                if duration != 0:
                    sp_item.sp_ratio = octate / div_duration
                    duration = 0
                    if week_count == 0:
                        split_data.list_week1.append(sp_item)
                    if week_count == 1:
                        split_data.list_week2.append(sp_item)
                    if week_count == 2:
                        split_data.list_week_extra.append(sp_item)

                octate = 0
                div_duration = 0
                duration = 0
                prev_datetime = None
                sp_item = SplitItem()
                sp_item.sp_time = item.rfp
                # interval_wall = item.rfp
                interval_wall += timedelta(seconds=interval)

        prev_datetime = item.rfp

    # all_data.list_split_data[index] = split_data
    return split_data

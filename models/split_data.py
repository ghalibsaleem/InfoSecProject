from models.split_item import SplitItem


class SplitData:
    def __init__(self, interval):
        no = 0
        if interval == 10:
            no = 6 * 60 * 9 * 5
        if interval == 227:
            no = 714
        if interval == 300:
            no = 540
        self.list_week1 = [SplitItem() for i in range(no)]
        self.list_week2 = [SplitItem() for i in range(no)]
        self.total_windows_count = no
        self.week1_count = 0
        self.week2_count = 0
        self.week_start = None

    list_week1 = []
    list_week2 = []

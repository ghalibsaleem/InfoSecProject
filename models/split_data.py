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
        self.list_week1 = [SplitItem()] * no
        self.list_week2 = [SplitItem()] * no
        self.list_week_extra = [SplitItem()] * no
        self.week_start = None

    list_week1 = []
    list_week2 = []
    list_week_extra = []

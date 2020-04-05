import os
from datahandlers.datamain import copy_data_to_obj, all_data


def main():
    copy_data_to_obj(os.curdir)
    print("")


if __name__ == '__main__':
    main()

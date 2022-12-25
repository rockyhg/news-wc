from datetime import date as dt
import os
import re

NEWS_DIR = os.path.join(os.path.dirname(__file__), "news")


def get_date_list() -> list:
    dir_list = os.listdir(NEWS_DIR)
    date_pattern = re.compile(r"^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$")
    for dir in dir_list:
        if date_pattern.fullmatch(dir) is None:
            dir_list.remove(dir)
        if dir == dt.today().strftime("%Y-%m-%d"):
            dir_list.remove(dir)
    dir_list = sorted(dir_list, reverse=True)
    return dir_list


if __name__ == "__main__":
    date_list = get_date_list()
    print(date_list)
    for i, date in enumerate(date_list, 1):
        print(f'<option value="{i}">{date}</option>')

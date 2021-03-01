from similarity.Jaro_git import JaroWinkler
import xlrd
import re
from pprint import pprint


def get_excel():
    xls = xlrd.open_workbook_xls("data.xls", encoding_override="utf-8")
    sheet = xls.sheet_by_index(0)
    job_name_list = (sheet.col_values(0, start_rowx=1))
    job_real_name_list = []
    for job_name in job_name_list:
        name = re.sub("（.*?）", "", str(job_name))
        name = re.sub("\(.*?\)", "", name)
        name = re.sub("\(.*?）", "", name)
        name = re.sub("（.*?\)", "", name)
        job_real_name_list.append(name)
    return job_real_name_list


def create_dict(name_list: list):
    jaro_threshold = 0.6
    jaro = JaroWinkler(0)
    job_name_dict = {}
    for name in name_list:
        if len(job_name_dict.keys()) > 0:
            for key in list(job_name_dict.keys()):
                # 相似性判断
                if jaro.similarity(name, key) > jaro_threshold:
                    value = job_name_dict.get(key)
                    insert_name = name if len(name) < len(key) else key
                    job_name_dict.pop(key)
                    job_name_dict[insert_name] = value + 1
                elif key == list(job_name_dict.keys())[-1]:
                    job_name_dict[name] = 1
        else:
            job_name_dict[name] = 1
    pprint(job_name_dict)


if __name__ == '__main__':
    job_name_list = get_excel()
    create_dict(job_name_list)

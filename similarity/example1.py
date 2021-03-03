from similarity.Jaro_git import JaroWinkler
import xlrd
import re
from pprint import pprint


def get_excel():
    xls = xlrd.open_workbook_xls("data.xls", encoding_override="utf-8")
    sheet = xls.sheet_by_index(3)
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
                    job_name_dict[name] = [].append()
        else:
            job_name_dict[name] = 1
    return job_name_dict


def reload():
    global job_name_dict
    job_new_dic = {}
    for key in list(job_name_dict.keys()):
        if len(job_new_dic.keys()) < 1:
            job_new_dic[key] = job_name_dict.get(key)
        else:
            for ele in list(job_new_dic.keys()):
                if jaro.similarity(ele, key) > 0.65:
                    real_name = ele if len(ele) < len(key) else key
                    value = job_new_dic.get(ele)
                    job_new_dic.pop(ele)
                    job_new_dic[real_name] = job_name_dict.get(key) + value
                else:
                    job_new_dic[key] = job_name_dict.get(key)
    job_name_dict = job_new_dic


if __name__ == '__main__':
    jaro = JaroWinkler(0)
    job_name_list = get_excel()
    job_name_dict = create_dict(job_name_list)
    reload()

    sorted_dict = {k: v for k, v in sorted(job_name_dict.items(), key=lambda item: item[1], reverse=True)}
    print(sorted_dict)
    for i in range(len(sorted_dict.keys())):
        if i < 10:
            print(list(sorted_dict.keys())[i], sorted_dict.get(list(sorted_dict.keys())[i]))
        else:
            break

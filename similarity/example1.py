from collections import OrderedDict

from similarity.Jaro_DaiHei import JaroDaiHei
import xlrd
import re


def get_excel():
    xls = xlrd.open_workbook_xls("./../process/process.xls", encoding_override="utf-8")
    sheet = xls.sheet_by_name("original职位")
    job_name_list = sheet.col_values(0, start_rowx=1)
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
    jaro = JaroDaiHei(0)
    job_name_dict = {}
    for name in name_list:
        if len(job_name_dict.keys()) > 0:
            temp_max_similarity = 0
            temp_key = ""
            is_ok = False
            for key in list(job_name_dict.keys()):
                # 相似性判断
                similarity = jaro.similarity(name, key)
                if similarity > jaro_threshold and similarity > temp_max_similarity:
                    temp_max_similarity = similarity
                    temp_key = checkAndMerge(name, key)
                    is_ok = True
                elif key == list(job_name_dict.keys())[-1] and temp_max_similarity == 0:
                    job_name_dict[name] = 1
                    is_ok = False
            if is_ok:
                value = job_name_dict.get(temp_key)
                insert_name = name if len(name) < len(temp_key) else temp_key
                job_name_dict.pop(temp_key)
                job_name_dict[insert_name] = value + 1

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
            temp_max_similarity = 0
            temp_key = ""
            is_ok = False
            for ele in list(job_new_dic.keys()):
                similarity = jaro.similarity(ele, key)
                if similarity > 0.65 and similarity > temp_max_similarity:
                    temp_key = ele
                    temp_max_similarity = similarity
                    is_ok = True
                elif ele == list(job_new_dic.keys())[-1] and temp_max_similarity == 0:
                    job_new_dic[key] = job_name_dict.get(key)
                    is_ok = False
            if is_ok:
                real_name = temp_key if len(temp_key) < len(key) else key
                value = job_new_dic.get(key)
                job_new_dic.pop(temp_key)
                try:
                    job_new_dic[real_name] = job_name_dict.get(key) + value
                except Exception:
                    print(key)
    job_name_dict = job_new_dic


def checkAndMerge(s1, s2):
    s1_list = [i for i in s1]
    s2_list = [j for j in s2]
    a = OrderedDict.fromkeys(s1_list).keys()
    b = OrderedDict.fromkeys(s2_list).keys()
    return "".join(list(a & b))


if __name__ == '__main__':
    jaro = JaroDaiHei(0)
    job_name_list = get_excel()
    job_name_dict = create_dict(job_name_list)
    # reload()

    sorted_dict = {k: v for k, v in sorted(job_name_dict.items(), key=lambda item: item[1], reverse=True)}
    print(sorted_dict)
    for i in range(len(sorted_dict.keys())):
        if i < 20:
            print(list(sorted_dict.keys())[i], sorted_dict.get(list(sorted_dict.keys())[i]))
        else:
            break

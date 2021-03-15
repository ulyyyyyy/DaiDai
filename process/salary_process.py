import xlrd
import re
import xlwt
from xlutils.copy import copy

re_salary = re.compile("([\d\.\-]*)([\S]*)$")

original_excel = xlrd.open_workbook_xls("process.xls")

original_table = original_excel.sheet_by_index(0)  # 通过索引顺序获取


def change_salery():
    newWb = xlwt.Workbook(encoding="uft-8", style_compression=0)
    newSheet = newWb.add_sheet("original")
    job_salary_list = original_table.col_slice(2, start_rowx=1, end_rowx=None)  # 返回由该列中所有的单元格对象组成的列表
    avg_salary_list = []

    for salary in job_salary_list:
        (num, unit) = (re_salary.findall(str(salary.value).strip()))[0]
        num = [float(x) for x in num.split("-")]
        avg_num = sum(num) / len(num)

        if unit == "万/月":
            avg_num *= 10000
        elif unit == "千/月":
            avg_num *= 1000
        elif unit == "元/天":
            avg_num *= 30
        else:
            avg_num = avg_num * 10000 / 12

        avg_salary_list.append(avg_num)
    for i in range(len(avg_salary_list)):
        try:
            newSheet.write(i + 1, 2, int(avg_salary_list[i]))
        except Exception as e:
            print(e)
            print(i + 1, avg_salary_list[i])
    newWb.save(r"process1.xls")


def change_job_name():
    pass


if __name__ == '__main__':
    change_salery()

import re
import xlrd
import jieba.analyse

data = xlrd.open_workbook_xls("./process/process.xls")

table = data.sheet_by_index(0)  # 通过索引顺序获取

job_name_list = table.col_slice(0, start_rowx=1, end_rowx=None)  # 返回由该列中所有的单元格对象组成的列表

job_name = re.findall("text:'(.*?)'", str(job_name_list))

job_description_list = table.col_slice(11, start_rowx=1, end_rowx=None)

job_description_list = re.findall("text:'(.*?)'", str(job_description_list))

for i in range(len(job_description_list[0: 5])):
    keywords = jieba.analyse.extract_tags(job_description_list[i], tsopK=10, withWeight=True, allowPOS=('n', 'nr', 'ns'))
    print(f"{job_name[i]}   ---   {[keyword[0] for keyword in keywords]}")

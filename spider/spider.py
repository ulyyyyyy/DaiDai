# Copyright (c) 2021 hei & DAI

import requests
import re
import json
import urllib.parse as parse
import xlwt
import time
from idna import unicode

# 设置请求头
from lxml import etree
from xlwt import easyxf

heade = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    "Accept-Language": "zh-CN,zh;q=0.9"
}

ROW = [1]

f = xlwt.Workbook(encoding="utf-8")
sheet1 = f.add_sheet('职位', cell_overwrite_ok=True)

default = easyxf('font: name Arial;')


def get_html(url):
    # 获取html内容
    res = requests.get(url, headers=heade)
    # 正则表达式匹配找到相关信息岗位信息
    result = re.findall("window.__SEARCH_RESULT__(.*?)</script>", res.text)
    # 岗位信息转化为json格式
    content = json.loads(result[0][2:])
    # 循环输出职位信息（职位名，公司名，工资，相关信息）
    write_2_xlxs(content)

    # 休眠
    time.sleep(3)


def write_2_xlxs(content: dict):
    # 写入数据
    global sheet1
    for job in content['engine_search_result']:
        try:
            job_name = job["job_name"]
            job_title = job["job_title"]
            company_name = job["company_name"]
            job_salary = job['providesalary_text']
            if len(job['attribute_text']) == 4:
                job_exp = job['attribute_text'][1]
                academic_requirements = job["attribute_text"][2]
                job_hc = job["attribute_text"][3]
            elif len(job['attribute_text']) == 3:
                job_exp = job['attribute_text'][0]
                academic_requirements = job['attribute_text'][1]
                job_hc = job["attribute_text"][2]
            else:
                job_exp = job['attribute_text'][0]
                academic_requirements = "无"
                job_hc = job["attribute_text"][1]
            job_welf = job["jobwelf_list"]
            company_type = job["companytype_text"]
            updated = job["updatedate"]

            job_href = job["job_href"]
            res = requests.get(job_href, headers=heade)
            content = unicode(eval(repr(res.text.encode('raw_unicode_escape'))), "gbk")
            tree = etree.HTML(content)
            data = tree.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div//text()')
            job_description = ""
            for d in data:
                job_description += d

            job_area = re.findall("<p class=\"msg ltype\" title=\"(.*?)&nbsp;&nbsp;", content)[0]
            job_info = [job_name, job_title, company_name, job_area, job_salary, job_exp, academic_requirements, job_hc,
                        job_welf, company_type, updated, job_description]

            for j in range(len(job_info)):
                sheet1.write(ROW[0], j, job_info[j], default)
            print(f"爬取第{ROW}条数据成功")
            ROW[0] = ROW[0] + 1
            time.sleep(1.5)
        except IndexError:
            print(job['attribute_text'])
        except Exception as e:
            print(e)
            print(f"爬取第{ROW}条数据失败")
    f.save(f'data.xls')


if __name__ == '__main__':
    name = input("请输入爬取的职位：")
    pages = int(input("请输入爬取页数："))

    title_row = ['工作名称', "职称", "公司名称", '工作地区', "薪资", "工作经验", '学历要求', '招聘人数', "工作福利", "公司类型", "发布时间", '职位描述']

    # 写入title
    for i in range(0, len(title_row)):
        sheet1.write(0, i, title_row[i], default)

    for i in range(1, pages + 1):
        print(f"正在爬取第{i}页")
        # 运行爬虫
        url = f'https://search.51job.com/list/000000,000000,0000,00,9,99,{parse.quote(parse.quote(name))},2,{i}.html'
        get_html(url)

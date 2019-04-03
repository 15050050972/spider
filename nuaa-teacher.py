# 爬取南航研究生导师信息
# http://gsmis.nuaa.edu.cn/gmis/xkjsb/xkds.aspx?xsbh=017
import requests
from bs4 import BeautifulSoup
import csv

baseUrl = 'http://gsmis.nuaa.edu.cn/gmis/xkjsb/'
r = requests.get(baseUrl + 'xkds.aspx?xsbh=017')
soup = BeautifulSoup(r.text, "lxml")
links = soup.find(id='Table5').find_all(
    'tr')[2].find_all('td')[2].find_all('a')

titles = ['姓名', '性别', '行政职务', '专业技术职务', '导师类别', '最后学位', '最后毕业学校', '工作单位', '学科一专业名称', '学科一内容',
          '学科二专业名称', '学科二内容', '个人简历', '发表学术论文', '科研成果及专利', '承担的科研项目', '指导研究生情况', '备注']
rows = []
# 从第14个开始，前面是博导
for i, link in enumerate(links[14:]):
    r = requests.get(baseUrl + link['href'])
    soup = BeautifulSoup(r.text, "html.parser")
    ids = ['lbldsxm', 'lbldsxb', 'lblxzzw', 'lblzc', 'lbldslb', 'lblxw', 'lblhxlyx', 'lblgzdw', 'lblcszym', 'lblyjfx',
           'lblcszym1', 'lblyjfx', 'txtgrjl', 'lblxsrz', 'lblxscj', 'lbljf', 'lblbz', 'txtbz']

    row = []
    for j, id in enumerate(ids):
        try:
            res = soup.find(id=id)
            if(j == 0):
                print(i, '-', len(links)-14, ':', res.get_text())
            # print(res.get_text())
            row.append(res.get_text())
        except AttributeError:
            row.append('')
    rows.append(row)

with open('result.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(titles)
    for row in rows:
        writer.writerow(row)

'''
# name = soup.find(id='lbldsxm')
    # sex = soup.find(id='lbldsxb')
    # 行政职务
    adminDuties = soup.find(id='lblxzzw')
    # 专业技术职务
    technicalPosition = soup.find(id='lblzc')
    # 导师类别
    tutorKind = soup.find(id='lbldslb')
    # 最后学位
    finalDegree = soup.find(id='lblxw')
    # 最后毕业学校
    finalSchool = soup.find(id='lblhxlyx')
    # 工作单位
    workUnit = soup.find(id='lblgzdw')
    # 学科一 专业名称
    profressionalName1 = soup.find(id='lblcszym')
    # 学科一 内容
    profressionalContent1 = soup.find(id='lblyjfx')
    # 学科二 专业名称
    profressionalName2 = soup.find(id='lblcszym1')
    # 学科二 内容
    profressionalContent2 = soup.find(id='lblyjfx')
    # 个人简历
    resume = soup.find(id='txtgrjl')
    # 发表学术论文
    paper = soup.find(id='lblxsrz')
    # 科研成果及专利
    patent = soup.find(id='lblxscj')
    # 承担的科研项目
    researchProject = soup.find(id='lbljf')
    # 指导研究生情况
    postgraduate = soup.find(id='lblbz')
    # 备注
    remark = soup.find(id='txtbz')
'''
import json
from selenium import webdriver
from lxml import etree
import os
import requests


# https://so.m.jd.com/category/all.html

# 获取一级分类,京东页面有反爬虫机制 这里用selenium捉取页面数据
def get_All_CateGory_Id():
    rootPatch = './京东分类'
    if not os.path.exists(rootPatch):
        os.mkdir(rootPatch)

    path = './phantomjs'
    driver = webdriver.PhantomJS(path)
    print('正在获取全部一级分类')
    driver.get('https://so.m.jd.com/category/all.html')
    data = driver.page_source
    selector = etree.HTML(data)
    print('获取完成---开始解析数据')
    cateGoaryLsit = selector.xpath('//*[@id="category11"]/li/a/text()')
    cateGoary_Id_List = selector.xpath('//*[@id="category11"]/li')
    i = 0
    for link in cateGoary_Id_List:
        dirPath = './京东分类/' + cateGoaryLsit[i]
        if not os.path.exists(dirPath):
            os.mkdir(dirPath)
        cateGoary_ID = link.xpath("@m_cid")[0]
        if cateGoary_ID != '-10086':
            get_Two_Categoary(cateGoary_ID, cateGoaryLsit[i])
        i = i + 1


# 进入二级分类
def get_Two_Categoary(categoary_Id, name):
    cateGory_url = 'https://so.m.jd.com/category/list.action?_format_=json&catelogyId=' + categoary_Id
    req = requests.get(cateGory_url)
    req.encoding = 'utf-8'
    print('正在获取' + name + '一级分类')
    one_path = './京东分类/' + name
    if not os.path.exists(one_path):
        print('目录已创建' + one_path)
        os.mkdir(one_path)
    jsonObject = json.loads(req.text)
    jsonList = json.loads(jsonObject['catalogBranch'])['data']
    for list in jsonList:
        # 二级分类名称
        two_name = list['name']
        print('正在一级分类<' + name + '>' + '的处理二级分类' + two_name)
        two_dirPath = one_path + '/' + two_name
        if not os.path.exists(two_dirPath):
            print('目录已创建' + two_dirPath)
            os.mkdir(two_dirPath)
        # 二级分类下面的三级分类
        catelogyList = list['catelogyList']
        for catelogy in catelogyList:
            icon = catelogy['icon']
            # 这里修改ICON的尺寸
            icon_size = icon.replace('s100x100', 's195x195')
            cateName = catelogy['name']
            print('正在获取三级分类<' + cateName + ">")
            if icon != '':
                downloaderPic(icon_size, two_dirPath, cateName)
            else:
                print('有一张空图片')


def downloaderPic(url: str, savePath: str, name: str):
    try:
        req = requests.get(url, timeout=10)
        if os.path.exists(savePath):
            three_path = savePath + '/' + name.replace('/', '') + '.jpg'
            fp = open(three_path, "wb")
            fp.write(req.content)
            fp.close()
            print('图片已经写入目录' + savePath)
        else:
            print('图片保存失败' + savePath)

    except requests.exceptions.ConnectionError:
        print
        '【错误】当前图片无法下载'


if __name__ == '__main__':
    get_All_CateGory_Id()

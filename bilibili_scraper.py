# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from bs4 import BeautifulSoup
import time


class Parameters:
    def __init__(self):
        self.dcap = {}
        self.driverPath = ""
        self.xPaths = {}
        self.cid = ""
        self.title = ""
        self.togglename = "v-part-toggle"


# 初始化参数
def init_parameters():
    p = Parameters()
    # 伪装成火狐浏览器(只是提供一个选择, 并不必要)
    p.dcap = dict(DesiredCapabilities.PHANTOMJS)
    p.dcap["phantomjs.page.settings.userAgent"] = \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 "
    # phantonJS的bin文件地址
    p.driverPath = "/Users/Shawn/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs"
    # xpaths
    p.xPaths["sortByHotButton"] = ".//*[@id='list_order_hot']"
    p.xPaths["videoList"] = "html/body/div[4]/div/div[2]/div/div[2]/div[2]/div[2]/ul"
    p.xPaths["videoInfo"] = ".//*[@id='player_placeholder']"
    p.xPaths["plist"] = ".//*[@id='plist']"
    p.xPaths["plistButton"] = ".//*[@id='plist']/span"
    p.xPaths["bgmlist"] = ".//*[@id='v_bgm_list_data']"
    return p


def get_video_plist(driver, page_url, p):
    link_list = []
    cut_current_list = re.search("/video/av[0-9]+/", page_url).group(0)
    try:
        driver.get(page_url)
        # 检查是否多p
        span = driver.find_elements_by_xpath(p.xPaths["plistButton"])
        if len(span) == 0:
            raise Exception('No other page found')
        # 检查是否有展开按钮, 有就按一下
        unfold_button = driver.find_elements_by_class_name(p.togglename)
        if len(unfold_button) == 1:
            unfold_button[0].click()
        # 截取展开后的所有链接
        plist = driver.find_element_by_xpath(p.xPaths["plist"])
        list_source = plist.get_attribute('innerHTML')
        # 导入bs4识别链接, 保存至link_list
        bsobj = BeautifulSoup(list_source, "html.parser")
        a_list = bsobj.findAll("a", {"href": re.compile("/video/[a-z0-9/_.]+")})
        link_list.append(cut_current_list)
        for a in a_list:
            link_list.append(str(a["href"]))
        return link_list
    except Exception as ex:
        print(ex)
        link_list.append(cut_current_list)
        return link_list


def get_video_bgmlist(driver, page_url, p):
    link_list = []
    cut_list = re.search("/video/av[0-9]+/", page_url).group(0)
    try:
        driver.get(page_url)
        # 找到链接栏, 导入bs4识别链接, 保存
        bgmlist = driver.find_element_by_xpath(p.xPaths["bgmlist"])
        list_source = bgmlist.get_attribute('innerHTML')

        bsobj = BeautifulSoup(list_source, "html.parser")
        a_list = bsobj.findAll("a", {"href": re.compile("/video/av[0-9]+/")})
        link_list.append(cut_list)
        for a in a_list:
            link_list.append(str(a["href"]))
        return link_list
    except Exception as ex:
        print(ex)
        link_list.append(cut_list)
        return link_list


def scraper(scrape_url, p, flag):
    driver = webdriver.PhantomJS(executable_path=p.driverPath,
                                 desired_capabilities=p.dcap)
    if flag == "new":
        link_list = get_video_bgmlist(driver, scrape_url, p)
    elif flag == "old":
        link_list = get_video_plist(driver, scrape_url, p)
    else:
        print('Flag not recognized!')
        driver.close()
        return None
    # 分别打开链接, 保存cid等信息
    for link in link_list:
        page_url = "http://www.bilibili.com" + str(link)
        # 爬取页面失败重试3次, 再失败则跳过
        cid_flag = get_page_info(driver, page_url, p)
        if not cid_flag:
            for i in range(3):
                cid_flag = get_page_info(driver, page_url, p)
                if cid_flag:
                    break
                print("Get cid failed, retrying...")
            if not cid_flag:
                print("Retry times out, skip")
                continue
        # 下载失败重试3次, 再失败则跳过
        save_flag = save_comments(driver, p)
        if not save_flag:
            for i in range(3):
                save_flag = save_comments(driver, p)
                if save_flag:
                    break
                print("Save comments failed, retrying...")
            if not save_flag:
                print("Retry times out, skip")
                continue
    driver.close()


def get_page_info(driver, page_url, p):
    try:
        driver.get(page_url)
        source_code = driver.page_source
        # 源代码中可以找到cid和title, 对应弹幕文件和标题
        title_reg = re.compile("(?<=<title>).*(?=</title>)")
        cid_reg = re.compile("(?<=cid=)[0-9]+")
        p.title = re.search(title_reg, source_code).group(0).encode('utf-8')
        p.cid = str(re.search(cid_reg, source_code).group(0))
        return True
    except Exception as ex:
        print("Get cid failed:")
        print(ex)
        return False


def save_comments(driver, p):
    # b站保存弹幕的地址在此
    comment_url = "http://comment.bilibili.tv/" + p.cid + ".xml"
    print(p.title)
    print("Fetching...")
    # 下载xml, 按标题作为文件名保存, 超时时长30秒
    try:
        driver.set_page_load_timeout(30)
        driver.get(comment_url)
        source = driver.page_source
        with open("./data/" + p.title + ".xml", 'w') as fd:
            fd.write(source.encode('utf-8'))
            print("Saved!")
        return True
    except Exception as ex:
        print("Save comments failed")
        print(ex)
        return False

p = init_parameters()
scraper("http://www.bilibili.com/video/av5313786/", p, "old")
scraper("http://www.bilibili.com/video/av5280311/", p, "new")

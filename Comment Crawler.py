# -*- coding: utf-8 -*-
# @Author: Hayashi 林
# @Date  : 2022/3/27 19:52
# 世界中に嵐を巻き起こしよう

from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time
import pandas as pd
import re


# # 过滤表情
# def clean(desstr, restr=''):
#     try:
#         co = re.compile(u'['u'\U0001F300-\U0001F64F' u'\U0001F680-\U0001F6FF'u'\u2600-\u2B55]+')
#     except re.error:
#         co = re.compile(u'('u'\ud83c[\udf00-\udfff]|'u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'u'[\u2600-\u2B55])+')
#     return co.sub(restr, desstr)


class Crawler(object):
    # 初始化浏览器配置
    def __init__(self, url):
        option = ChromeOptions()
        # 反屏蔽
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        # 修改下载地址
        option.add_experimental_option("prefs",
                                       {"download.default_directory": "D:\\LH_pycharm\\Wangyiyun Music"})
        self.browser = webdriver.Chrome(options=option)
        self.browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                                     {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
        # 隐式等待，直到网页加载完毕，最长等待时间为20s
        self.browser.implicitly_wait(20)
        # 目标网页：url
        self.url = url

    # 提交查询并下载
    def download_comment(self):
        self.browser.get(self.url)
        # 切换frame
        self.browser.switch_to.frame("g_iframe")

        # 获取歌曲名称
        song_title = self.browser.find_element_by_xpath("//em[@class='f-ff2']").text
        print('歌曲名称：', song_title)
        # 预设评论存储格式
        comment_df = pd.DataFrame(columns=['Comment', 'Data_id'])

        # 提取最大页数
        max_page_num = self.browser.find_elements_by_xpath('//a[@href="#"]')[-3].text
        print('最大评论页数:', max_page_num)

        # 翻页循环
        page = 1
        while page <= int(max_page_num):
            print('开始下载第', page, '页')
            # 鼠标滚动到页面底部以刷新
            self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            try:
                comment_nodes1 = self.browser.find_elements_by_class_name('itm')
                comment_nodes2 = self.browser.find_elements_by_css_selector("[class='cnt f-brk']")
                print(len(comment_nodes1), len(comment_nodes2))
                for node_num in range(len(comment_nodes1)):
                    node1 = comment_nodes1[node_num]
                    data_id = str(node1.get_attribute('data-id'))

                    node2 = comment_nodes2[node_num]
                    comment = node2.text
                    # comment包含两部分信息，格式形如：用户昵称+'：'+用户评论
                    # 这里只提取用户评论
                    comment = comment.split('：', 1)[1]
                    # # 过滤网络文本中的各种表情符号
                    # comment = clean(comment)
                    # 只提取评论里的汉字字符
                    pattern = u'[\u4e00-\u9fff]+'  # 汉字正则表达式
                    re_compile = re.compile(pattern)
                    comment = ' '.join(re_compile.findall(comment))

                    temp_df = pd.DataFrame({'Data_id': data_id, 'Comment': comment}, index=[1])
                    comment_df = comment_df.append(temp_df, ignore_index=True)  # 忽略原有的index，直接从最后一行开始追加
                # 点击“下一页”
                self.browser.find_elements_by_xpath('//div[@id="comment-box"]/div/div[2]/div[3]/div/a')[-1].click()
            except:
                print('当前页面无评论')
                time.sleep(3)
                break
            print(comment_df.tail(3))
            page += 1
        # 去除最开头的热门评论
        # 依靠[data_id, comment]的唯一性删除
        comment_df = comment_df.drop_duplicates()  # drop_duplicates()默认判断全部列
        comment_df = comment_df.reset_index(drop=True)  # 重置索引
        # 存储
        comment_df.to_csv('Music Comments_{}.csv'.format(song_title), encoding='gb18030')
        self.browser.close()


url_list = ['https://music.163.com/#/song?id=30612859', 'https://music.163.com/#/song?id=1487546210']
for url_num in range(len(url_list)):
    url = url_list[url_num]
    print('开始下载：', url_num)
    Wangyi_Music = Crawler(url)
    Wangyi_Music.download_comment()

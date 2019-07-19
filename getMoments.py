from appium import webdriver
import time
import re
import sys

#进入昵称为name的好友的朋友圈的点击逻辑
def enter_pengyouquan(name):
    driver.find_element_by_id('com.tencent.mm:id/iq').click()  #点击搜索图标
    time.sleep(2)
    driver.find_element_by_id('com.tencent.mm:id/kh').send_keys(name)  #输入搜索文字
    time.sleep(2)
    driver.find_element_by_id('com.tencent.mm:id/q0').click()  #点击第一个搜索结果
    driver.find_element_by_id('com.tencent.mm:id/jy').click()  #点击聊天界面右上角三个小点
    driver.find_element_by_id('com.tencent.mm:id/e0c').click() #点击头像
    driver.find_element_by_id('com.tencent.mm:id/d7w').click() #点击朋友圈

#上拉方法
def swipe_up(distance, time):  #distance为滑动距离，time为滑动时间
    width = 1080
    height = 2150  # width和height根据不同手机而定
    driver.swipe(1 / 2 * width, 9 / 10 * height, 1 / 2 * width, (9 / 10 - distance) * height, time)

#获取当前朋友圈界面的文字
def get_onepage():
    eleLst = get_onepage_elementlist()
    pagetext = []
    for e in eleLst:
        try:
            pagetext.append(e.get_attribute('text'))
        except:
            pass
    return pagetext

#获取当前朋友圈界面的相关元素
def get_onepage_elementlist():
    pict_list = driver.find_elements_by_id('com.tencent.mm:id/nm')  #带图朋友圈配文和视频朋友圈配文
    link_list = driver.find_elements_by_id('com.tencent.mm:id/kt')  #链接朋友圈配文和纯文字朋友圈
    elementlist = pict_list + link_list
    return elementlist

#获取往前倒推year_count年到现在的所有朋友圈
def get_pages(year_count):
    pagestext = []
    current_year = driver.find_element_by_id("com.tencent.mm:id/ekg").get_attribute("text") #获得当前年份
    while True:
        try:
            end_year = str(int(current_year[0:4]) - year_count) + "年"
            y = driver.find_element_by_id("com.tencent.mm:id/ekg").get_attribute("text")   #在页面中寻找显示年份的元素，没找到就会报错，继续上拉
            if y == end_year:   #到达结束年份
                break
            else:  #未到达结束年份，继续上拉
                pagetext=get_onepage()
                for t in pagetext:
                    if t not in pagestext:
                        pagestext.append(t)
                swipe_up(1 / 2, 2000)

        except:
            pagetext = get_onepage()
            for t in pagetext:
                if t not in pagestext:
                    pagestext.append(t)
            swipe_up(1 / 2, 2000)


    pagetext = get_onepage()
    for t in pagetext:
        if t not in pagestext:
            pagestext.append(t)
    while True:
        try:
            driver.find_element_by_id("com.tencent.mm:id/ekg")
            swipe_up(1/12,500)
        except:
            break
    #删除最后一页多获取的朋友圈文本
    lastPage=get_onepage()
    for t in lastPage:
        if t in pagestext:
            pagestext.remove(t)
    return pagestext

def store_PYQText(PYQ_list,store_path):  #将朋友圈文本存储到指定路径
    f = open(store_path, 'w', encoding='utf-8')
    for text in PYQ_list:
        f.write(text + '\n\n')
    f.close()

#去除表情文本
def remove_icondesc(list, storepath):
    f = open(storepath, 'w', encoding='utf-8')
    patten = re.compile('\w+(?![\u4e00-\u9fa5]*])')  #匹配除表情文本外的所有文本
    for s in list:
        splitted_sentences = re.findall(patten, s)
        for p in splitted_sentences:
            f.write(p + '\n')
    f.close()

if __name__ == '__main__':
    desired_caps = {
        'platformName': 'Android',
        'deviceName': '37KNW18710001152',
        'platformVersion': '9',
        'appPackage': 'com.tencent.mm',  # apk包名
        'appActivity': 'com.tencent.mm.ui.LauncherUI',  # apk的launcherActivity
        'noReset': 'True',  # 每次运行脚本不用重复输入密码启动微信
        'unicodeKeyboard': 'True',  # 使用unicodeKeyboard的编码方式来发送字符串
        'resetKeyboard': 'True'  # 将键盘给隐藏起来
    }
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    time.sleep(5)
    enter_pengyouquan('沐皮')
    PYQ_list = get_pages(1)  #获取最近一年的朋友圈
    store_PYQText(PYQ_list,r'D:\词云\沐皮完整朋友圈.txt')  #存储原始朋友圈
    remove_icondesc(PYQ_list, r'd:\词云\沐皮.txt')  #存储删除表情文本和符号之后的朋友圈，为生成词云做准备
    driver.quit()




import os
import re
import time
import wait
import fileinput
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ChromeOptions


def vision(account):
    print("等待软件加载...")
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 全程隐藏浏览器
    option.add_argument("headless")
    # 全程静音播放
    option.add_argument("--mute-audio")
    option.add_argument('log-level=3')
    browser = webdriver.Chrome(options=option)
    print('等待网页加载...')
    browser.get('http://www.51ixuejiao.com/student/index.ashx')
    time.sleep(5)

    input_account = browser.find_element_by_xpath("//*[text()='账号/手机号/身份证号']/preceding-sibling::input")
    input_account.send_keys(account)

    input_password = browser.find_element_by_xpath("//*[text()='密码']/preceding-sibling::input")
    input_password.send_keys(account[-6:])

    browser.get_screenshot_as_file("./jt.png")
    try:
        Image.open('./jt.png').show()
    except:
        print("若未弹出图片，请自行打开jt.png文件查看验证码")
    input_code = browser.find_element_by_xpath("//*[text()='验证码']/preceding-sibling::input")
    code = input("输入验证码：")
    input_code.send_keys(code)

    browser.find_element_by_class_name("btnLogin").click()
    cookie_value = browser.get_cookie("sharekeyid")["value"]
    time.sleep(2)

    if not os.path.exists("./restUrl.txt"):
        couid = input("输入课程id,请确保已购买：")
        class_id(couid, cookie_value, browser)

    f = open("./restUrl.txt", "r")
    lines = f.readlines()
    f.close()

    for i in lines:
        browser.get(i.replace("\n", ''))
        print("等待视频加载...")
        try:
            time.sleep(3)
            browser.execute_script('window.onblur=null')
            browser.execute_script(f'document.querySelector("video").playbackRate=2')
        except:
            browser.get(i.replace("\n", ''))
        while 1:
            time_str = browser.find_element_by_id("videoinfo").get_attribute('textContent')
            show_str = time_str.split('，')
            end = re.search("%", time_str).end()
            if time_str[end - 4:end] == '100%':
                print('当前视频播放完成')
                add_url("./successUrl.txt", i)
                minus_log("./restUrl.txt")
                break
            try:
                wait.visible_xpath("//div[@class='qplayer-playbtn']/button", browser, 10)
                button = browser.find_element_by_xpath("//div[@class='qplayer-playbtn']/button")
                start_button = button.get_attribute('class')
            except:
                browser.get(i.replace("\n", ''))
                continue
            if start_button == 'qplayer-active qplayer-play':
                print('当前暂停，等待点击开始')
                try:
                    button.click()
                    print("已开始")
                except:
                    print('点击开始失败刷新页面!')
                    browser.get(i.replace("\n", ''))
                    continue
            title = browser.find_element_by_xpath("//div[@class='olitem li-video current ']/a").get_attribute(
                "textContent").replace("\n", '').replace(" ", '')
            print(f'正在播放：{title}，已' + show_str[3])
            time.sleep(1)

    os.remove("./restUrl.txt")
    os.remove('./successUrl.txt')
    os.remove('./jt.png')
    browser.close()
    print("任务完成")


def class_id(couid, cookie_value, browser):
    browser.get(f"http://www.51ixuejiao.com/CourseStudy.ashx?couid={couid}&sharekeyid={cookie_value}")

    if wait.visible_xpath("//div[@isvideo='true']", browser):
        lists = browser.find_elements_by_xpath("//div[@isvideo='true']")
        for i in lists:
            olid = i.get_attribute('olid')
            class_url = f"http://www.51ixuejiao.com/CourseStudy.ashx?couid={couid}&sharekeyid={cookie_value}&olid={olid}"
            add_url("./restUrl.txt", class_url + '\n')
    return


# 用于写入url
def add_url(file, write):
    f = open(file, 'a+')
    f.write(write)
    f.close()


# 用于删除url
def minus_log(file):
    for line in fileinput.input(file, inplace=1):
        if not fileinput.isfirstline():
            print(line.replace('\n', ''))

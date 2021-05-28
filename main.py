from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
#实现无可视化界面
from selenium.webdriver.chrome.options import Options
#实现规避检测
from selenium.webdriver import ChromeOptions

#实现无可视化界面的操作
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

#实现规避检测
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
browser = webdriver.Chrome(executable_path='./chromedriver.exe',options=option)
UserName = ''
PassWord = ''
Course_ID = ['']
Tearcher_ID = ['']
global cnt
cnt = 0


def login():
    # 登录界面
    browser.get(
        'https://oauth.shu.edu.cn/login/eyJ0aW1lc3RhbXAiOjE2MTA4OTM4NTU1MjkxODMxNTAsInJlc3BvbnNlVHlwZSI6ImNvZGUiLCJjbGllbnRJZCI6InlSUUxKZlVzeDMyNmZTZUtOVUN0b29LdyIsInNjb3BlIjoiIiwicmVkaXJlY3RVcmkiOiJodHRwOi8veGsuYXV0b2lzcC5zaHUuZWR1LmNuL3Bhc3Nwb3J0L3JldHVybiIsInN0YXRlIjoiIn0=')
    browser.find_element_by_id('username').send_keys(UserName)
    browser.find_element_by_id('password').send_keys(PassWord)
    browser.find_element_by_id('submit').click()
    print('登录完成')
    return


def semester():
    # 选择学期界面
    print('进入学期界面')
    time.sleep(3)
    browser.find_elements_by_name('rowterm')[1].click();
    browser.find_element_by_class_name('btn-primary').click()
    return


# 课程查询页
def query():
    # 课程查询页
    time.sleep(2.5)
    browser.find_element_by_link_text('课程查询').click()
    print('进入课程查询页面')
    time.sleep(2.5)
    browser.find_element_by_name('CID').send_keys(Course_ID)
    browser.find_element_by_name('TeachNo').send_keys(Tearcher_ID)
    browser.find_element_by_css_selector('td>label>input').click()
    flag = True
    while flag:
        time.sleep(1.5)
        browser.find_element_by_id('QueryAction').click()
        try:
            browser.find_element_by_xpath('//tr[@name="rowclass"]/td[@style="color: Red;"]')  # 出现了就说明可以选课
        # 人数满了
        except Exception:
            global cnt
            cnt += 1
            print(cnt, '人数已满')
        # 人数未满
        else:
            print('人数未满')
            flag = False
    return


def select():
    # 选课详情页
    Flag = True
    while Flag:
        query()
        browser.find_element_by_link_text('选课').click()
        time.sleep(1)
        print('==================进入选课页面===============')
        browser.find_element_by_id('CID0').send_keys(Course_ID)
        browser.find_element_by_id('TNo0').send_keys(Tearcher_ID)
        browser.find_element_by_id('FastInputAction').click()
        try:
            # 结果页面
            time.sleep(3)
            browser.find_element_by_css_selector('td[style="color:Red;"]')  # 出现了就说明没选成功
        # 选成功了
        except NoSuchElementException:
            browser.find_element_by_xpath('//td[@style="text-align:left;"]/button').click()
            Flag = False
            print('选课成功=========================================================')
            browser.quit()
        # 选失败了
        else:
            time.sleep(1)
            browser.find_element_by_xpath('//td[@style="text-align:left;"]/button').click()
    return


if __name__ == "__main__":
    login()
    semester()
    select()

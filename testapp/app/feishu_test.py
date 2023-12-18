#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/18 17:29
# @Author  : v_bkaiwang
# @File    : feishu_test.py
# @Software: win10 Tensorflow1.13.1 python3.6.3

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.test_data import UserData

URL = "https://www.feishu.cn"
TEST_CODE = "https://www.feishu.cn 123123123"


def get_window(browser_name: str, url: str, hold: bool) -> object:
    """
    启动Chrome浏览器
    :param browser_name:选择的浏览器名字
    :param url:目标网站
    :param hold:是否保持状态
    :return:窗口对象
    """
    print('=================================Start_test=================================')
    if browser_name == 'chrome':
        web_driver = webdriver.Chrome(keep_alive=hold)
    elif browser_name == 'firefox':
        web_driver = webdriver.Firefox()
    elif browser_name == 'ie':
        web_driver = webdriver.Ie()
    # elif browser_name == 'opera':
    #     driver = webdriver.Opera()
    else:
        raise ValueError("Unsupported browser: " + browser_name)
    # 最大化窗口
    # web_driver.maximize_window()
    web_driver.get(url)
    return web_driver


def click_element_by_xpath(driver, xpath: str) -> None:
    """
    点击元素
    :param driver:窗口对象
    :param xpath:元素
    :return:
    """
    try:
        # 等待元素加载完成
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        # 点击元素
        element.click()
    except Exception as e:
        print("点击元素时发生异常：", e)


def input_element_by_xpath(driver, xpath: str, input_text: str) -> None:
    """
    点击和输入一起
    :param driver:窗口对象
    :param xpath:元素
    :param input_text:输入的文字
    :return:
    """
    try:
        # 等待元素加载完成
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

        # 输入文本
        element.click()
        element.send_keys(input_text)
    except Exception as e:
        print("点击和输入元素时发生异常：", e)


def click_element_by_text(driver, text: str) -> None:
    """
    根据文本进行元素操作
    :param driver:窗口对象
    :param text:目标文本
    :return:
    """
    try:
        # 找到包含指定文本的元素并点击
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '" + text + "')]"))
        )
        element.click()
    except Exception as e:
        print("点击元素时发生异常：", e)


def send_message_and_return(driver, xpath: str, input_text: str) -> None:
    """
    这个方法有模拟回车
    :param driver:窗口对象
    :param xpath:元素
    :param input_text:目标文本
    :return:
    """
    try:
        # 等待元素加载完成
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

        # 输入文本
        element.click()
        element.send_keys(input_text)
        # 模拟回车
        element.send_keys(webdriver.common.keys.Keys.RETURN)
    except Exception as e:
        print("点击和输入元素时发生异常：", e)


def close_window(driver):
    """
    关闭窗口 手机要清除登录态
    :param driver:
    :return:
    """
    driver.quit()
    print('=================================Test_completed!!!=================================')


if __name__ == '__main__':

    print()
    driver = get_window(browser_name='chrome', url=URL, hold=True)
    # 有两个弹窗，都是一个层级里的
    click_element_by_xpath(driver, '/html/body/div[2]/div[2]/div/div/div')
    click_element_by_xpath(driver, '//*[@id="app"]/div/div[2]/div/div/div/div/a[3]')
    time.sleep(2)
    # 切换登陆模式
    click_element_by_xpath(driver, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/div/div/div[1]/div/span')

    # 账号密码登录 前提是登陆过一次 有cookie才可以登录，不然需要输入手机验证码

    time.sleep(2)  # 确认账号
    input_element_by_xpath(driver, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[1]/div/div[2]'
                                   '/div/div[2]/div/div[1]/div[2]/div[1]/div/div/div[2]/input', UserData.name)
    time.sleep(2)  # 勾选协议
    click_element_by_xpath(driver, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div'
                                   '[2]/div/div[2]/label/span[1]/input')
    time.sleep(2)  # 进入输入密码界面
    click_element_by_xpath(driver, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div[2]/div/button')

    time.sleep(2)
    input_element_by_xpath(driver, '//*[@id="root"]/div/div[2]/div[2]/div[1]/'
                                   'div/div/div[3]/div/div[2]/div/div/div/div/div[1]/div/div/div/input', UserData.pw)
    # 这里输入多了会有校验码
    time.sleep(2)
    click_element_by_xpath(driver, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div/div[3]/div/div[3]/div/button')

    # 这里缺少验证码 暂时临时输入 应该可以用接口获得验证码
    time.sleep(10)
    input_element_by_xpath(driver,
                           '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div/div[4]/div/div[2]'
                           '/div/div/div/div/div[2]/div[1]/div[1]/div[1]/input',
                           input('请输入验证码:'))

    time.sleep(4)  # 点击9个点按钮 到二级界面
    click_element_by_xpath(driver, '//*[@id="app"]/div/div[2]/div/div/div/div/div[7]/div/span')
    click_element_by_xpath(driver, '/html/body/div[3]/div[1]/div/div/div/div[1]/ul/li[1]/div')
    # 打开新页面 切换窗口
    old_window, new_window = driver.window_handles
    driver.switch_to.window(new_window)
    time.sleep(3)
    click_element_by_xpath(driver, '//*[@id="app"]/section/div/section/section/section[5]')
    time.sleep(2)  # 通过 元素文字找到tester2的位置且点击
    click_element_by_text(driver, 'tester2')

    # 弹出二级窗口
    click_element_by_xpath(driver, '//*[@id="root-userCardModal"]/div/div[1]/div'
                                   '/div/div/div[1]/div[1]/div[3]/div[3]/button[1]')
    for index in range(6):
        # 模拟按下回车键 点击输入框并输入 这里飞书不稳定 经常载不出文本框但是能发送
        send_message_and_return(driver, '//*[@id="root-messenger-nav-application"]/'
                                        'div/div/div[2]/div[1]/div/div/div/div/di'
                                        'v[1]/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/pre', TEST_CODE)
    close_window(driver)

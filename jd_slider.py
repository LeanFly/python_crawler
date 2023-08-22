# coding = utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import ddddocr
from icecream import ic
import base64
from PIL import Image
from io import BytesIO
import time
import pyautogui


def get_slide_path(bg, slide):
    det = ddddocr.DdddOcr(ocr=False,  det=False)

    # 转换成 Iamge
    background_img = Image.open(BytesIO(base64.b64decode(bg.split(';base64,')[1])))
    target_img = Image.open(BytesIO(base64.b64decode(slide.split(';base64,')[1])))
    # 重新设定宽高
    background_img_resize = background_img.resize((290, 179))
    target_img_resize = target_img.resize((59, 179))
    # 转换成 byte
    bg_byte = BytesIO()
    tg_byte = BytesIO()
    background_img_resize.save(bg_byte, format='JPEG')
    target_img_resize.save(tg_byte, format='PNG')

    res = det.slide_match(tg_byte.getvalue(), bg_byte.getvalue())
    ic(res)
    x = res['target'][0]
    ic(x)
    return(x)

def get_track(distance):
        '''
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        '''
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.5
        # 初速度
        v = 10

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 10
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

def auto_slide(browser):
    if browser.find_element(By.CLASS_NAME, 'verifyBtn'):
        browser.find_element(By.CLASS_NAME, 'verifyBtn').click()
    
    WebDriverWait(browser,4).until(expected_conditions.visibility_of_element_located((By.ID, 'cpc_img')))
    slider_bg = browser.find_element(By.ID, 'cpc_img').get_attribute('src')
    slider_tar = browser.find_element(By.ID, 'small_img').get_attribute('src')
    slider_path = get_slide_path(slider_bg, slider_tar)
    slider_but = browser.find_element(By.CSS_SELECTOR, '#captcha_modal > div > div.captcha_footer > div > img')

    # 点中滑块按钮
    ActionChains(browser).click_and_hold(slider_but).perform()

    # 引入轨迹算法
    track_list = get_track(slider_path)
    ic(track_list)
    track_path = 0
    for i in track_list:
        ActionChains(browser).move_by_offset(xoffset=i, yoffset=0).perform()
        track_path += i
    time.sleep(1)
    ActionChains(browser,duration=100).move_by_offset(xoffset=(slider_path - track_path), yoffset=2.7).perform()
    time.sleep(0.5)
    # 释放
    ActionChains(browser, duration=500).release().perform()
    ic(browser.find_element(By.CLASS_NAME, 'img_tips_wraper').text)
    # ic(WebDriverWait(browser, 3).until(expected_conditions.text_to_be_present_in_element((By.CLASS_NAME, 'img_tips_wraper'), '验证成功')))
    if WebDriverWait(browser, 3).until(expected_conditions.text_to_be_present_in_element((By.CLASS_NAME, 'img_tips_wraper'), '验证成功')):
        print('验证成功')
    #     ic(browser.find_element(By.CLASS_NAME, 'img_tips_wraper').text)
    time.sleep(5)

    # cfe.m.jd.com 如果提示 安全验证 点击安全验证按钮清求滑块，如果提示 前往登录 则跳过
    if 'h5.m.jd.com' in browser.current_url:
        WebDriverWait(browser,4).until(expected_conditions.visibility_of_element_located((By.ID, 'cpc_img')))
        slider_bg = browser.find_element(By.ID, 'cpc_img').get_attribute('src')
        slider_tar = browser.find_element(By.ID, 'small_img').get_attribute('src')
        slider_path = get_slide_path(slider_bg, slider_tar)
        slider_but = browser.find_element(By.CSS_SELECTOR, '#captcha_modal > div > div.captcha_footer > div > img')

        # 点中滑块按钮
        ActionChains(browser).click_and_hold(slider_but).perform()

        # 引入轨迹算法
        track_list = get_track(slider_path)
        ic(track_list)
        track_path = 0
        for i in track_list:
            ActionChains(browser).move_by_offset(xoffset=i, yoffset=0).perform()
            track_path += i
        time.sleep(1)
        ActionChains(browser,duration=100).move_by_offset(xoffset=(slider_path - track_path), yoffset=2.7).perform()
        time.sleep(0.5)
        # 释放
        ActionChains(browser, duration=500).release().perform()
        ic(browser.find_element(By.CLASS_NAME, 'img_tips_wraper').text)
        # WebDriverWait(browser,4).until()
        ic(browser.find_element(By.CLASS_NAME, 'img_tips_wraper').text)
        try:
            cpc_ele = browser.find_element(By.ID, 'cpc_img')
            ic(cpc_ele.get_attribute('src'))
            ic(cpc_ele.text)
        except:
            pass
    if 'cfe.m.jd.com' in browser.current_url:
        # browser.find_element(By.CLASS_NAME, 'verifyBtn').click()
        WebDriverWait(browser,4).until(expected_conditions.visibility_of_element_located((By.ID, 'cpc_img')))
        slider_bg = browser.find_element(By.ID, 'cpc_img').get_attribute('src')
        slider_tar = browser.find_element(By.ID, 'small_img').get_attribute('src')
        slider_path = get_slide_path(slider_bg, slider_tar)
        slider_but = browser.find_element(By.CSS_SELECTOR, '#captcha_modal > div > div.captcha_footer > div > img')

        # 点中滑块按钮
        ActionChains(browser).click_and_hold(slider_but).perform()

        # 引入轨迹算法
        track_list = get_track(slider_path)
        ic(track_list)
        track_path = 0
        for i in track_list:
            ActionChains(browser).move_by_offset(xoffset=i, yoffset=0).perform()
            track_path += i
        time.sleep(1)
        ActionChains(browser,duration=100).move_by_offset(xoffset=(slider_path - track_path), yoffset=2.7).perform()
        time.sleep(0.5)
        # 释放
        ActionChains(browser, duration=500).release().perform()
        ic(browser.find_element(By.CLASS_NAME, 'img_tips_wraper').text)
        # WebDriverWait(browser,4).until()
        ic(browser.find_element(By.CLASS_NAME, 'img_tips_wraper').text)
        try:
            cpc_ele = browser.find_element(By.ID, 'cpc_img')
            ic(cpc_ele.get_attribute('src'))
            ic(cpc_ele.text)
        except:
            pass



if __name__ == '__main__':
    browser = webdriver.Chrome(executable_path="C:\\Users\\ningm\\Documents\python\\browser-drivers\\chromedriver-win-112.exe")

    # browser.get('https://h5.m.jd.com/pb/014137480/2hxUVs4cC2oSZQrFqD1PHxzE7Yee/index.html?scval=pc_detail&ReturnUrl=http%3A%2F%2Fitem.jd.com%2F100027728882.html')
    browser.get('https://cfe.m.jd.com/privatedomain/risk_handler/03101900/?returnurl=https%3A%2F%2Fitem.jd.com%2F10060881246372.html&evtype=2&rpid=rp-186856865-10054-1682573319064')
    browser.maximize_window()
    # time.sleep(5)
    
        # time.sleep(10)
    do_slide = True
    while True:
        auto_slide(browser)
        if WebDriverWait(browser, 3).until(expected_conditions.text_to_be_present_in_element((By.CLASS_NAME, 'img_tips_wraper'), '验证成功')):
            # do_slide = False
            break
            # ic(do_slide)
        # do_slide = True

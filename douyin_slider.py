import requests
import time
from icecream import ic
from ddddocr import DdddOcr

from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


# 初始化检测工具 ddddOcr
det_api = DdddOcr(show_ad=False)

# 生成无头浏览器配置项
edge_options = Options()
# edge_options.add_argument('--headless')
# edge_options.add_argument('--disable-gpu')
# edge_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54'
# edge_options.add_argument(f'user-agent={edge_ua}')

browser = webdriver.Edge(options=edge_options)
browser.get(url)
browser.implicitly_wait(30)
browser.maximize_window()

# 滑块计算
def captcha_slide(bg, slide):
    # # 初始化检测工具 ddddOcr
    # det = ddddocr.DdddOcr(det=False, ocr=False)
    det_api.det = False
    det_api.ocr = False
    # with open('target.png', 'rb') as f:
    #     target_bytes = f.read()

    # with open('background.png', 'rb') as f:
    #     background_bytes = f.read()
    target_bytes = requests.get(slide).content
    background_bytes = requests.get(bg).content

    res = det_api.slide_match(target_bytes, background_bytes)
    ic(res)
    x = res["target"][0] * (340 / 552)
    ic(x)
    return x

# 自动过滑块验证
def captcha_pass(browser):
    # browser.refresh()
    time.sleep(10)
    # 滑块验证
    try:
        if browser.find_element(By.ID, "captcha_container"):
            print("\n************** 发现滑块验证 **************\n")
            # ic(browser.find_element(By.ID, "captcha_container"))

            # browser.refresh()
            if WebDriverWait(browser, 20).until(
                expected_conditions.presence_of_element_located(
                    (By.ID, "captcha-verify-image")
                )
            ):
                # 判断验证类型，滑块验证或者文字点选验证
                if browser.find_element(
                    By.CSS_SELECTOR,
                    "#captcha_container > div > div.captcha_verify_bar.sc-cMljjf.eBYEht > div.captcha_verify_bar--title.sc-jAaTju.iIMDNr",
                ):
                    logger.info("进入文字点选验证")
                    target_img = (
                        browser.find_element(
                            By.CSS_SELECTOR,
                            "#captcha_container > div > div.captcha_verify_bar.sc-cMljjf.eBYEht > div.captcha_verify_bar--title.sc-jAaTju.iIMDNr",
                        )
                        .find_element(By.ID, "verify-bar-code")
                        .get_attribute("src")
                    )

                    target_words = ocr.readtext(target_img)

                    target_words = target_words[0][1]
                    # target_words = target_words.keys()
                    # target_words = list(target_words)
                    logger.info("验证文字：{}".format(target_words))
                    bg = browser.find_element(By.ID, "captcha-verify-image")
                    poses = captcha_text(bg.get_attribute("src"), size=True)
                    logger.info("备选文字：{}".format(poses))

                    for word in target_words:
                        logger.info(word)
                        try:
                            pos = poses[word]
                            logger.info(pos)
                            ActionChains(browser).move_to_element_with_offset(
                                bg, pos[0], pos[1]
                            ).click().perform()
                            time.sleep(0.5)
                        except Exception as e:
                            logger.info("文字验证异常 -> {}".format(e))
                            continue
                    verify_btn = browser.find_element(
                        By.CSS_SELECTOR,
                        "#captcha_container > div > div.captcha_verify_action.sc-jDwBTQ.dhdXHN > div.verify-captcha-submit-button.submit-button___StyledDiv-u3glzd-0.fCoXkP",
                    )
                    verify_btn.click()

                else:
                    # ic(
                    #     browser.find_element(
                    #         By.ID, "captcha-verify-image"
                    #     ).get_attribute("src")
                    # )
                    # ic(
                    #     browser.find_element(
                    #         By.CSS_SELECTOR,
                    #         "#captcha_container > div > div.captcha_verify_img--wrapper.sc-gZMcBi.jzVByM > img.captcha_verify_img_slide.react-draggable.sc-VigVT.ggNWOG",
                    #     ).get_attribute("src")
                    # )
                    try:
                        print("\n************** 尝试滑块验证 **************\n")
                        slide_bg = browser.find_element(
                            By.ID, "captcha-verify-image"
                        ).get_attribute("src")
                        slide_target = browser.find_element(
                            By.CSS_SELECTOR,
                            "#captcha_container > div > div.captcha_verify_img--wrapper.sc-gZMcBi.jzVByM > img.captcha_verify_img_slide.react-draggable.sc-VigVT.ggNWOG",
                        ).get_attribute("src")
                        slide_path = captcha_slide(slide_bg, slide_target)
                        slide_bar = browser.find_element(
                            By.CSS_SELECTOR,
                            "#secsdk-captcha-drag-wrapper > div.secsdk-captcha-drag-icon.sc-kEYyzF.fiQtnm",
                        )
                        # 选中
                        ActionChains(browser).click_and_hold(slide_bar).perform()
                        # 移动算法，移动完整距离之后回退 1个像素的距离
                        for i in [
                            slide_path * 0.7,
                            slide_path * 0.2,
                            slide_path * 0.08,
                            slide_path * 0.02,
                            -1,
                        ]:
                            ActionChains(browser).move_by_offset(
                                xoffset=i, yoffset=0
                            ).perform()
                        # 释放鼠标
                        ActionChains(browser, duration=500).release().perform()
                    except Exception as e:
                        ic(e)
                        pass
    except Exception as e:
        ic(e)
        pass

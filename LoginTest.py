import json
import random
from time import sleep

import undetected_chromedriver.v2 as uc
from lxml import etree
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from chaojiying import Chaojiying_Client

chrome_options = uc.ChromeOptions()
# --禁用扩展
chrome_options.add_argument("--disable-extensions")
# # --禁用弹出窗口阻止
chrome_options.add_argument("--disable-popup-blocking")
# --配置文件目录=默认值
chrome_options.add_argument("--profile-directory=Default")
# --忽略证书错误
chrome_options.add_argument("--ignore-certificate-errors")
# --禁用插件发现
chrome_options.add_argument("--disable-plugins-discovery")
# --隐姓埋名
chrome_options.add_argument("--incognito")
# --没有第一次运行
chrome_options.add_argument('--no-first-run')
# --无服务自动运行
chrome_options.add_argument('--no-service-autorun')
# --无默认浏览器检查
chrome_options.add_argument('--no-default-browser-check')
# --密码存储=基本
chrome_options.add_argument('--password-store=basic')
# --没有沙箱
chrome_options.add_argument('--no-sandbox')


bro = uc.Chrome(version_main=104,use_subprocess=True, options=chrome_options)
# //浏览器最大化，不覆盖任务栏
bro.maximize_window()

bro.get("https://main.m.taobao.com/")
# sleep(20)
# data=bro.page_source
# print(data)
# tree = etree.HTML(data)
# tree.xpath('/html/body/div[1]/div/div/div[2]/div[1]/div[1]/a[1]/img').click()
bro.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/div[1]/a[1]/img').click()


# # bro.find_element(By.XPATH, '//*[@id="fm-login-id"]').send_keys('13178800635')
# # bro.find_element(By.XPATH, '//*[@id="fm-login-password"]').send_keys('swinz1319kfy')
# # bro.find_element(By.XPATH, '//*[@id="login-form"]/div[4]/button').click()

# with open("cookies.txt","r") as f:
#     cookies_list=json.load(f)
#     for cookie in cookies_list:
#         bro.add_cookie(cookie)
# sleep(3)
# with open("cookies.txt","w") as f:
#     f.write(json.dumps(bro.get_cookies()))

# sleep(3)
# bro.refresh()
# sleep(10)
# data=bro.page_source
# tree = etree.HTML(data)
# print(data)
# aa=tree.xpath('//*[@id="J_SiteNavLogin"]/div[1]/div/a/text()')
# print(aa)

sleep(100)











# 亚马逊登陆
# bro.implicitly_wait(30)
# bro.find_element(By.XPATH, '//*[@id="ap_email"]').send_keys('13178800635')
# bro.find_element(By.XPATH, '//*[@id="ap_legal_agreement_check_box"]').click()
# bro.find_element(By.XPATH, '//*[@id="continue"]').click()
# bro.implicitly_wait(30)
# bro.find_element(By.XPATH, '//*[@id="ap_password"]').send_keys('swinz1319kfy')
# bro.find_element(By.XPATH, '//*[@id="signInSubmit"]').click()

# # 验证码操作
# sleep(1)
# bro.find_element(By.XPATH, '//*[@id="ap_password"]').send_keys('swinz1319kfy')
# img = bro.find_element(By.XPATH, '//*[@id="auth-captcha-image"]').screenshot_as_png
# bro.implicitly_wait(30)
# chaojiying = Chaojiying_Client('13178800635', '123456', '938481')
# # 6位验证码类型编号1902
# dic = chaojiying.PostPic(img, 1902)
# verify_code = dic['pic_str']
# print(verify_code)
# for i in verify_code:
#     bro.find_element(By.XPATH, '//*[@id="auth-captcha-guess"]').send_keys(i)
#     # bro.find_element(By.XPATH, '//*[@id="auth-captcha-guess"]').send_keys(Keys.CONTROL + 'a')
#     # bro.find_element(By.XPATH, '//*[@id="auth-captcha-guess"]').send_keys(verify_code)
# bro.find_element(By.XPATH, '//*[@id="auth-captcha-guess"]').send_keys(Keys.BACK_SPACE)
# sleep(10)
# bro.find_element(By.XPATH, '//*[@id="signInSubmit"]').click()




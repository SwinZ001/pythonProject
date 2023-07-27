from time import sleep

from appium import webdriver
from selenium.webdriver.common.by import By

desired_caps = {
    "platformName": "Android",
    "appium:platformVersion": "7.1.2",
    "appium:deviceName": "SM-G955N",
    "appium:appPackage": "com.taobao.taobao",
    "appium:appActivity": "com.taobao.tao.TBMainActivity"
}

server = 'http://localhost:4723/wd/hub'

driver = webdriver.Remote(server,desired_caps)

# w=driver.get_window_size()['width']
# h=driver.get_window_size()['height']
# print(str(w))
driver.implicitly_wait(50)
driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.FrameLayout[3]/android.widget.ImageView[2]').click()


import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By

desired_caps = dict(

    deviceName='Android',
    platformName='Android',
    appPackage='com.android.chrome',
    appActivity='org.chromium.chrome.browser.ChromeTabbedActivity'

)
options = UiAutomator2Options()
options.device_name = 'Android'
options.udid = '54da5eee'
options.app_package = 'com.android.chrome'
options.app_activity = 'org.chromium.chrome.browser.ChromeTabbedActivity'
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
driver.implicitly_wait(10)
time.sleep(10)
driver.get('http://google.com')

contexts = driver.contexts

for context in contexts:
    print(context)

driver.switch_to.context('WEBVIEW_chrome')

time.sleep(1)
driver.find_element(By.XPATH, "//*[@name='q']").send_keys("Hello Appium !!!")
driver.switch_to.context('NATIVE_APP')

time.sleep(2)
driver.quit()

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
driver.get('https://rahulshettyacademy.com/angularAppdemo/')

contexts = driver.contexts

for context in contexts:
    print(context)

driver.switch_to.context('WEBVIEW_chrome')

time.sleep(1)
# driver.find_element(By.XPATH, '//button[@routerlink="/library"]').click()
driver.find_element(By.XPATH, "//span[@class='navbar-toggler-icon']").click()
driver.find_element(By.XPATH, "//a[@href='/angularAppdemo/products']").click()
driver.execute_script("window.scrollBy(0,1000)", "")
txt = driver.find_element(By.CSS_SELECTOR, "a[href*='/products/3']").text
assert "Devops" in txt
driver.find_element(By.CSS_SELECTOR, "a[href*='/products/3']").click()
driver.switch_to.context('NATIVE_APP')

time.sleep(2)
driver.quit()

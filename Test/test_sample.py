from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By

from Src.TestBase.AppiumDriverSetup import WebDriverSetup


class TestHomePage(WebDriverSetup):
    def test_login(self):
        driver = self.driver
        driver.implicitly_wait(60)
        driver.find_element(by=AppiumBy.ID, value='bd.com.upay.customer.uat:id/login_button').click()
        #driver.find_element(by=AppiumBy.ID, value='com.android.permissioncontroller:id/permission_allow_foreground_only_button').click()
        driver.find_element(by=AppiumBy.XPATH, value="//android.widget.EditText[@text='01XXXXXXXXX']").send_keys("01894841467")
        driver.find_element(by=AppiumBy.XPATH, value="//android.widget.EditText[@text='⬤⬤⬤⬤⬤⬤']").send_keys(
            "2580")
        driver.find_element(by=AppiumBy.XPATH, value="(//android.widget.ImageView[@resource-id='bd.com.upay.customer.uat:id/sendButton'])[2]").click()
        sleep(30)
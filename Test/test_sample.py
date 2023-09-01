from time import sleep
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By


@pytest.mark.usefixtures("setup")
class TestHomePage:
    def test_sample(self):
        pass
        sleep(10)

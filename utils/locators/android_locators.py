from selenium.webdriver.common.by import By
from utils.data import TestData


class CommonLocator(object):
    pass


class LoginPageLocator(object):
    COUNTRY_DROPDOWN = (By.ID, "com.androidsample.generalstore:id/spinnerCountry")
    COUNTRY = (By.XPATH, f"//android.widget.TextView[@text='{TestData.COUNTRY}']")
    NAME_FIELD = (By.ID, "com.androidsample.generalstore:id/nameField")
    GENDER = (
        By.XPATH,
        f"//android.widget.RadioButton[@resource-id='com.androidsample.generalstore:id/radio{TestData.GENDER}']")
    LETS_SHOP = (By.ID, "com.androidsample.generalstore:id/btnLetsShop")


class HomePageLocator(object):
    pass

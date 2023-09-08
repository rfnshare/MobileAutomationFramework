from selenium.webdriver.common.by import By
from utils.data import TestData


class CommonLocator(object):
    TOAST_MESSAGE = (By.XPATH, "//android.widget.Toast[1]")
    OK = (By.ID, "android:id/button1")


class LoginPageLocator(object):
    COUNTRY_DROPDOWN = (By.ID, "com.androidsample.generalstore:id/spinnerCountry")
    COUNTRY = (By.XPATH, f"//android.widget.TextView[@text='{TestData.COUNTRY}']")
    NAME_FIELD = (By.ID, "com.androidsample.generalstore:id/nameField")
    GENDER = (
        By.XPATH,
        f"//android.widget.RadioButton[@resource-id='com.androidsample.generalstore:id/radio{TestData.GENDER}']")
    LETS_SHOP = (By.ID, "com.androidsample.generalstore:id/btnLetsShop")


class HomePageLocator(object):
    PRODUCT_ADD_TO_CART = (
        By.XPATH,
        "//android.widget.TextView[@text='{}']/parent::android.widget.LinearLayout//android.widget.TextView["
        "@text='ADD TO CART']")

    CART_BUTTON = (By.ID, "com.androidsample.generalstore:id/appbar_btn_cart")
    CART_TITLE = (By.XPATH, "//android.widget.TextView[@text='Cart']")
    PRODUCT_NAME = (By.ID, "com.androidsample.generalstore:id/productName")
    PRODUCT_PRICE = (By.ID, "com.androidsample.generalstore:id/productPrice")
    TOTAL_AMOUNT = (By.ID, "com.androidsample.generalstore:id/totalAmountLbl")
    TERMS_AND_CONDITIONS_BUTTON = (By.ID, "com.androidsample.generalstore:id/termsButton")
    TERMS_AND_CONDITIONS_BUTTON_TITLE = (By.ID, "com.androidsample.generalstore:id/alertTitle")
    CHECKBOX = (By.CLASS_NAME, "android.widget.CheckBox")
    PROCEED_BUTTON = (By.ID, "com.androidsample.generalstore:id/btnProceed")
    @classmethod
    def product_add_to_cart(cls, product_name):
        return cls.PRODUCT_ADD_TO_CART[1].format(product_name)

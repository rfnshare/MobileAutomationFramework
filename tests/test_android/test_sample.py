import pytest
import allure
from pages.android_pages.home_page import HomePage
from utils.common import get_test_data


@allure.title("Login & Home Page Test")
@pytest.mark.usefixtures("setup")
class TestHomePage:
    @allure.step("test_fill_form")
    @allure.description("Filling Form with different datasets")
    @pytest.mark.regression
    @pytest.mark.parametrize("data", get_test_data("info"))
    def test_fill_form(self, data):
        homepage = HomePage(self.driver)
        homepage.filling_form(data["country"], data["name"], data["gender"])
        homepage.capture_screenshot()

    @allure.step("test_error_msg")
    @allure.description("Filling Form with blank name field")
    @pytest.mark.smoke
    def test_error_msg(self):
        homepage = HomePage(self.driver)
        homepage.validating_blank_name_error_message()
        homepage.capture_screenshot()

    @allure.step("test_shopping")
    @allure.description("Shopping a product & validate cart page")
    @pytest.mark.skip
    def test_shopping(self):
        homepage = HomePage(self.driver)
        homepage.shopping()
        homepage.capture_screenshot()

    @allure.step("test_price_validate")
    @allure.description("Shopping multiple product & validate price cart page")
    @pytest.mark.regression
    @pytest.mark.xfail
    def test_price_validate(self):
        homepage = HomePage(self.driver)
        homepage.validating_cart_price()
        homepage.capture_screenshot()

import pytest

from pages.android_pages.home_page import HomePage
from utils.common import get_test_data


@pytest.mark.usefixtures("setup")
class TestHomePage:
    @pytest.mark.parametrize("data", get_test_data("info"))
    def test_fill_form(self, data):
        homepage = HomePage(self.driver)
        homepage.filling_form(data['country'], data['name'], data['gender'])
        homepage.capture_screenshot()

    def test_error_msg(self):
        homepage = HomePage(self.driver)
        homepage.validating_blank_name_error_message()
        homepage.capture_screenshot()

    def test_shopping(self):
        homepage = HomePage(self.driver)
        homepage.shopping()
        homepage.capture_screenshot()

    def test_price_validate(self):
        homepage = HomePage(self.driver)
        homepage.validating_cart_price()
        homepage.capture_screenshot()
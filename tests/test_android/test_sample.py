import pytest
from pages.android_pages.home_page import HomePage


@pytest.mark.usefixtures("setup")
class TestHomePage:
    def test_fill_form(self):
        homepage = HomePage(self.driver)
        homepage.filling_form()
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
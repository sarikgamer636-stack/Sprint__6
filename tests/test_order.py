import allure
import pytest
import time
from selenium import webdriver
from pages.main_page import MainPage
from pages.order_page import OrderPage
from data.test_data import ORDER_DATA
from urls import BASE_URL, REDIRECT_URL


@allure.epic("Заказ самоката")
@allure.feature("Позитивный сценарий оформления заказа")
class TestOrder:

    @classmethod
    def setup_class(cls):
        options = webdriver.FirefoxOptions()
        options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Firefox(options=options)
        cls.driver.get(BASE_URL)
        cls.main_page = MainPage(cls.driver)
        cls.order_page = OrderPage(cls.driver)
        cls.main_page.accept_cookies()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    @allure.title("Успешный заказ самоката")
    @allure.description("Проверка полного заказа самоката с двух кнопок 'Заказать' входа и разных данных")
    @pytest.mark.parametrize("order_data", ORDER_DATA)
    @pytest.mark.parametrize("entry_point", ["header", "bottom"])
    def test_positive_order_flow(self, order_data, entry_point):
        self.driver.get(BASE_URL)
        self.main_page.accept_cookies()

        with allure.step(f"Переход к заказу через {entry_point}"):
            if entry_point == "header":
                self.main_page.click_order_header()
            else:
                self.main_page.click_order_bottom()
        with allure.step("Заполнение первой формы"):
            self.order_page.fill_first_form(
                order_data["name"],
                order_data["surname"],
                order_data["address"],
                order_data["metro"],
                order_data["phone"]
        )

        with allure.step("Заполнение второй формы"):
            self.order_page.fill_second_form(
                order_data["date"],
                order_data["rental_period"],
                order_data["color"],
                order_data["comment"]
        )

        with allure.step("Проверка успешного создания заказа"):
            assert self.order_page.is_success_modal_displayed(), \
                "Всплывающее окно успеха не появилось"
            assert "Заказ оформлен" in self.order_page.get_success_text()

        self.order_page.close_success_modal()

        with allure.step("Проверка логотипа Самоката"):
            self.main_page.click_scooter_logo()
            assert BASE_URL in self.driver.current_url

        with allure.step("Проверка переадресации при нажатии на Яндекс через редирект"):
            self.main_page.click_yandex_logo()
            self.driver.switch_to.window(self.driver.window_handles[1])
            time.sleep(10)
            assert REDIRECT_URL in self.driver.current_url

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
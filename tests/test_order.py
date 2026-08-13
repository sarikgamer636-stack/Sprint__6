import allure
import pytest
import time
from pages.main_page import MainPage
from pages.order_page import OrderPage
from data.test_data import ORDER_DATA
from urls import BASE_URL, REDIRECT_URL


@allure.epic("Заказ самоката")
@allure.feature("Позитивный сценарий оформления заказа")
class TestOrder:

    @allure.title("Успешный заказ самоката")
    @allure.description("Проверка полного заказа самоката с двух кнопок 'Заказать' входа и разных данных")
    @pytest.mark.parametrize("order_data", ORDER_DATA)
    @pytest.mark.parametrize("entry_point", ["header", "bottom"])
    def test_positive_order_flow(self,driver, order_data, entry_point):

        main_page = MainPage(driver)
        order_page = OrderPage(driver)

        driver.get(BASE_URL)
        main_page.accept_cookies()

        with allure.step(f"Переход к заказу через {entry_point}"):
            if entry_point == "header":
                main_page.click_order_header()
            else:
                main_page.click_order_bottom()
        with allure.step("Заполнение первой формы"):
            order_page.fill_first_form(
                order_data["name"],
                order_data["surname"],
                order_data["address"],
                order_data["metro"],
                order_data["phone"]
        )

        with allure.step("Заполнение второй формы"):
            order_page.fill_second_form(
                order_data["date"],
                order_data["rental_period"],
                order_data["color"],
                order_data["comment"]
        )

        with allure.step("Проверка успешного создания заказа"):
            assert order_page.is_success_modal_displayed(), \
                "Всплывающее окно успеха не появилось"
            assert "Заказ оформлен" in order_page.get_success_text()

        order_page.close_success_modal()

        with allure.step("Проверка логотипа Самоката"):
            main_page.click_scooter_logo()
            assert BASE_URL in main_page.get_current_url()

        with allure.step("Проверка переадресации при нажатии на Яндекс через редирект"):
            main_page.click_yandex_logo()
            main_page.switch_to_new_window()
            time.sleep(30)
            assert REDIRECT_URL in main_page.get_current_url()

        main_page.close_current_window_and_switch_back()
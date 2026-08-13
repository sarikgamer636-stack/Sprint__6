import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class OrderPage(BasePage):

    NAME_INPUT = (By.XPATH, "//input[@placeholder='* Имя']")
    SURNAME_INPUT = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS_INPUT = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_INPUT = (By.XPATH, "//input[@placeholder='* Станция метро']")
    PHONE_INPUT = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")
    DATE_INPUT = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    RENTAL_PERIOD = (By.XPATH, "//div[contains(@class, 'Dropdown-control')]")
    COLOR_BLACK = (By.ID, "black")
    COLOR_GREY = (By.ID, "grey")
    COMMENT_INPUT = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
    ORDER_BUTTON = (By.XPATH, "//div[contains(@class, 'Order_Buttons')]/button[text()='Заказать']")
    CONFIRM_BUTTON = (By.XPATH, "//button[text()='Да']")
    SUCCESS_MODAL = (By.XPATH, "//div[contains(@class, 'Order_ModalHeader')]")
    MODAL_OVERLAY = (By.CLASS_NAME, "Order_Overlay__3KW-T")

    def metro_option(self, station_name: str):
        return (By.XPATH, f"//*[contains(text(), '{station_name}')]")

    def rental_option(self, period: str):
        return (By.XPATH, f"//div[contains(@class, 'Dropdown-option') and text()='{period}']")

    @allure.step("Заполняем первую форму заказа")
    def fill_first_form(self, name, surname, address, metro, phone):
        self.send_keys(self.NAME_INPUT, name)
        self.send_keys(self.SURNAME_INPUT, surname)
        self.send_keys(self.ADDRESS_INPUT, address)

        metro_field = self.find_clickable(self.METRO_INPUT)
        metro_field.click()
        metro_field.clear()
        metro_field.send_keys(metro)

        time.sleep(1)

        option = self.wait.until(
            EC.element_to_be_clickable(self.metro_option(metro))
        )
        option.click()

        self.send_keys(self.PHONE_INPUT, phone)
        self.click(self.NEXT_BUTTON)

    @allure.step("Заполняем вторую форму заказа")
    def fill_second_form(self, date, rental_period, color, comment):
        date_field = self.find_clickable(self.DATE_INPUT)
        date_field.click()
        date_field.clear()
        date_field.send_keys(date)

        date_field.send_keys(Keys.ESCAPE)
        date_field.send_keys(Keys.ENTER)
        self.driver.find_element(By.TAG_NAME, "body").click()

        try:
            self.wait.until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "react-datepicker"))
            )
        except:
            pass

        time.sleep(0.5)

        self.click(self.RENTAL_PERIOD)
        self.click(self.rental_option(rental_period))

        if color == "black":
            self.click(self.COLOR_BLACK)
        else:
            self.click(self.COLOR_GREY)

        self.send_keys(self.COMMENT_INPUT, comment)
        self.click(self.ORDER_BUTTON)
        self.click(self.CONFIRM_BUTTON)

    @allure.step("Проверка отображение всплывающего окна успеха")
    def is_success_modal_displayed(self):
        return self.is_displayed(self.SUCCESS_MODAL)

    @allure.step("Получение текста всплывающего окна успеха")
    def get_success_text(self):
        return self.get_text(self.SUCCESS_MODAL)

    @allure.step("Закрыть всплывающее окно успеха")
    def close_success_modal(self):
        try:
            overlay = self.wait.until(EC.element_to_be_clickable(self.MODAL_OVERLAY))
            overlay.click()
            self.wait.until(EC.invisibility_of_element_located(self.MODAL_OVERLAY))
        except:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
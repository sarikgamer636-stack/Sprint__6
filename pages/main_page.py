import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MainPage(BasePage):

    COOKIE_BUTTON = [By.ID, "rcc-confirm-button"]
    ORDER_BUTTON_HEADER = [By.XPATH, ".//div[contains(@class, 'Header_Nav')]/button[text()='Заказать']"]
    ORDER_BUTTON_BOTTOM = [By.XPATH, "//div[contains(@class, 'Home_FinishButton')]/button[text()='Заказать']"]
    SCOOTER_LOGO = [By.XPATH, "//a[contains(@class, 'Header_LogoScooter')]"]
    YANDEX_LOGO = [By.XPATH, "//a[contains(@class, 'Header_LogoYandex')]"]
    FAQ_QUESTION = [By.ID, "accordion__heading-{}"]
    FAQ_ANSWER = [By.ID, "accordion__panel-{}"]

    @allure.step('Кукииии')
    def accept_cookies(self):
        try:
            self.click(self.COOKIE_BUTTON)
        except:
            pass

    @allure.step('Клик "Заказать" в шапке')
    def click_order_header(self):
        self.click(self.ORDER_BUTTON_HEADER)

    @allure.step('Клик "Заказать" внизу страницы')
    def click_order_bottom(self):
        self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(self.ORDER_BUTTON_BOTTOM))
        self.click(self.ORDER_BUTTON_BOTTOM)

    @allure.step('Клик на FAQ вопрос')
    def click_faq_question(self, index):
        locator = (self.FAQ_QUESTION[0], self.FAQ_QUESTION[1].format(index))
        self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(locator))
        self.click(locator)

    def get_faq_answer_text(self, index):
        locator = (self.FAQ_ANSWER[0], self.FAQ_ANSWER[1].format(index))
        return self.get_text(locator)

    @allure.step('Клик на лого "Самокат"')
    def click_scooter_logo(self):
        slogo = self.find_clickable(self.SCOOTER_LOGO)
        self.driver.execute_script("arguments[0].click();", slogo)

    @allure.step('Клик на лого "Яндекс"')
    def click_yandex_logo(self):
        logo = self.find_clickable(self.YANDEX_LOGO)
        self.driver.execute_script("arguments[0].click();", logo)

    @allure.step("Получаем текущий URL")
    def get_current_url(self):
        return self.driver.current_url

    @allure.step("Переключаемся на новое окно")
    def switch_to_new_window(self):
        self.driver.switch_to.window(self.driver.window_handles[1])

    @allure.step("Закрываем текущее окно и возвращаемся на исходное")
    def close_current_window_and_switch_back(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

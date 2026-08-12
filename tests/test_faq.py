import allure
import pytest
from selenium import webdriver
from pages.main_page import MainPage
from data.test_data import FAQ_DATA

@allure.epic("Главная страница")
@allure.feature("Раздел FAQ (Вопросы о важном)")
class TestFAQ:

    @classmethod
    def setup_class(cls):
        options = webdriver.FirefoxOptions()
        options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Firefox(options=options)
        cls.driver.get("https://qa-scooter.praktikum-services.ru/")
        cls.main_page = MainPage(cls.driver)
        cls.main_page.accept_cookies()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    @allure.title("Проверка ответа в разделе FAQ")
    @allure.description("При клике на вопрос открывается правильный ответ")
    @pytest.mark.parametrize("index, question, expected_answer", FAQ_DATA)
    def test_faq_accordion(self, index, question, expected_answer):
        with allure.step(f"Кликаем на вопрос №{index + 1}"):
            self.main_page.click_faq_question(index)

        with allure.step("Проверяем текст ответа"):
            actual_answer = self.main_page.get_faq_answer_text(index)
            assert expected_answer in actual_answer, \
            f"Ожидался текст: '{expected_answer}', получен: '{actual_answer}'"
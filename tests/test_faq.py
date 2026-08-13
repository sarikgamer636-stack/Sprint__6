import allure
import pytest
from pages.main_page import MainPage
from data.test_data import FAQ_DATA

@allure.epic("Главная страница")
@allure.feature("Раздел FAQ (Вопросы о важном)")
class TestFAQ:

    @allure.title("Проверка ответа в разделе FAQ")
    @allure.description("При клике на вопрос открывается правильный ответ")
    @pytest.mark.parametrize("index, question, expected_answer", FAQ_DATA)
    def test_faq_accordion(self,driver, index, question, expected_answer):
        main_page = MainPage(driver)
        main_page.accept_cookies()

        with allure.step(f"Кликаем на вопрос №{index + 1}"):
            main_page.click_faq_question(index)

        with allure.step("Проверяем текст ответа"):
            actual_answer = main_page.get_faq_answer_text(index)
            assert expected_answer in actual_answer, \
            f"Ожидался текст: '{expected_answer}', получен: '{actual_answer}'"
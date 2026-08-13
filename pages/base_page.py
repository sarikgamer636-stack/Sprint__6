import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Поиск элемента")
    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    @allure.step("Поиск кликабельного элемента")
    def find_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    @allure.step("Клик по элементу")
    def click(self, locator):
        self.find_clickable(locator).click()

    @allure.step("Ввод текста в поле")
    def send_keys(self, locator, text):
        element = self.find_clickable(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Проверка, что элемент отображается")
    def is_displayed(self, locator):
        try:
            return self.find_element(locator).is_displayed()
        except:
            return False

    @allure.step("Получение текста элемента")
    def get_text(self, locator):
        return self.find_element(locator).text
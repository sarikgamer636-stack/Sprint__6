import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from urls import BASE_URL


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Firefox(options=options)
    driver.get(BASE_URL)
    yield driver
    driver.quit()

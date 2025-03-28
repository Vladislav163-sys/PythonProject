from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pytesseract
from PIL import Image

# Инициализация драйвера
driver = webdriver.Chrome()  # Убедитесь, что у вас установлен ChromeDriver
driver.get("https://b2c.passport.rt.ru/auth")
driver.set_window_size(1920, 1080)
driver.implicitly_wait(10)

def test_password_recovery():
    # Тест-кейс 1: Выбор метода восстановления
    driver.find_element(By.LINK_TEXT, "Забыл пароль").click()
    driver.find_element(By.ID, 't-btn-tab-mail').click()
    driver.find_element(By.ID, "username").send_keys("user@example.com")  # Замените на тестовый e-mail
    assert "Электронная почта" in driver.page_source  # Проверка отображения формы

    # Тест-кейс 2: Отправка кода на e-mail
    driver.find_element(By.ID, "username").send_keys(Keys.RETURN)
    time.sleep(2)  # Ждем отправки кода
    assert "Восстановление пароля" in driver.page_source  # Проверка отправки кода

    # Тест-кейс 3: Ввод правильного кода
    driver.find_element(By.NAME, "code").send_keys("123456")  # Замените на правильный код
    assert "Введите новый пароль" in driver.page_source  # Проверка перехода к вводу нового пароля

    # Тест-кейс 4: Ввод неверного кода
    driver.find_element(By.NAME, "code").send_keys("wrong_code")
    assert "Неверный код. Повторите попытку" in driver.page_source  # Проверка сообщения об ошибке

    # Тест-кейс 5: Время жизни кода истекло
    driver.find_element(By.NAME, "code").send_keys("expired_code")  # Код, который истек
    assert "Время жизни кода истекло" in driver.page_source  # Проверка сообщения об ошибке

    # Тест-кейс 6: Ограничение на ввод только цифр
    driver.find_element(By.NAME, "code").send_keys("abc123")
    assert "Неверный код. Код должен состоять только из цифр" in driver.page_source  # Проверка сообщения об ошибке

    # Тест-кейс 7: Ввод нового пароля с неправильными правилами
    driver.find_element(By.NAME, "new_password").send_keys("123")
    driver.find_element(By.NAME, "submit").click()
    assert "Пароль должен содержать не менее 8 символов" in driver.page_source  # Проверка сообщения об ошибке

    # Тест-кейс 8: Проверка уникальности нового пароля
    driver.find_element(By.NAME, "new_password").send_keys("previous_password")  # Замените на предыдущий пароль
    driver.find_element(By.NAME, "submit").click()
    assert "Пароль не должен совпадать с предыдущими" in driver.page_source  # Проверка сообщения об ошибке

def test_registration():
    # Тест-кейс 9: Переход на страницу регистрации
    driver.find_element(By.LINK_TEXT, "Зарегистрироваться").click()
    assert "Регистрация" in driver.page_source  # Проверка перехода на страницу регистрации

    # Тест-кейс 10: Проверка полей формы регистрации
    driver.find_element(By.NAME, "name").send_keys("Имя")
    driver.find_element(By.NAME, "surname").send_keys("Фамилия")
    driver.find_element(By.NAME, "email").send_keys("user@example.com")
    driver.find_element(By.NAME, "phone").send_keys("1234567890")
    driver.find_element(By.NAME, "password").send_keys("password777")
    driver.find_element(By.NAME, "submit").click()
    assert "Подтверждение" in driver.page_source  # Проверка перехода к следующему шагу

    # Тест-кейс 11: Проверка формата e-mail
    driver.find_element(By.NAME, "email").send_keys("invalid_email")
    driver.find_element(By.NAME, "submit").click()
    assert "Некорректный e-mail" in driver.page_source  # Проверка сообщения об ошибке

    # Тест-кейс 12: Проверка уникальности e-mail
    driver.find_element(By.NAME, "email").send_keys("existing_user@example.com")  # Замените на существующий e-mail
    driver.find_element(By.NAME, "submit").click()
    assert "E-mail уже привязан к учетной записи" in driver.page_source  # Проверка сообщения об ошибке

def test_authorization():
    # Тест-кейс 14: Проверка наличия файлов cookie
    driver.delete_all_cookies()  # Убедитесь, что cookies отключены
    driver.find_element(By.ID, "username").send_keys("user@example.com")  # Замените на тестовый e-mail
    driver.find_element(By.ID, "password").send_keys("password777")
    driver.find_element(By.NAME, "submit").click()
    assert "Пожалуйста, включите cookies для продолжения" in driver.page_source  # Проверка сообщения об ошибке

    # Тест-кейс 15: Проверка атрибутов форм в зависимости от продукта
    driver.find_element(By.LINK_TEXT, "ЕЛК Web").click()  # Выбор продукта
    assert "атрибут1" in driver.page_source  # Проверка наличия атрибутов формы

# Запуск тестов
try:
    test_password_recovery()
    test_registration()
    test_authorization()
finally:
    driver.quit()  # Закрытие браузера
from env_stash import TXT_FILE
import time

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from letter import entrypoint_letter


def try_to_apply(driver, curr_post_link, our_letter, original_window) -> bool:
    """
    Confirms appliance and sends letter
    # Может уже быть нажата!!! Обработать
    """
    # тут надо обработать "уже откликнулся"
    try:
        apply = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'bloko-button_kind-success')))
        apply.click()

        letter_trig = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-qa='vacancy-response-letter-toggle']"))
        )
        letter_trig.click()

        time.sleep(1)

        letter_textarea = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[contains(@placeholder, 'Напишите, почему')]"))
        )
        letter_textarea.send_keys(our_letter)
        time.sleep(1)

        submit_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-qa='vacancy-response-letter-submit']"))
        )
        submit_button.click()

        return True

    except TimeoutException:
        """Если не прямой аплай"""
        textarea = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@data-qa='vacancy-response-popup-form-letter-input']"))
        )
        textarea.send_keys(our_letter)

        response_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[span[text()='Откликнуться']]"))
        )
        response_button.click()
        # submit_button(driver=driver)

        if len(driver.find_elements(By.CLASS_NAME, '-form-')) != 2:
            check = input("Check if everything is correct, we doubt if form was submitted.\nIf you want not to finish test, press `l`, and we will write down this post link and your letter in txt file for you.\n")
            if check == 'l':
                write_to_our_file(curr_post_link, our_letter)
            return True
    except NoSuchElementException:
        input('No element found. Idk what to do. Go debug.')
        return True
    finally:
        if original_window in driver.window_handles:
            driver.close()
            # Переключение обратно на оригинальную вкладку
            driver.switch_to.window(original_window)


def post_logic(driver: WebDriver, original_window, curr_post_link: str) -> bool:
    """Handelds logic inside the post tab"""
    try:
        preparation(driver=driver, curr_post_link=curr_post_link, original_window=original_window)

        # if not input("`Enter` to skip, any other chars to apply\n"):
        # #  Коменты для ответа на всё
        #     driver.close()
        #     driver.switch_to.window(original_window)
        #     return False

        our_letter = """Добрый день!\n\nПрочитал описание Вашей вакансии, отдельное спасибо составлителю за чёткое и понятное изложение.\n
        Понравились Ваши цели и достижения, мне было бы интересно у Вас работать. Обладаю 2х летним опытом в Питоне и окружении вокруг него(Django, FastAPI, ORMs, SQL/NoSQL, Docker, Celery и тд, так что уверен, что и с Вами найдем общий язык)\n\nБуду рад продолжить общение,\nСпасибо)"""
        # our_letter = entrypoint_letter.main()

        try:
            res = try_to_apply(driver=driver, curr_post_link=curr_post_link, our_letter=our_letter,
                               original_window=original_window)
            if res:
                return True
        except Exception as e:
            write_to_our_file(curr_post_link, e)
            # write_to_our_file(curr_post_link, our_letter)

        return False
    except Exception as e:
        print(e)
        driver.close()
        driver.switch_to.window(original_window)
        return False


def ready_to_use(driver: WebDriver, original_window):
    """Логика прохода по контейнерам вакансий в поиске"""
    is_any_left = True
    number_of_posts = 0
    time.sleep(2)

    elements = driver.find_elements(By.CLASS_NAME, 'bloko-header-section-2')
    while is_any_left:
        for element in elements:
            link = element.find_element(By.TAG_NAME, "a").get_attribute("href")

            res = post_logic(driver=driver, curr_post_link=link, original_window=original_window)

            if res:
                number_of_posts += 1

        # Где-то надо обработать логику конца неотвеченых вакансий
        break

    return number_of_posts, is_any_left

    # while is_any_left:
    # post_link = driver.find_element(By.XPATH, '//*[@id="a11y-main-content"]/div[2]/div/div/div/h2/span/a')
    # post_link_class = driver.find_element(By.CLASS_NAME, 'vacancy-search-item__card')
    # post_link = (driver.find_element(By.XPATH, '//*[@id="a11y-main-content"]/div[2]/div/div/div/h2/span/a')
    #              .get_attribute('href'))
    # if not post_link:
    #     break
    #
    # res = reply_on_post(driver, post_link, original_window, curr_wait)
    #
    # if res:
    #     number_of_posts += 1


def preparation(driver, original_window, curr_post_link):
    driver.execute_script("window.open('');")
    WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))

    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break

    driver.get(curr_post_link)


def write_to_our_file(curr_post_link, our_letter):
    with open(TXT_FILE, 'a', encoding='utf-8') as file:
        file.write(f"Link: {curr_post_link}\n")
        file.write(f"Letter: {our_letter}\n")
        file.write("-" * 40 + "\n")  # Разделитель для читаемости


def submit_button(driver: WebDriver):
    try:
        submit_response = driver.find_element(By.XPATH, "//button[data-qa='vacancy-response-submit-popup']")
        print("Found vacancy-response-submit-popup")
    except NoSuchElementException:
        submit_response = None
        print("vacancy-response-popup-close-button not found")

    # Если первый элемент не найден, пытаемся найти второй элемент
    if submit_response is None:
        try:
            submit_response = driver.find_element(By.XPATH, "//button[data-qa='vacancy-response-popup-close-button'")
            print("Found vacancy-response-popup-close-button")
        except NoSuchElementException:
            submit_response = None
            print("vacancy-response-submit-popup not found")

    # Проверяем, был ли найден какой-либо элемент, и выполняем клик
    if submit_response:
        submit_response.click()
        print("Submit button clicked")
    else:
        print("No submit button found")

# Вариант когда не найдет textarea. Я не помню, что это за случай
#
# if textarea:
#     our_letter = main()
#     textarea.send_keys(our_letter)
#     driver.find_element(By.CSS_SELECTOR, "button[data-qa='vacancy-response-letter-submit']").click()
# else:
#     driver.find_element(By.XPATH, '//*[@id="HH-React-Root"]/div/div/div[3]/div['
#                                   '1]/div/div/div/div/div/div[4]/div/div/div[4]/div/div['
#                                   '1]/div/div/div[8]/button').click()
#     driver.find_element(By.XPATH, '')
#
#     letter = main()
#
#     driver.find_element(By.XPATH, '//*[@id="HH-React-Root"]/div/div/div[3]/div[1]/div/div/div/div/div/div['
#                                   '4]/div/div/div[4]/div/div[1]/div/div/div[8]/form/textarea').send_keys(letter)
#     driver.find_element(By.XPATH, '//*[@id="HH-React-Root"]/div/div/div[3]/div[1]/div/div/div/div/div/div['
#                                   '4]/div/div/div[4]/div/div[1]/div/div/div[10]/form/div/button').click()



# <button class="bloko-button bloko-button_kind-primary"
# type="submit" data-qa="vacancy-response-letter-submit"><span>Отправить</span></button>




# def try_to_apply(driver, curr_post_link, our_letter, original_window) -> bool:
#     """
#     Confirms appliance and sends letter
#     # Может уже быть нажата!!! Обработать
#     """
#
#     apply = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'bloko-button_kind-success')))
#     apply.click()
#     # тут надо обработать "уже откликнулся"
#     try:
#         letter_trig = WebDriverWait(driver, 5).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-qa='vacancy-response-letter-toggle']"))
#         )
#         letter_trig.click()
#
#         time.sleep(1)
#
#         driver.find_element(By.XPATH, "//textarea[contains(@placeholder, 'Напишите, почему')]").send_keys(our_letter)
#         time.sleep(1)
#
#
#         button = WebDriverWait(driver, 5).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-qa='vacancy-response-letter-submit']"))
#         )
#         button.click()
#
#         return True
#
#     except TimeoutException:
#         """Если не прямой аплай"""
#         textarea = WebDriverWait(driver, 5).until(
#             EC.presence_of_element_located((By.XPATH, "//textarea[@data-qa='vacancy-response-popup-form-letter-input']"))
#             )
#
#         textarea.send_keys(our_letter)
#
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//button[span[text()='Откликнуться']]"))
#         ).click()
#         # submit_button(driver=driver)
#
#         if driver.find_elements(By.CLASS_NAME, '-form-') != 2:
#             check = str(input("Check if everything is correct, we doubt if form was submitted.\nIf you want not to finish test, press `l`, and we will write down this post link and your letter in txt file for you.\n"))
#             if check == 'l':
#                 write_to_our_file(curr_post_link, our_letter)
#             return True
#     except NoSuchElementException:
#         input('No element found. Idk what to do. Go debug.')
#         return True
#     finally:
#         if original_window in driver.window_handles:
#             driver.close()
#             # Переключение обратно на оригинальную вкладку
#             driver.switch_to.window(original_window)
# # Почему-то не нажимается написать сопровод
#         # driver.switch_to.window(original_window)

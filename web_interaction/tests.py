import time

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from driver_utils import setUp

# LINK_here = 'https://hh.ru/vacancy/103352647?query=javascript&hhtmFrom=vacancy_search_list'
# LINK_switch = 'https://hh.ru/vacancy/94554590?hhtmFrom=vacancy_response'
# LINK_usual = 'https://hh.ru/vacancy/103506626?query=javascript+next&hhtmFrom=vacancy_search_list'
# SOME_LINK = 'https://hh.ru/vacancy/102802836?utm_medium=cpc_hh&utm_source=clickmehhru&utm_campaign=593938&utm_local_campaign=971181&utm_content=630367'


# def main():
#     driver = setUp()
#
#     driver.get(SOME_LINK)
#
#     try:
#         #         # click_link = WebDriverWait(driver, 5).until(
#         #         #     EC.presence_of_element_located((By.CLASS_NAME, 'bloko-button_kind-success'))
#         #         # )
#         #         # print(f"Click link is here {click_link}")
#         #         # click_link.click()
#         #
#         #
#         soprovod_usual = WebDriverWait(driver, 5).until(By.XPATH, "//button[span[text()='Написать сопроводительное'")
#
#         soprovod_usual_css = WebDriverWait(driver, 2).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-qa='vacancy-response-letter-toggle']"))
#         )
#         print(f"Сопровод {soprovod_usual_css}")
#
#         #         # soprovod_usual_XPATH = WebDriverWait(driver, 2).until(
#         #         #     EC.presence_of_element_located((By.XPATH, '//*[@id="HH-React-Root"]/div/div/div[3]/div[1]/div/div/div/div/div/div[4]/div/div[5]/div/div[1]/div/div/div[10]/button'))
#         #         # )
#         #         # print(f"Сопровод {soprovod_usual_XPATH}")
#         #
#         #         # soprovod_usual_CSS_CLASSNAME = WebDriverWait(driver, 2).until(
#         #         #     EC.presence_of_element_located((By.CSS_SELECTOR, "vacancy-response-letter-toggle"))
#         #         # )
#         #         # print(f"Сопровод {soprovod_usual}")
#         #
#         soprovod_usual_css.click()
#         #
#         #
#         #
#         #
#         #
#         time.sleep(1)
#         #
#         #
#         #
#         #
#         textarea_usual = driver.find_element(By.XPATH, "//textarea[contains(@placeholder, 'Напишите, почему')]")
#         textarea_usual.send_keys("Спасибо")
#         #
#         #         # textarea_second_both = WebDriverWait(driver, 5).until(
#         #         #     EC.presence_of_element_located((By.XPATH, "//textarea[@data-qa='vacancy-response-popup-form-letter-input']"))
#         #         #     )
#         #         # textarea_second_both.send_keys("Спасибо")
#         time.sleep(1)
#         #
#         #
#         submit_response_usual = driver.find_element(By.CSS_SELECTOR, "button[data-qa='vacancy-response-letter-submit']")
#         #
#         #
#         #         # submit_response_for_form_right_away = WebDriverWait(driver, 10).until(
#         #         #     EC.presence_of_element_located((By.XPATH, "//button[span[text()='Откликнуться']]"))
#         #         # )  ЭТОТ РАБОТАЕТ
#         #         # print(submit_response_for_form_right_away)
#         #
#         #
#         print(submit_response_usual)
#         #
#         #
#         return True
#     #
#     except TimeoutException:
#         """Если не прямой аплай"""
#         textarea = WebDriverWait(driver, 5).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, "//textarea[@data-qa='vacancy-response-popup-form-letter-input']"))
#         )
#         if driver.find_elements(By.CLASS_NAME, '-form-') != 2:
#             print("Not 2")
#     except NoSuchElementException:
#         input('No element found. Idk what to do. Go debug.')
#         return True
#     finally:
#         driver.close()
#
#
# main()

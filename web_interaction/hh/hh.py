from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from selenium.webdriver.remote.webdriver import WebDriver

from web_interaction.hh.hh_post import ready_to_use
from web_interaction.driver_utils import setUp, establish_connection, scroll_page

TOTAL_COUNT = 0
DRIVER = None


def hh_entrypoint() -> bool:
    """Main hh script."""
    driver = DRIVER

    try:
        driver = setUp()
        wait = establish_connection(driver=driver)
        original_window = driver.current_window_handle

        input(
            "Are you satisfied with the search?\nIf not change filters or query in browser\nPress `Enter` to commit\n"
        )
        original_link = driver.current_url

        go(driver, original_window, original_link, wait)

        return True

    except Exception as e:
        print("Произошла ошибка:", e)
        return False
    finally:
        if isinstance(driver, WebDriver):
            driver.quit()


def go(driver, original_window, initial_link, wait) -> int:
    """Логика от инициации страницы поиска до работы внутри поста, включая перелистывание"""
    total_count = TOTAL_COUNT
    curr_link = initial_link
    is_more = True

    while is_more:
        scroll_page(driver)
        count, is_more = ready_to_use(driver, original_window)

        print(f"Мы ответили на {count} вакансий на этой странице")
        total_count += count

        curr_link = get_flipped_link(curr_link)
        if is_more:
            driver.get(curr_link)

    print(f"За этот прогон мы ответили суммарно на {total_count} вакансий")

    return total_count


def get_flipped_link(link):
    """if page -> +1, else page=1"""

    # Разбираем URL на компоненты
    url_parts = urlparse(link)
    query_params = parse_qs(url_parts.query)

    # Проверяем, есть ли параметр страницы в URL
    if "page" in query_params:
        # Увеличиваем номер страницы на 1
        current_page = int(query_params["page"][0])
        query_params["page"] = str(current_page + 1)
    else:
        # Если параметра страницы нет, добавляем его с начальным значением 1
        query_params["page"] = "1"

    # Собираем новый URL
    new_query = urlencode(query_params, doseq=True)
    new_url_parts = list(url_parts)
    new_url_parts[4] = new_query
    new_url = urlunparse(new_url_parts)

    return new_url

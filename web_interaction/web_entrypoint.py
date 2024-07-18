import logging

import web_interaction.hh.hh as hh
import web_interaction.linkedIn as linkedIn
from web_interaction.telega.telegram import telegram_entrypoint

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


def main(web_type: int = 2) -> None:
    try:
        match web_type:
            case 1:
                channel = int(input("Give the chat id\n"))
                telegram_entrypoint(channel=channel)
            case 2:
                hh.hh_entrypoint()
            case 3:
                linkedIn.linkedin_entrypoint()
            case _:
                print("None")
    except KeyboardInterrupt:
        if hh.DRIVER:
            print(f"У нас есть драйвер")
            hh.DRIVER.quit()
        print(f"Вы прервали выполнение.\nМы откликнулись на {hh.TOTAL_COUNT} вакансий.")


if __name__ == "main":
    main()

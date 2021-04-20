import schedule

from mypythia.scheduler.tools import load_config, process_message


def place_requests() -> None:
    for info in load_config():
        process_message(info)


schedule.every(60).seconds.do(place_requests)

while True:
    schedule.run_pending()

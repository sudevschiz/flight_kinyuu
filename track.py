import requests
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
from time import sleep
import datetime

AIR_LAB_API_KEY = ""
FLIGHT_IATA = "UL127"
BOT_TOKEN = ""
CHAT_ID = ""


def prepare_message(api_response):
    # convert updated time from unix timestamp
    ts = api_response["response"][0]["updated"]
    update_time = datetime.datetime.utcfromtimestamp(ts)
    # Convert to IST
    update_time = update_time + datetime.timedelta(hours=5, minutes=30)
    update_time = update_time.strftime("%Y-%m-%d %H:%M:%S")

    info = f"""
    Status: {api_response['response'][0]['status']}
    Latitude: {api_response['response'][0]['lat']}
    Longitude: {api_response['response'][0]['lng']}
    Speed: {api_response['response'][0]['speed']}
    Altitude: {api_response['response'][0]['alt']}
    Direction: {api_response['response'][0]['dir']}
    Updated: {update_time} IST
    """
    return info


def get_flight_info():
    params = {"api_key": AIR_LAB_API_KEY, "flight_iata": FLIGHT_IATA}
    method = "flights"
    api_base = "http://airlabs.co/api/v9/"
    api_result = requests.get(api_base + method, params)
    api_response = api_result.json()
    # print(api_response)

    try:
        info = prepare_message()
    except:
        info = "No data available"
    return info


def send_message():
    info = get_flight_info()
    updater = Updater(BOT_TOKEN, use_context=True)
    updater.bot.send_message(chat_id=CHAT_ID, text=info)
    updater.stop()


def main():
    """
    Send message to the group every 5 minutes
    """
    while 1:
        send_message()
        sleep(300)


if __name__ == "__main__":
    main()

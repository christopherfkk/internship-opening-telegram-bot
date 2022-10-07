import requests
import time
import schedule
from bs4 import BeautifulSoup
import os


def send_text(message):
    # Define parameters
    bot_token = os.environ['TELEGRAM BOT TOKEN']
    my_chat_id = os.environ['TELEGRAM CHAT ID']
    parse_mode = 'Markdown'

    # Assemble URL
    url = (
        f'https://api.telegram.org/bot{bot_token}/'
        f'sendMessage?chat_id={my_chat_id}&parse_mode={parse_mode}&text={message}'
    )

    response = requests.get(url)
    return response.json()


def check_meta_opening():
    # Search meta jobs with filter intern
    url = "https://www.metacareers.com/jobs?q=intern&roles=intern"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find "There are currently no open opportunities, please check back soon!"
    if soup.find("div", {"class": "_6b80"}):
        no_opening_text = soup.find("div", {"class": "_6b80"}).text
        msg = (
            f'Don\'t think Meta posted any internship postings today:\n'
            f'Found: "{no_opening_text}"'
        )
    else:
        msg = (
            f'Maybe Meta posted internship postings today!:\n'
            f'Check: "{url}"'
        )
    send_text(msg)


# schedule.every().day.at("15:00").do(check_meta_opening)
# schedule.every(2).minutes.do(check_meta_opening)

if __name__ == '__main__':
    check_meta_opening()
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

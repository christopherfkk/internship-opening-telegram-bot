import os
import requests
from bs4 import BeautifulSoup
import time
import schedule


def send_text(message: str) -> None:
    
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
    assert response.status_code == 200
    return


def check_meta_opening() -> None:
                                      
    # Search meta jobs with filter on "intern"
    meta_url = "https://www.metacareers.com/jobs?q=intern&roles=intern"
    response = requests.get(meta_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the text: "There are currently no open opportunities, please check back soon!"
    no_opening_ele = soup.find("div", {"class": "_6b80"})
    if no_opening_ele: # get class from browser inspect console
                                      
        msg = (
            f'I think Meta\'s internships are still closed today. Found:\n\n'
            f'`{no_opening_ele.text}`'
        )
                                      
    else:
                                      
        msg = (
            f'Maybe Meta posted internship openings today! Check:\n\n'
            f'{meta_url}'
        )
    
    # Send a correct message to me
    send_text(msg)
    return

# # Uncomment this if run on cloud  
# schedule.every().day.at("15:00").do(check_meta_opening)

if __name__ == '__main__':
                                      
    # Run using Window's built-in Task Scheduler
    check_meta_opening()
                                      
    # # Uncommment this if run on cloud
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

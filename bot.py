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


def check_opening(company: str, opening_url: str, no_opening_ele_id: str, no_opening_ele_type: str) -> None:
                                      
    # Search meta jobs with filter on "intern"
    response = requests.get(opening_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the text: "There are currently no open opportunities, please check back soon!"
    no_opening_ele = soup.find(f"{no_opening_ele_type}", {"class": f"{no_opening_ele_id}"})
    print(no_opening_ele)
    if no_opening_ele: # get class from browser inspect console
                                      
        msg = (
            f'I think {company.upper()}\'s internships are still closed today. Found:\n\n'
            f'`{no_opening_ele.text}`'
        )
                                      
    else:
                                      
        msg = (
            f'Maybe {company.upper()} posted internship openings today! Check:\n\n'
            f'{opening_url}'
        )
    
    # Send a correct message to me
    send_text(msg)
    return

# # Uncomment this if run on cloud  
# schedule.every().day.at("15:00").do(check_meta_opening)


if __name__ == '__main__':
                                      
    # Run using Window's built-in Task Scheduler
    check_opening("meta", "https://www.metacareers.com/jobs?q=intern&roles=intern", "_6b80", "div")
    check_opening("duolingo", "https://careers.duolingo.com/?type=Intern&department=Software+Engineering", "F_CHk", "p")

    # # Uncommment this if run on cloud
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

import email
import imaplib
import re
import time
from email.header import decode_header

from decouple import config

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.google.com"


class ClickAutomation:
    def __init__(self):
        s = Service(ChromeDriverManager().install())
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        # keep chrome open
        # self.options.add_experimental_option("detach", True)
        self.options.add_experimental_option(
            "excludeSwitches",
            ['enable-logging'])
        self.driver = webdriver.Chrome(
            options=self.options,
            service=s)
        self.driver.implicitly_wait(50)

        self.collection = []
        super(ClickAutomation, self).__init__()

    def __enter__(self):
        self.driver.get(BASE_URL)

    def submit_form(self, url):
        self.driver.get(url)
        self.driver.find_element(by=By.CSS_SELECTOR, value='input[value="Confirm"]').click()
        print("clicked button")


def email_login():
    # account credentials
    username = config("MAIL")
    password = config("PASSWORD")

    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    imap.login(username, password)
    return imap


def checkmail(imap):
    # select the mailbox I want to delete in
    # if you want SPAM, use imap.select("SPAM") instead
    imap.select("INBOX")

    # search for specific mails by sender and subject
    # Could be ALL , UNSEEN ...
    search_query = 'FROM "forwarding-noreply@google.com" UNSEEN'
    status, messages = imap.search(None, search_query)

    messages = messages[0].split(b' ')
    links = []
    for mail in messages:
        if mail:
            _, msg = imap.fetch(mail, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject = decode_header(msg["Subject"])[0][0]

                    if isinstance(subject, bytes):
                        subject = subject.decode()

                    # Extract the link using regular expressions
                    content = msg.get_payload()
                    link_match = re.search(r"(https://mail-settings\.google\.com/mail/vf-.*?)\n", content)
                    if link_match:
                        link = link_match.group(1)
                        print("Opening link:", link)
                        links.append(link)

    return links


# initialize the class
bot = ClickAutomation()
# login the mail
imap = email_login()
while True:

    # check email
    links = checkmail(imap)
    # loop through all the unseen links
    for link in links:
        try:
            #  submit the form
            bot.submit_form(link)
            print("Done. \n Clicking .....")
        except Exception as a:
            print(a)
        print("Waiting for 10 seconds...")
        time.sleep(10)
    time.sleep(15)

# close the mailbox
imap.close()

# logout from the account
imap.logout()

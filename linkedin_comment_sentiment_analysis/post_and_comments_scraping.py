from linkedin_post_scraper_with_python import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import csv
from textblob import TextBlob

import time

def loginAndGetData(): 
    # Set up the Selenium webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--allow-cross-origin-auth-prompt')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')    
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_extension('/Users/emmanuelaudu/Library/Application Support/Google/Chrome/Default/Extensions/ggmdpepbjljkkkdaklfihhngmmgmpggp/2.0_0.crx')
    prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome('/chromedriver', options=options)
    driver.get('https://www.linkedin.com/login')

    wait = WebDriverWait(driver, 50)

    # Enter login information and submit
    username = driver.find_element(By.ID, 'username')
    password = driver.find_element(By.ID, 'password')
    username.send_keys("kole.audu@gmail.com")
    password.send_keys("Janeoluchi1")
    password.send_keys(Keys.RETURN)

    # wait = WebDriverWait(driver,60)
    # xpath = """
    #     //h3[contains(text(), "Let's do a quick security check")]
    # """
    # wait.until(EC.presence_of_element_located((By.XPATH, xpath)))    
    # home_children_button = driver.find_element(By.ID, 'home_children_button')
    
    # time.sleep(1)
    # home_children_button.click()


    # Wait for the login to complete and navigate to the page to scrape
    wait = WebDriverWait(driver, 50)
    wait.until(EC.presence_of_element_located((By.ID, 'global-nav-typeahead')))
    driver.get('https://www.linkedin.com/company/ezoperations/posts/?feedView=all')

    # Wait for the page to load and retrieve the page source
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    # time.sleep(5)

    # time.sleep(2)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    time.sleep(1)

    comment_buttons =  driver.find_elements(By.XPATH, "//li[contains(@class, 'social-details-social-counts__comments')]")

# Scroll down the page while looking for comment buttons
   # Scroll down to the bottom of the page
    actions = ActionChains(driver)

    last_height = driver.execute_script("return document.body.scrollHeight")
    # move the cursor to the button and click it
    counter = 0
    while True:
        # just to reduce presentation time
        counter += 1
        if(counter == 4):
            break
        # Scroll to the bottom of the page
        body = driver.find_element(By.TAG_NAME, "body")
        time.sleep(1)
        body.send_keys(Keys.END)

        # driver.execute_script("window.scrollBy(0, document.body.scrollHeight/3);")

        time.sleep(1)
        
        # Check if we have any new comment buttons
        print(" I just scrolled again");

        new_comment_buttons =  driver.find_elements(By.XPATH, "//li[contains(@class, 'social-details-social-counts__comments')]")

        # if(len(new_comment_buttons)):
        #     print(new_comment_buttons[len(new_comment_buttons) - 1].get_attribute("outerHTML"))

        time.sleep(1)

        if len(new_comment_buttons) > len(comment_buttons):
            comment_buttons = new_comment_buttons

        scroll_height = driver.execute_script("return document.body.scrollHeight")
        if scroll_height == last_height:
            break
        last_height = scroll_height

            

    print("I'm done with the scrolling now")

    comments = []
    counter = 0
    for button in comment_buttons:

        counter += 1

        if(counter == 2):
            break
        actions.move_to_element(button).perform()
        time.sleep(2)
        parent_div = button.find_element(By.XPATH, "./ancestor::div[contains(@class, 'social-details-social-activity')][contains(@class, 'update-v2-social-activity')]")
        time.sleep(1)
        b = button.find_element(By.TAG_NAME, "button")
        print(parent_div.get_attribute("outerHTML"))

        time.sleep(2)

        b.click()
        time.sleep(1)
        comment_span = parent_div.find_element(By.XPATH, "//span[contains(@class, 'comments-comment-item__main-content feed-shared-main-content--comment t-14 t-black t-normal')]")
        time.sleep(1)
        comment = comment_span.find_element(By.XPATH, ".//span").text
        comments.append(comment);
        print("comment: ")
        print(comment)

    # for the presentation alone, take out after
    if(len(comments) > 1):
        comment = comments[0]
    else:
        comment = "So excited to be pafrt of such an amazing team. Thank you."
    

    blob = TextBlob(comment)
    sentiment_score = blob.sentiment.polarity
    sentiment_feeling = ""
    if sentiment_score > 0:
        sentiment_feeling = 'Positive'
    elif sentiment_score < 0:
        sentiment_feeling = 'Negative'
    else:
        sentiment_feeling = 'Neutral'

    # Save data to CSV file
    with open('comments.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['comment','sentiment_score','sentiment'])
        writer.writerow([comment,str(sentiment_score),sentiment_feeling] )

    # time.sleep(2)
    driver.quit()

    print("Thank you for listening to this. :D")

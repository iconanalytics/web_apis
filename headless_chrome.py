from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException as SelenimumTimeout

import requests
import time



class HeadlessChrome():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('user-data-dir=C:\\Users\\charles.fawole\\AppData\\Local\\Google\\Chrome\\User Data\\Default') #use my browser cookies to log into webpage
        self.driver = webdriver.Chrome(options=chrome_options)  # Optional argument, if not specified will search path.


    def close_browser(self):
        self.driver.quit()

    def get_page_source(self):
         page_source = (self.driver.page_source)
         return page_source

    def get_page(self, url):
         return self.driver.get(url)

    def close_browser(self):
        self.driver.quit()

    def scroll_page(self,n_times = 1,sleep_time=0):
        for i in range(n_times):
            time.sleep(sleep_time)
            print("scrolling...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #scoll probaly causes overlap in scraped record. Not scolling enough, it seems

    def create_element_by_xpath(self,xpath,timeout):
        web_element  = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath)))

        return web_element
        
    
    def post_deprecated(self):  #this is a legacy method do not call it,
        #time.sleep(10)

        create_post_button_xpath = '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div[1]/div[1]/div/div/div/div[1]/div'

        create_post_button = self.create_element_by_xpath(create_post_button_xpath,30)
        #create_post_button  = WebDriverWait(self.driver, 30).until(
        #    EC.presence_of_all_elements_located((By.XPATH, create_post_button_xpath)))

        #create_post_button = self.driver.find_elements_by_xpath(create_post_button_xpath)
        create_post_button = create_post_button[0]
        create_post_button.click()

        #time.sleep(10)
        #IMPORTANT: Send URL before sending text
        #post_textbox_xpath = '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/form/div/div/div/div/div/div[1]/div/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div'
        #post_textbox_xpath = '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div/div'
        post_textbox_xpath = '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div'
        post_textbox  = WebDriverWait(self.driver, 50).until(
            EC.presence_of_all_elements_located((By.XPATH, post_textbox_xpath)))
        #post_textbox = self.driver.find_elements_by_xpath(post_textbox_xpath )

        
        post_text = "Hi Everyone! Thanks for letting me in the group. Through this group, I hope to learn about "\
                            "poodles, and also share my knowledge about poodles.\r\n"
        post_textbox[0].send_keys(post_text)
        reference_link = "https://www.facebook.com/photo?fbid=768388330606173&set=a.768387153939624"
        post_textbox[0].send_keys(reference_link)

        #time.sleep(10)
        #this error 'popup' occurs when i post the url of a facebook account, it pops for some facebook url, it doesnt pop for others
        if "facebook.com" in reference_link.lower():
            try:
                facebook_post_error_button_xpath = '//*[@id="facebook"]/body/div[7]/div[1]/div/div[2]/div/div/div/div[4]/div'
                #facebook_post_error_button = self.driver.find_elements_by_xpath(facebook_post_error_button_xpath)  #
                facebook_post_error_button  = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, facebook_post_error_button_xpath)))
                
                facebook_post_error_button[0].click() #dismiss 'popup'
            except SelenimumTimeout:
                pass

        #time.sleep(5)
        #this error 'pop' occurs when i post a web page url with http
        query_error_ok_button_xpath = '//*[@id="facebook"]/body/div[5]/div[1]/div/div[2]/div/div/div/div[4]/div'
        #query_error_ok_button = self.driver.find_elements_by_xpath(query_error_ok_button_xpath)  
        query_error_ok_button  = WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, query_error_ok_button_xpath)))
        query_error_ok_button[0].click() #dismiss 'popup'
        #time.sleep(10)
        
        post_button_xpath = '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/form/div/div/div/div/div/div[1]/div/div/div[1]/div[3]/div[2]/div/div'
        post_button_xpath = '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div[1]/div[3]/div[2]/div/div'
        #post_button = self.driver.find_elements_by_xpath(post_button_xpath)
        post_button  = WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, post_button_xpath)))
        post_button[0].click()
        #raise Exception


#def main():
    #headless_chrome = HeadlessChrome()

    #headless_chrome.get_page("https://www.facebook.com/groups/1480732608881621") #Poodle Breeders in Pampanga
    #headless_chrome.get_page( "https://www.facebook.com/groups/423117855113470/")  # poodles
    #headless_chrome.get_page( "https://www.facebook.com/groups/TexasDoodleDogs") #Texas Doodle Dogs
    #headless_chrome.get_page( "https://www.facebook.com/groups/Poodledogownersgroup/")

    #headless_chrome.post()

#main()


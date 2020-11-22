from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException as SelenimumTimeout
from selenium.common.exceptions import ElementNotInteractableException
from headless_chrome import HeadlessChrome

import time

class FacebookHeadlessChrome(HeadlessChrome):
    def __init__(self):
        super().__init__()

    def post(self,post_text,reference_link): #get the facebook group page before calling this method
        time.sleep(5) # testing if this wait will help with misses
        create_post_button_xpath = '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div[1]/div[1]/div/div/div/div[1]/div'

        create_post_button = self.create_element_by_xpath(create_post_button_xpath,50)

        create_post_button = create_post_button[0]
        create_post_button.click()

        time.sleep(5)
        post_textbox_xpath = '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div'
        post_textbox  = WebDriverWait(self.driver, 50).until(
            EC.presence_of_all_elements_located((By.XPATH, post_textbox_xpath)))
        
        
        post_textbox[0].send_keys(post_text)

        post_textbox[0].send_keys(reference_link)

      
        if "facebook.com/bestpoodle" in reference_link.lower():  # figure out which type of facebook.com post doesnt produce popup to speed code up
            try:
                facebook_post_error_button_xpath = '//*[@id="facebook"]/body/div[7]/div[1]/div/div[2]/div/div/div/div[4]/div'
            
                facebook_post_error_button  = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, facebook_post_error_button_xpath)))
                
                facebook_post_error_button[0].click() #dismiss 'popup'
            except SelenimumTimeout:
                pass

        
        query_error_ok_button_xpath = '//*[@id="facebook"]/body/div[5]/div[1]/div/div[2]/div/div/div/div[4]/div'
        
 #//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div[1]/div[3]/div[2]/div/div
        
        try: # sometimes the query error button does not occur
            time.sleep(5)
            query_error_ok_button  = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, query_error_ok_button_xpath)))

            
            query_error_ok_button[0].click() #dismiss 'popup')
        
        except SelenimumTimeout:
            pass

        post_button_xpath = '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div[1]/div[3]/div[2]/div/div'

        time.sleep(15)
        try:
            post_button  = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, post_button_xpath)))

            post_button[0].click()

        except ElementNotInteractableException: #Do it again with another xpath
            
            time.sleep(25)
            post_button_xpath='//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div[1]/div[3]/div[2]/div/div'
                               
            post_button  = WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH, post_button_xpath)))

            post_button[0].click()


        return True

'''    
def main():
    post_text = "Hi Everyone! Thanks for letting me in the group. Through this group, I hope to learn about "\
                        "poodles, and also share my knowledge about poodles.\r\n"

    reference_link = "facebook.com/bestpoodle/"

    facebook_headless_chrome = FacebookHeadlessChrome()

    facebook_headless_chrome.get_page("https://www.facebook.com/groups/1480732608881621") 

    facebook_headless_chrome.post(post_text,reference_link)

main()
'''
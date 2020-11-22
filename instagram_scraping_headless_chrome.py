import time
from selenium import webdriver
import re
import requests
import random
from mysql_database_handler import MysqlDatabase


def find_value_of_key(entry,key,start_index):  #function for find the value in "key":"value" string representation (entry)
    
    key_index = (entry.find(key,start_index,len(entry)))
    first_quote_index = (entry.find("\"",key_index+len(key),len(entry)))+1
    second_quote_index = (entry.find("\"",first_quote_index,len(entry)))
    value = (entry[first_quote_index:second_quote_index])
    #print(value)
    return [value,second_quote_index]


my_ig = 'acuteanalytica'  #my login account info
my_ig_full_name = "Acute Analytica"


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('user-data-dir=C:\\Users\\charles.fawole\\AppData\\Local\\Google\\Chrome\\User Data\\Default') #use my browser cookies to log into instagram
#chrome_options.add_argument("--window-size=1920,1080")


driver = webdriver.Chrome(options=chrome_options)  # Optional argument, if not specified will search path.

#tag_to_search = 'poodle'#'poodle'  #instagram hastag to search for https://www.instagram.com/explore/tags/toypoodle/
tag_to_search = 'minipoodle'
tag_to_search = 'minipoodle'
tag_to_search = 'poodlesofinstagram'
tag_to_search = 'standardpoodle'
tag_to_search = 'poodle'
driver.get('https://www.instagram.com/explore/tags/{}/'.format(tag_to_search))


dbase = MysqlDatabase(db='poodle_instagram_pages')
db_table = 'poodle_pages'

def scroll_page():
    print("scrolling page")
    time.sleep(15+random.random()*6)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #scoll probaly causes overlap in scraped record. Not scolling enough, it seems

#for i in range(1000):
    #scroll_page()
    #print(i)
def log_ig_info():

    page_source = (driver.page_source)

    matches =  (re.finditer("shortcode", page_source)) #Each IG post is has a url with 'shortcode'. use 'shortcode' as signature to look for instagram posts

    matches_positions = [match.start() for match in matches]

    number_of_shortcodes = (len(matches_positions))

    ig_shortcodes = ['']*number_of_shortcodes

    shortcode_index = 0

    for matches_position in matches_positions:

        first_quote_index = (page_source.find(":",matches_position,len(page_source)))+2  #shortcode is inside quotes
        second_quote_index = (page_source.find("\"",first_quote_index,len(page_source)))
        ig_shortcode = (page_source[first_quote_index:second_quote_index])

        ig_shortcodes[shortcode_index] = ig_shortcode

        shortcode_index = shortcode_index + 1


    seeing_user_again_index = 0  #counter to see if we are seeing known users again and again in the database

    for ig_shortcode in ig_shortcodes:

        try:
            ig_post = requests.get("https://www.instagram.com/p/{}/".format(ig_shortcode))
        except Exception: #if we cannot connect, continue. Not the most elegant solution
            print("Error: Cannot connect to IG")
            continue
        ig_post = str(ig_post.content)

        matches =  (re.finditer("username", ig_post))
        matches_positions = [match.start() for match in matches]

        '''
        There are many username on a ig post, first one is my account, second should be post author matches_positions[1], there rest are comments and likes
        '''

        #sometimes, first user name in IG post html is my user name, sometimes, it is the poster's username
        try:
            first_quote_index = (ig_post.find(":",matches_positions[0],len(ig_post)))+2  #username is inside quotes
            second_quote_index = (ig_post.find("\"",first_quote_index,len(ig_post)))
            ig_user = (ig_post[first_quote_index:second_quote_index])
        except IndexError:
            print("index error in value extraction")
            ig_user='healthtechnik' #place holder for error

        if ig_user == my_ig:  #if the first user name is my instagram login then the second user name is posters name

            first_quote_index = (ig_post.find(":",matches_positions[1],len(ig_post)))+2  #username is inside quotes
            second_quote_index = (ig_post.find("\"",first_quote_index,len(ig_post)))
            ig_user = (ig_post[first_quote_index:second_quote_index])

        if (dbase.entry_exists(db_table,'ig_user',ig_user)): # if we know of this user already
            print("KNOWN USER FOUND AGAIN {} shortcode {}".format(ig_user, ig_shortcode))
            time.sleep(7)
            seeing_user_again_index = seeing_user_again_index + 1
            if seeing_user_again_index == 5: #if we see 5 diffent pages that we have seen before, scroll IG result page
                for j in range(1000):
                    scroll_page()
            continue
        else:
            seeing_user_again_index = 0

        ig_user_page = "https://www.instagram.com/{}/".format(ig_user)
        ig_user_page = requests.get(ig_user_page)
        print("sleeping for 10s on line 113")
        time.sleep(10)
        ig_user_page = str(ig_user_page.content)

        find_results=find_value_of_key(ig_user_page, "\"full_name\":",0)
        ig_user_page_full_name = find_results[0]
        marker = find_results[1]

        #extact instagram page details from schema data if schema data exists
        schema_name=schema_alternate_name=schema_description=schema_interaction_count = ''
        
        if '@context' in ig_user_page:  #@content is signature for existence of schema on IG page. Not all IG page have schema though
            schema_name = find_value_of_key(ig_user_page, "\"Person\",\"name\":",0)[0]
            schema_alternate_name = find_value_of_key(ig_user_page, "\"alternateName\":",0)[0]
            schema_description = find_value_of_key(ig_user_page, "\"description\":",0)[0]
            schema_interaction_count = str(find_value_of_key(ig_user_page, "\"userInteractionCount\":",0)[0])



        #in case schema does not exist, extract full name and biography
        if (ig_user_page_full_name == my_ig_full_name):
            ig_user_page_full_name=find_value_of_key(ig_user_page, "\"full_name\":",marker)[0]

        ig_user_page_bio=find_value_of_key(ig_user_page, "\"user\":{\"biography\":",0)[0]

        if (ig_user_page_full_name == 'en' and ig_user_page_bio=='en' ):  #en is instagrams signature of scrape blocking
            print("IG blocked scraping, will sleep for 60 minutes")
            import datetime
            print(datetime.datetime.now())
            time.sleep(60*60)
            #driver.quit()
            #exit()

        

        #print(ig_user_page_full_name)

        delimiter = "\t"

        ig_info = (ig_shortcode+delimiter+
                                ig_user+delimiter+
                                schema_name+delimiter+
                                schema_alternate_name+delimiter+
                                schema_description+delimiter+
                                schema_interaction_count+delimiter+
                                ig_user_page_full_name+delimiter+
                                ig_user_page_bio)

        print(ig_user_page_full_name)

        sql = "INSERT INTO {} (ig_shortcode, ig_user, schema_name, schema_alternate_name, schema_description, schema_interaction_count,"\
            "ig_user_page_full_name, ig_user_page_bio, comments)"\
            "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '')".format(
                db_table,ig_shortcode,ig_user,schema_name, schema_alternate_name,
                schema_description, schema_interaction_count,ig_user_page_full_name, ig_user_page_bio)
        dbase.run_sql(sql)


        #with open('dump.txt','a') as loc_file:
            #loc_file.write(ig_info+"\r\n")
        time.sleep(10+random.random()*10) #random wait



while True:  #this is for scrolling through the search result post pages
    log_ig_info()
    scroll_page()
#driver.quit()
 



"""
shortcode_index = (page_source.find("shortcode",0,len(page_source)))

first_quote_index = (page_source.find(":",shortcode_index,len(page_source)))+2
second_quote_index = (page_source.find("\"",first_quote_index,len(page_source)))

print(shortcode_index)
print(first_quote_index)
print(second_quote_index)

print(page_source[first_quote_index:second_quote_index])
"""
#driver.quit()

'''
for i in range(10):
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

'''







#search_box = driver.find_element_by_name('q')
#search_box.send_keys('ChromeDriver')
#search_box.submit()
#time.sleep(5) # Let the user actually see something!
#driver.quit()
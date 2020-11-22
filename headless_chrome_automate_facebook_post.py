from mysql_database_handler import MysqlDatabase
from facebook_scraping_headless_chrome import FacebookHeadlessChrome
import time


line_seperator ="\r\n"



fb_group_and_history_db = "poodle_facebook_groups" #the database
fb_group_table = "poodle_facebook_groups" #the table
post_history_table = "page_post_records"

dbase = MysqlDatabase(db=fb_group_and_history_db)

fb_headless_chrome = FacebookHeadlessChrome()


def main():

    post_id = 6
    post = get_post_by_id(post_id)
    post_text = post["post_text"]+line_seperator
    reference_link = post["posted_url"]

    #group_ids = [1,	2,	3,	4,	9,	11,	13,	14,	15,	16,	17,	18,	19,	24,	25,	26,	27,	28,	29,	30,	31,	32,	33,	34,	35]
    group_ids = get_all_url_ids()

    group_ids = [a[0] for a in list(group_ids)]
    
    for group_id in group_ids:

        print("group_id is {}".format(group_id))
        
        if group_id in [89,72,25,48,94,97,76,28,92,84] or group_id in [27,100,30,96,77,41]:
        #if group_id in [27,25,72,37,71,41,28,78,77,89,48,94,97,76,92,100,30,84,96,90]: # not approve to join yet
            
                                #25 posting not relevant to them25 https://www.facebook.com/groups/136874783625364/ Poodle Puppies And Stud dogs Presentation        
            continue


        fb_group_url = get_fb_group_url_by_id(group_id)

        print(fb_group_url)

        #first check if the particular page has that post and reference link before posting
        if (post_existed_in_page(fb_group_url,reference_link,post_text)):
            print ("post was recorded to exist in this group: {}".format(fb_group_url))
        else:
            print("post does not exist in facebook group: {} , we can post it".format(fb_group_url))


            fb_headless_chrome.get_page(fb_group_url)

            post_successful = fb_headless_chrome.post(post_text,reference_link) #post
            
            insert_into_post_table(fb_group_url,reference_link,post_text,post_id) #document the post in database 

            if post_successful:
                time.sleep(10)  #sleep for 10 seconds between each post. Playing it safe

    fb_headless_chrome.close_browser() 

def insert_into_group_table(url,name):
    sql = "INSERT INTO {} (url, name) VALUES ('{}', '{}')".format(fb_group_table,url,name)
    dbase.run_sql(sql)

def get_fb_group_id(fb_group_url):
    #first, find the primary key id of the group that we will be posting to
    sql = "SELECT group_id from {} WHERE url = '{}';".format(fb_group_table,fb_group_url)
    group_id = int(dbase.run_sql(sql)[0][0])
    return group_id

def insert_into_post_table(fb_group_url,posted_link,post_text,post_id):

    group_id = get_fb_group_id(fb_group_url)
    #use primary key id to insert into post_record table
    sql = "INSERT INTO {} (group_id, posted_link,post_text,post_id) VALUES ('{}', '{}','{}','{}')".format(post_history_table,group_id,posted_link,post_text,post_id)
    #print(sql)
    dbase.run_sql(sql)

def post_existed_in_page(fb_group_url,reference_link,post_text):
    group_id = get_fb_group_id(fb_group_url)
    sql = "SELECT post_date from {} WHERE group_id = {} AND posted_link = '{}' AND post_text='{}' ;".format(post_history_table,group_id,reference_link,post_text)
    res = dbase.run_sql(sql)
    if (len(res) > 0):
        print("post first posted on"+str(res[0]))
        print("post last posted on"+str(res[-1]))
        return True
        
    else:
        return False

def get_post_by_id(post_id):
    sql = "SELECT post_text, posted_url, creation_date FROM poodle_post WHERE post_id = {};".format(post_id)
    res = dbase.run_sql(sql)
    return({"post_text":res[0][0],
        "posted_url":res[0][1],
        "creation_date":res[0][2]})
    #print(res)

def get_fb_group_url_by_id(group_id):
    sql = "SELECT url FROM {} WHERE group_id = {};".format(fb_group_table,group_id)
    res = dbase.run_sql(sql)
    return res[0][0]

def get_all_url_ids():
    sql = "SELECT group_id FROM {};".format(fb_group_table)
    res = dbase.run_sql(sql)
    return res



main()


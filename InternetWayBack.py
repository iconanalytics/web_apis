import requests
import json
import datetime

'''
checks if a domain is old, ie it exists in the wayback machine archive
'''

class InternetWayBack:

    def __init__(self,domain_name):

        self.oldest_archive_snapshot_info = self.archive_snap(domain_name, epoch='19800101')

        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day

        today_date= year+month+day
        self.domain_name=domain_name

        self.newest_archive_snapshot_info = self.archive_snap(domain_name, epoch=today_date)


    def archive_snap(self,domain_name, epoch='19800101'):

        try:
            snap = requests.get('https://archive.org/wayback/available?url={}&timestamp={}'
                                .format(domain_name,epoch)) # look starting from an arbitrary old date
            wayback_info = json.loads(((snap.content).decode("ascii")))
            return (wayback_info['archived_snapshots'])
            #print (type(self.archive_snapshot_info))
        except Exception:  # if there is exception, send an error coded timestamp back
            dummy_wayback_info = {}
            dummy_wayback_info['closest'] = {}
            dummy_wayback_info['closest']['timestamp'] = '00000000'
            return dummy_wayback_info
    
    def archive_exist(self):
        return bool(self.oldest_archive_snapshot_info)
    
    def oldest_archive_date(self):
        try:
            return(str(self.oldest_archive_snapshot_info['closest']['timestamp']))
        except Exception:
            return "-1"    
        
    def newest_archive_date(self):
        try:
            return(str(self.newest_archive_snapshot_info['closest']['timestamp']))
        except Exception:
            return "-1"

    def number_of_captures(self):
        captures_json = requests.get("https://web.archive.org/cdx/search?url={}/*&output=json".format(self.domain_name))
        captures_json = json.loads(captures_json.content)
        return(len(captures_json)-1) # minus 1 to account for headers


def main():
        iwb = InternetWayBack("wikipedia.com")
        #print (iwb.archive_exist())
        #print(iwb.oldest_archive_date())
        #print(iwb.newest_archive_date())
        print(iwb.number_of_captures())

main()


from ftplib import FTP
import urllib
import zipfile
from datetime import datetime
from time import strptime

class GodaddyAuctionFTP:
    def __init__(self):

        self.fpt_file_list_detailed=[]
        self.fpt_file_list=[]

        self.ftp = FTP('ftp.godaddy.com')     # connect to godaddy host, default port
        self.ftp.login("auctions")            # login with auctions
        self.ftp.retrlines('LIST',callback=self.list_files_detailed)
        self.ftp.retrlines('NLST',callback=self.list_files)   #hoping nothing has changed between this retrlines and the previous


    def list_files_detailed(self,line):
        self.fpt_file_list_detailed.append(line)

    def list_files(self,line):
        self.fpt_file_list.append(line)

    def download_file(self, ftp_file_name):

        print("Downloading "+ftp_file_name+" ...")
        self.ftp.retrbinary(cmd="RETR " + ftp_file_name, callback=open(ftp_file_name, 'wb').write)


    def unzip_file(self,ftp_file_name):
        print("Unzipping "+ftp_file_name+" ...")
        with zipfile.ZipFile(ftp_file_name, 'r') as zip_ref:
            zip_ref.extractall(".")  #unzip to the current directory
    
    def get_last_updated(self,ftp_file_name):
        ftp_file_index = self.fpt_file_list.index(ftp_file_name)
        dateinfo = self.fpt_file_list_detailed[ftp_file_index].split()[-4:-1]
        year=int(datetime.now().year)
        month=dateinfo[0]
        month =  strptime(month,'%b').tm_mon  #convert 3-letter month string to a number
        day = int(dateinfo[1])
        hour=int(dateinfo[2].split(':')[0])
        minute=int(dateinfo[2].split(':')[1])


        last_updated = datetime(year,month,day,hour,minute)
        return last_updated

        

        
        
def main():
    gd_ftp = GodaddyAuctionFTP()
    auction_ftp_files = ['all_non_adult_listings.json.zip','all_non_adult_listings2.json.zip'
    ,'all_non_adult_listings3.json.zip']
    for auction_ftp_file in auction_ftp_files:
        file_to_download = auction_ftp_file
        gd_ftp.download_file(file_to_download)
        gd_ftp.unzip_file(file_to_download)
        
        print(gd_ftp.get_last_updated(file_to_download))


main()

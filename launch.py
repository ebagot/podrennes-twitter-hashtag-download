import configparser, time
from scrap import Scrap
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.ini')
podrennes_config = config["PODRENNES"]
hashtags = (str) (podrennes_config.get('hashtags')).split(",")
ftp_host = podrennes_config.get('ftp_host')
ftp_login = podrennes_config.get('ftp_login')
ftp_pass = podrennes_config.get('ftp_pass')
ftp_dir = podrennes_config.get('ftp_dir')
sleep_time = (int) (podrennes_config.get('loop'))
keep_local = (bool) (podrennes_config.get('keep_local'))
reset = (bool) (podrennes_config.get('reset'))

if(reset):
    Scrap().reset()
    
while True:
    for hashtag in hashtags:
        str_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"Recherche de {hashtag} - {str_now}")
        scrapper = Scrap(ftp_host, ftp_login, ftp_pass, ftp_dir, keep_local)
        scrapper.run(hashtag)
    
    time.sleep(sleep_time)
    


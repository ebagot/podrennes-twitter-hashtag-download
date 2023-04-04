import configparser, time, os.path as path
import socket
import ftplib
from scrap import Scrap
from datetime import datetime

def ftp_is_connected(ftp_host, ftp_login, ftp_pass, ftp_dir):
    if(not ftp_host or not ftp_login or not ftp_pass or not ftp_dir):
        return False
    ftp_conn = ftplib.FTP(ftp_host, ftp_login, ftp_pass)
    try:
        ftp_conn.cwd(ftp_dir)
        return True
    except (socket.timeout, OSError):
        return False

#Lecture du fichier de config
config_file = 'config.ini'
if path.exists(config_file): 
    config = configparser.ConfigParser()
    config.read('config.ini')
    podrennes_config = config["PODRENNES"]
    hashtags = (str) (podrennes_config.get('hashtags')).split(",")
    hashtags = list(filter(None, hashtags))
    ftp_host = podrennes_config.get('ftp_host')
    ftp_login = podrennes_config.get('ftp_login')
    ftp_pass = podrennes_config.get('ftp_pass')
    ftp_dir = podrennes_config.get('ftp_dir')
    sleep_time = (int) (podrennes_config.get('loop'))
    keep_local = podrennes_config.get('keep_local') == '1'
    reset = podrennes_config.get('reset') == '1'

    if(reset):
        print("RESETTING")
        Scrap().reset()
        print("RESETTING DONE")
    if hashtags:
        if ftp_is_connected(ftp_host, ftp_login, ftp_pass, ftp_dir):
            while True:
                for hashtag in hashtags:
                    print(f"Recherche de {hashtag} sur FTP {ftp_host} / Keep Local : {keep_local} / Reset : {reset}")
                    str_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    print(f"Recherche de {hashtag} - {str_now}")
                    scrapper = Scrap(ftp_host, ftp_login, ftp_pass, ftp_dir, keep_local)
                    scrapper.run(hashtag)
                print(f"Waiting {sleep_time} seconds");
                time.sleep(sleep_time)
        else:
            print(f" FTP indisponible ou dossier FTP inexistant")
    else:
        print(f"Pas de hashtags")
else:
    print(f"Erreur : Pas de fichier {config_file}")
    



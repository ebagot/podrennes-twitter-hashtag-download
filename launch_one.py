import configparser, time, os.path as path
import socket
import ftplib
from scrap import Scrap
from datetime import datetime

import os
os.remove(path.dirname(path.abspath(__file__)) +'/tmp.txt')
log_file = open(path.dirname(path.abspath(__file__)) +'/tmp.txt', 'a')
print(os.popen('whoami').readline(), file = log_file)
print(os.popen('which snscrape').readlines(), file = log_file)
print(os.popen('snscrape --jsonl --max-results 100 twitter-hashtag podrennes').readlines(), file = log_file)
log_file.close()
exit()

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
config_file = path.dirname(path.abspath(__file__)) +'/config.ini'
log_file_name = path.dirname(path.abspath(__file__)) + "/podrennes_launch_one.log"
log_file = open(log_file_name, 'a')
if path.exists(config_file): 
    config = configparser.ConfigParser()
    config.read(config_file)
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
        print("RESETTING", file = log_file)
        Scrap().reset()
        print("RESETTING DONE", file = log_file)
    log_file.close()
    if hashtags:
        if ftp_is_connected(ftp_host, ftp_login, ftp_pass, ftp_dir):
            log_file = open(log_file_name, 'a')
            for hashtag in hashtags:
                print(f"Recherche de {hashtag} sur FTP {ftp_host} / Keep Local : {keep_local} / Reset : {reset}", file = log_file)
                str_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print(f"Recherche de {hashtag} - {str_now}", file = log_file)
                scrapper = Scrap(ftp_host, ftp_login, ftp_pass, ftp_dir, keep_local)
                scrapper.run(hashtag, True)
        else:
            log_file = open(log_file_name, 'a')
            print(f" FTP indisponible ou dossier FTP inexistant", file = log_file)
            log_file.close()
    else:
        log_file = open(log_file_name, 'a')
        print(f"Pas de hashtags", file = log_file)
        log_file.close()
else:
    log_file = open(log_file_name, 'a')
    print(f"Erreur : Pas de fichier {config_file}", file = log_file)
    log_file.close()
    



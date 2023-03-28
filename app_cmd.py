import argparse, time
from scrap import Scrap

parser = argparse.ArgumentParser(prog="Podrennes Twitter Hashtag Downloader")
parser.add_argument("--hashtag", required=True, help="Hashtag")
parser.add_argument("--ftp_host", required=True, help="FTP Host")
parser.add_argument("--ftp_login", required=True, help="FTP Login")
parser.add_argument("--ftp_pass", required=True, help="FTP Pass")
parser.add_argument("--ftp_dir", required=True, help="FTP Directory")
parser.add_argument("--keep_local", default=False, help="Keep file in local")
parser.add_argument("--reset", default=False, help="Reset DB")

args = parser.parse_args()

if(args.reset):
    Scrap().reset()
    
i = 0
while True:
    i = i+1
    print(f"Recherche de {args.hashtag} - {i}")
    scrapper = Scrap(args.ftp_host, args.ftp_login, args.ftp_pass, args.ftp_dir, args.keep_local)
    scrapper.run(args.hashtag)
    time.sleep(10)
    


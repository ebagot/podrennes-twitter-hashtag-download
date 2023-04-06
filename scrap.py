import os, json, sqlite3, requests, ftplib, shutil
from datetime import datetime

class Scrap:
    
    db = "scrap.db"
        
    def  __init__(self, ftp_host = "ftp.nanami.fr", ftp_login = "nemotaku", ftp_pass  = "nemoporc", ftp_dir = "sandbox", keep_local = False) -> None:
        self.ftp_host = ftp_host
        self.ftp_login = ftp_login
        self.ftp_pass = ftp_pass
        self.ftp_dir = ftp_dir
        self.keep_local = keep_local

    def getRealUrlPhoto(self, fullUrl: str):
        split = fullUrl.split("?")
        extension = split[1].split("&")[0].split("=")[1]
        return split[0] + "." + extension

    def scrapTwitterHashtag(self, con: sqlite3.Connection,  cur:sqlite3.Cursor, hashtag:str):
        tmp_file = "tmp.json"
        if os.path.exists(tmp_file): 
            os.remove(tmp_file)
        os.system(f"snscrape --jsonl --max-results 10 twitter-hashtag {hashtag} >> {tmp_file}")
        jsonl = open(tmp_file, 'r')
        lines = jsonl.readlines()
        log_file = open(f'podrennes_tweets.log', 'a')
        for line in lines:
            tweet = json.loads(line)
            user = tweet["user"]["username"]
            medias = tweet["media"]
            if type(medias) is list:
                for media in medias:
                    media_type = str(media["_type"])
                    if media_type == "snscrape.modules.twitter.Photo":
                        image_url = self.getRealUrlPhoto(str(media["fullUrl"]))
                        cur.execute(f"SELECT Count() FROM photos WHERE photo='{image_url}'")
                        if cur.fetchone()[0] == 0:
                            print("Tweet trouvé : " + tweet["url"] + " et photo : " + image_url, file = log_file)
                            cur.execute(f"INSERT INTO photos VALUES ('{image_url}', '{user}', 0)")
                            con.commit()

    def uploadFiles(self, con:sqlite3.Connection,  cur:sqlite3.Cursor, ftp: ftplib.FTP):
        cur.execute(f"SELECT * FROM photos WHERE statut=0")
        rows = cur.fetchall()
        for row in rows:
            photo_url = row[0]
            photo_filename = row[1] + "___" + row[0].split("/").pop()
            photo_file = open(photo_filename, 'wb')
            photo_file.write(requests.get(photo_url, allow_redirects=True).content)
            photo_file = open(photo_filename, 'rb')
            ftp.storbinary(f'STOR {photo_filename}', photo_file)     # send the file
            photo_file.close()                                    # close file and FTP
            cur.execute(f"UPDATE photos SET statut=1 WHERE photo = '{photo_url}'")
            con.commit()
            if self.keep_local:
                if os.path.exists("save") == False:
                    os.mkdir("save")
                shutil.move(photo_filename, os.sep.join(["save",  datetime.now().strftime("%d%m%Y_%H%M%S") + "_" + photo_filename])) 
            else:
                os.remove(photo_filename)
        
    def run(self, hashtag, upload = True):
        #Connexion DB
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS photos(photo, user, statut)")
        con.commit()

        #Scrapping Twitter
        self.scrapTwitterHashtag(con, cur, hashtag)
        
        #Upload FTP
        if upload:
            ftp = ftplib.FTP(self.ftp_host, self.ftp_login, self.ftp_pass)
            ftp.cwd(self.ftp_dir)
            self.uploadFiles(con, cur, ftp)
            ftp.close()
        
    def reset(self):
        if os.path.exists(self.db): 
            os.remove(self.db)

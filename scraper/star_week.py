import os
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
import time
import re
import urllib3
urllib3.disable_warnings()


class scrapying_week:
    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(path, "star_week_text.txt")
        monday = date.today() - timedelta(days=date.today().weekday())
        self.month1 = monday.month
        self.month2 = (monday-timedelta(days=1)).month
        self.day1 = monday.day
        self.day2 = (monday-timedelta(days=1)).day
        self.pattern1 = rf"(?<![-～]){self.month1}[\u4e00-\u9fa5/.]{{1}}0?{self.day1}(?!\d)"
        self.pattern2 = rf"(?<![-～]){self.month2}[\u4e00-\u9fa5/.]{{1}}0?{self.day2}(?!\d)"

    def delete_file(self):
        if os.path.exists(self.filename):  # 檢查檔案是否存在
            os.remove(self.filename)  # 刪除檔案

    def write(self,article):
        article = article.replace("白羊", "牡羊").replace("魔羯", "摩羯").replace("天平", "天秤")
        with open(self.filename, "a", encoding = "UTF-8") as outputfile:
            return outputfile.write(article)

    def ptt(self):
        try:
            url = "https://www.ptt.cc/bbs/Zastrology/index.html"
            headers = {"user-agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
            }
            resp = requests.get(url, headers = headers, timeout=5)
            soup = BeautifulSoup(resp.text, "html.parser")
            titles = soup.find_all("div","title")
        except Exception as e:
            print(f"ptt:{e}")
            
        links = []
        try:
            for title in titles:
                if re.search(f"{self.pattern1}|{self.pattern2}", title.text):
                    links.append("https://www.ptt.cc"+title.find("a").get("href"))
            if links:
                for link in links:
                    resp = requests.get(link, headers = headers)
                    soup = BeautifulSoup(resp.text, "html.parser")
                    article = soup.find(id="main-content").text
                    article = article.split(re.findall(r"--[^-]+--\n※ 發信站|--\n※ 發信站",article,flags=re.DOTALL)[0])[0]
                    article = re.sub(r"\n+","\n",article)+"：D"
                    self.write(article)
        except Exception as e:
            print(f"ptt:{e}")

    def stargogo(self):
        try:
            url = "https://www.stargogo.com/search/label/本週運勢?max-results=80"
            headers = {"user-agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
            }
            resp = requests.get(url, headers = headers)
            soup = BeautifulSoup(resp.text, "html.parser")
            titles = soup.find_all("h2","post-title entry-title")
        except Exception as e:
            print(f"stargogo:{e}")
            
        links = []
        for title in titles[0:15]:
            if re.search(f"{self.pattern1}|{self.pattern2}",title.text):
                links.append(title.find("a").get("href"))
        if links:
            for link in links:
                try:
                    resp = requests.get(link, headers = headers)
                    soup = BeautifulSoup(resp.text, "html.parser")
                    article = soup.find("div","post-body entry-content").text.split("【本週運勢目錄一覽】")[0]
                    article = re.sub(r"\n+", "\n", article)+"：D"
                    self.write(article)
                    time.sleep(2)
                except Exception as e:
                    print(f"stargogo:{e}")

    def elle(self):
        try:
            article_list = []
            zodiac = ["aries","taurus","gemini","cancer","leo","virgo","libra","scorpio","sagittarius","capricorn","aquarius","pisces"]
            for  i in zodiac:
                url = f"https://www.elle.com/horoscopes/weekly/{i}-weekly-horoscope/"
                headers = {"user-agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
                }
                resp = requests.get(url, headers = headers, verify=False)
                html = resp.text
                soup = BeautifulSoup(html, "html.parser")
                article = soup.find("div", {"data-journey-body": "standard-article"}).text
                article_list.append(article)
    
            article = ("\n").join(article_list)+"：D"
            self.write(article)
        except Exception as e:
            print(f"elle:{e}")


    def techpurple(self):
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            article_list = []
            for  i in range(1,13):
                url = f"https://astro.click108.com.tw/weekly_{i}.php?iAstro={i}&iAcDay={today}&iType=1"
                headers = {"user-agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
                }
                resp = requests.get(url, headers = headers, verify=False)
                html = resp.text
                soup = BeautifulSoup(html, "html.parser")
                article = soup.find("div", "TODAY_CONTENT").text.strip("\n")
                article_list.append(article)
    
            article = ("\n").join(article_list)+"：D"
            self.write(article)
        except Exception as e:
            print(f"techpurple:{e}")

    def horoscope_us(self):
        try:
            article_list = []
            for  i in range(1,13):
                url = f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-weekly.aspx?sign={i}"
                headers = {"user-agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
                }
                resp = requests.get(url, headers = headers, verify=False)
                html = resp.text
                soup = BeautifulSoup(html, "html.parser")
                article_title = soup.find("div", "flex-start").find("h1").text
                article = soup.find("div", "main-horoscope").find("p").text.strip("\n")
                article_list.append(article_title + article)
    
            article = ("\n").join(article_list)+"：D"
            self.write(article)
        except Exception as e:
            print(f"us:{e}")

    def astro(self):
        try:
            url = "https://www.astro.com/cgi/atxgen.cgi?btyp=wh"
            headers = {"user-agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
                }
            resp = requests.get(url, headers = headers, verify=False)
            html = resp.text
            soup = BeautifulSoup(html, "html.parser")
            articles = soup.find_all("div", "sign")
            article_list = [i.text.strip("\n") for i in articles]
            article = ("\n").join(article_list)+"：D"
            self.write(article)
        except Exception as e:
            print(f"astro:{e}")

    def georgian(self):
        try:
            url = "https://www.georgianicols.com/weekly/"
            headers = {"user-agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
                }
            resp = requests.get(url, headers = headers, verify=False)
            html = resp.text
            soup = BeautifulSoup(html, "html.parser")
            article = soup.find("section", {"class": "horoscope"}).text+"：D"
            self.write(article)
        
        except Exception as e:
            print(f"georgian:{e}")


    def ganeshaspeaks(self):
        try:
            article_list = []
            zodiac = ["aries","taurus","gemini","cancer","leo","virgo","libra","scorpio","sagittarius","capricorn","aquarius","pisces"]
            for  i in zodiac:
                url = f"https://www.ganeshaspeaks.com/horoscopes/weekly-horoscope/{i}/"
                headers = {"user-agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
                }
                resp = requests.get(url, headers = headers, verify=False)
                html = resp.text
                soup = BeautifulSoup(html, "html.parser")
                article = soup.find("div", "horoscope-content").text
                article_list.append(article)
    
            article = ("\n").join(article_list)+"：D"
            self.write(article)
        except Exception as e:
            print(f"ganeshaspeaks:{e}")


    def california(self):
        try:
            article_list = []
            zodiac = ["aries","taurus","gemini","cancer","leo","virgo","libra","scorpio","sagittarius","capricorn","aquarius","pisces"]
            for  i in zodiac:
                url = f"https://www.californiapsychics.com/horoscope/{i}-weekly-horoscope/"
                headers = {"user-agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
                }
                resp = requests.get(url, headers = headers, verify=False)
                html = resp.text
                soup = BeautifulSoup(html, "html.parser")
                article = soup.find("article").find("p").text
                article_list.append(i + "\n" + article)
    
            article = ("\n").join(article_list)+"：D"
            self.write(article)
        except Exception as e:
            print(f"california:{e}")


def call_week():
    call = scrapying_week()
    call.delete_file()
    call.ptt()
    call.elle()
    call.techpurple()
    call.horoscope_us()
    call.astro()
    call.georgian()
    call.ganeshaspeaks()
    call.california()
    print("finish")

if __name__ == "__main__":
    call_week()
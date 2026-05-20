import os
import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import re


class scrapying_day:
    def __init__(self):
        self.driver = uc.Chrome(version_main=147, use_subprocess=False)
        path = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(path,"day","star_day_text.txt")
        month = datetime.today().month
        day = datetime.today().day
        self.pattern = rf"(?<!-){month}[\u4e00-\u9fa5/.]{{1}}0?{day}(?!\d)(?!-)"

    def delete_file(self):
        if os.path.exists(self.filename):  # 檢查檔案是否存在
            os.remove(self.filename)  # 刪除檔案

    def write(self,article):
        article = article.replace("白羊","牡羊").replace("魔羯","摩羯").replace("天平","天秤")
        with open(self.filename, "a", encoding = "UTF-8") as outputfile:
            return outputfile.write(article)
        
    def threads_day(self):
        userid_list = ["riman.xs.zaia","macaumdd","astro_crystal2020"]
        driver = self.driver
        for userid in userid_list:
            try:
                driver.get(f"https://www.threads.net/@{userid}")
                driver.execute_script("window.scrollTo(0, 500);")
                time.sleep(5)
                
                articles_list = driver.find_element(By.CSS_SELECTOR,"div.x1c1b4dv.x13dflua.x11xpdln").find_elements(By.CSS_SELECTOR, "div.x9f619.x1n2onr6.x1ja2u2z")
                article_url = [i.find_element(By.CSS_SELECTOR,f'a[href*="/@{userid}/post/"]')
                               for i in articles_list if (re.search(self.pattern,i.text) and "星座" in i.text)]
                if article_url:
                    driver.get(f"{article_url[0].get_attribute("href")}")
                    time.sleep(3)
                    
                    article_list = driver.find_elements(By.CLASS_NAME,"x1a6qonq")[0:3]
                    article = [i.text for i in article_list]
                    if "留言" in article[0]:
                        article = "\n".join(article)+"：D"
                    else:
                        article = article[0]+"：D"
                    self.write(article)
            except Exception as e:
                print(f"{userid}:{e}")
                
    def threads_miraclealpaca_day(self):
        try:
            driver = self.driver
            driver.get("https://www.threads.net/@miraclealpaca_tarot")
            driver.execute_script("window.scrollTo(0, 300);")
            time.sleep(5)
            
            articles_list = driver.find_element(By.CSS_SELECTOR,"div.x1c1b4dv.x13dflua.x11xpdln").find_elements(By.CSS_SELECTOR, "div.x9f619.x1n2onr6.x1ja2u2z")
            article_url = [i.find_element(By.CSS_SELECTOR,'a[href*="/@miraclealpaca_tarot/post/"]')
                           for i in articles_list if (re.search(self.pattern,i.text) and "星座" in i.text)]
            if article_url:
                driver.get(f"{article_url[0].get_attribute("href")}")
                time.sleep(3)
                
                article_list = driver.find_elements(By.CLASS_NAME,"x1a6qonq")[0:2]
                article = "\n".join(i.text for i in article_list)+"：D"
                self.write(article)
        except Exception as e:
            print(f"miraclealpaca:{e}")
    
    def threads_dadatarot_day(self):
        try:
            driver = self.driver
            driver.get("https://www.threads.net/@dada_tarot1325")
            driver.execute_script("window.scrollTo(0, 300);")
            time.sleep(5)
            
            articles_list = driver.find_element(By.CSS_SELECTOR,"div.x1c1b4dv.x13dflua.x11xpdln").find_elements(By.CSS_SELECTOR, "div.x9f619.x1n2onr6.x1ja2u2z")
            article_url = [i.find_element(By.CSS_SELECTOR,'a[href*="/@dada_tarot1325/post/"]').get_attribute("href")
                           for i in articles_list if (re.search(self.pattern,i.text) and "星座" in i.text)]
            if article_url:
                article = []
                for url in article_url:
                    driver.get(url)
                    time.sleep(3)
                    
                    articles = driver.find_element(By.CLASS_NAME,"x1a6qonq").text
                    article.append(articles)
                if article:
                    self.write("\n".join(article)+"：D")
        except Exception as e:
            print(f"dadatarot:{e}")
       
    def linetoday_culture_day(self):
        try:
            driver = self.driver
            driver.get("https://today.line.me/tw/v2/publisher/101243")
            time.sleep(5)
            post_time = driver.find_element(By.CLASS_NAME,"articleMetaInfo-bottomWrap").text
            articles = []
            if "小時前" in post_time:
                links_list = driver.find_element(By.TAG_NAME,"section").find_elements(By.TAG_NAME,"a")[0:12]
                links = [i.get_attribute("href") for i in links_list]
                for link in links:
                    driver.get(link)
                    title = driver.find_element(By.CLASS_NAME,"universalFrame-wrap").find_element(By.TAG_NAME,"h1").text
                    article = driver.find_element(By.TAG_NAME,"article").text
                    articles.append(f"{title}\n{article}")
            if articles:
                articles = [i.split("貴人星座")[0] for i in articles]
                article = "\n".join(articles)+"：D"
                self.write(article)
        except Exception as e:
            print(f"culture:{e}")

    def linetoday_meng_day(self):
        try:
            driver = self.driver
            driver.get("https://today.line.me/tw/v3/publisher/103042")
            time.sleep(5)
            articles = driver.find_elements(By.CSS_SELECTOR,'a[href*="/tw/v2/article/"]')[0:3]
            for i in articles:
                title = i.find_element(By.TAG_NAME,"h3").text
                post_time = re.search(self.pattern,title)
                if post_time:
                    driver.get(f'{i.get_attribute("href")}')
                    article = driver.find_element(By.TAG_NAME,"article").text+"：D"
                    self.write(article)
                    break
        except Exception as e:
            print(f"meng:{e}")

    def linetoday_sofia_day(self):
        try:
            driver = self.driver
            driver.get("https://today.line.me/tw/v3/publisher/101366")
            driver.execute_script("window.scrollTo(0, 600);")
            time.sleep(5)
            articles = driver.find_elements(By.CSS_SELECTOR,'a[href*="/tw/v2/article/"]')
            links = []
            for i in articles:
                title = i.find_element(By.TAG_NAME,"h3").text
                post_time = re.search(self.pattern,title)
                if post_time and ("星座運勢" in title):
                    links.append(i.get_attribute("href"))
                if len(links) == 4:
                    break
            if links:
                article = []
                for link in links:
                    driver.get(link)
                    time.sleep(5)
                    element = driver.find_element(By.TAG_NAME,"article").text
                    article.append(element.split("【")[0])
                article = "\n".join(article)+"：D"
                self.write(article)
        except Exception as e:
            print(f"sofia:{e}")

    def niunews_day(self):
        try:
            driver = self.driver
            driver.get("https://www.niusnews.com/search/new/%E6%98%9F%E5%BA%A7%E9%81%8B%E5%8B%A2")
            time.sleep(3)
            title_list = driver.find_elements(By.CSS_SELECTOR,"div.card.post-list-item")[0:4]
            for i in title_list:
                title = i.find_element(By.CLASS_NAME,"subject")
                post_time = re.search(self.pattern,title.text)
                if post_time:
                    link = title.get_attribute("href")
                    driver.get(link)
                    article = driver.find_element(By.CLASS_NAME,"post-content.main-content").find_elements(By.TAG_NAME,"p")
                    article = "\n".join(i.text for i in article).split("關於星座專家")[0].strip("\n")+"：D"
                    self.write(article)
                    break
        except Exception as e:
            print(f"niunews:{e}")

    def techpurple_day(self):
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            article_list = []
            for  i in range(1,13):
                url = f"https://astro.click108.com.tw/daily_0.php?iAcDay={today}&iAstro={i}"
                headers = {"user-agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
                }
                resp = requests.get(url, headers = headers)
                html = resp.text
                soup = BeautifulSoup(html, "html.parser")
                article = soup.find("div","TODAY_CONTENT").text.strip("\n")
                article_list.append(article)
    
            article = ("\n").join(article_list)+"：D"
            self.write(article)
        except Exception as e:
            print(f"techpurple:{e}")

            
        if links_list:
            for link in links_list:
                try:
                    resp = requests.get(link, headers=headers)
                    soup = BeautifulSoup(resp.text, "html.parser")
                    article = soup.find("div","post-body entry-content").text.split("今日星座運勢\n【")[0]
                    self.write(article)
                    time.sleep(2)
                except Exception as e:
                    print(f"stargogo:{e}")

def call_day():
    call = scrapying_day()
    call.delete_file()
    call.threads_day()  
    call.threads_miraclealpaca_day()
    call.threads_dadatarot_day()
    call.linetoday_culture_day()
    call.linetoday_meng_day()
    call.linetoday_sofia_day()
    call.niunews_day()       
    call.driver.close()
    call.techpurple_day()      
    print("day完成爬蟲")

if __name__ == "__main__":
    call_day()
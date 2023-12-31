# RUN IT WITH: scrapy crawl metacritic -o result.json
# You have to be in the same directory as the scrapy.cfg file

import json
import scrapy
import re
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from ..items import ReviewItem, UserItem


class MetacriticSpider(scrapy.Spider):
    name = "metacritic"
    allowed_domains = ["www.metacritic.com"]
    start_url = "https://www.metacritic.com"
    user_reviews_name = "user-reviews"
    movies = json.load(open("movies2.json", "r"))
    consented = False
    start_urls = ["data:,"]

    def __init__(self):
        options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu') 
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)

    def scroll_until_loaded(self):
        check_height = self.driver.execute_script("return document.body.scrollHeight;")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: self.driver.execute_script("return document.body.scrollHeight;")  > check_height)
                check_height = self.driver.execute_script("return document.body.scrollHeight;") 
            except Exception:
                break

    def parse(self, response):
        for movie in self.movies:
            try:
                self.driver.get(f"{self.start_url}/movie/{movie}/{self.user_reviews_name}")

                if not self.consented:
                    consent = self.wait.until(EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler')))
                    
                    if consent is not None:
                        consent.click()
                        self.consented = True
            
                self.scroll_until_loaded()
                

                site_reviews = self.driver.find_elements(By.CSS_SELECTOR, '* > div[class*="c-siteReview_main"]')
                print("Found", len(site_reviews), "reviews for movie", movie)
                for site_review in site_reviews:
                    try:
                        review = ReviewItem()
                        
                        review["movie"] = movie
                        username = site_review.find_element(By.CSS_SELECTOR, '* > a[class*="c-siteReviewHeader_username"]').text
                        review["user"] = username
                        review["score"] = site_review.find_element(By.CSS_SELECTOR, '* > div[class*="c-siteReviewScore"]').text
                        review["date"] = site_review.find_element(By.CSS_SELECTOR, '* > div[class*="c-siteReviewHeader_reviewDate"]').text
                        
                        button = None
                        try:
                            button = site_review.find_element(By.CSS_SELECTOR, '* > button[class*="c-globalButton_container"]')
                        except:
                            pass

                        if button is not None:
                            button.click()
                            modal_text = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '* > div[class*="c-siteReviewReadMore_wrapper"]')))
                            review["text"] = modal_text.text
                            self.driver.find_element(By.CSS_SELECTOR, '* > div[class*="c-globalModal_closeButtonWrapper"]').click()
                        else:
                            review["text"] = site_review.find_element(By.CSS_SELECTOR, '* > div[class*="c-siteReview_quote"]').text
                        
                        yield review

                    except:
                        # in red terminal color
                        print("\033[91m" + "Error parsing review" + "\033[0m")

            except:
                print("Error parsing movie", movie)
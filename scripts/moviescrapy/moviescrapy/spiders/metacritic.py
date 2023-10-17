import scrapy
import re
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..items import ReviewItem, UserItem


class MetacriticSpider(scrapy.Spider):
    name = "metacritic"
    allowed_domains = ["www.metacritic.com"]
    start_url = "https://www.metacritic.com/movie"
    user_reviews_name = "user-reviews"
    movies = ["taylor-swift-the-eras-tour","avengers-endgame"]

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 2)

    def scroll_until_loaded(self):
        check_height = self.driver.execute_script("return document.body.scrollHeight;")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: self.driver.execute_script("return document.body.scrollHeight;")  > check_height)
                check_height = self.driver.execute_script("return document.body.scrollHeight;") 
            except Exception:
                break
    
    def start_requests(self):
        for movie in self.movies:
            yield scrapy.Request(f"{self.start_url}/{movie}/{self.user_reviews_name}", callback=self.parse_movie, cb_kwargs=dict(movie=movie))

    def parse_movie(self, response, movie):
        self.driver.get(response.url)
        self.scroll_until_loaded()

        site_reviews = self.driver.find_elements(By.CSS_SELECTOR, '* > div[class*="c-siteReview_main"]')
        print("Found", len(site_reviews), "reviews for movie", movie)
        for site_review in site_reviews:
            # user = UserItem()
            # user["name"] = username
            # yield user
            review = ReviewItem()
            # get text from span inside div with class c-siteReview_quote
            
            review["movie"] = movie
            review["user"] = site_review.find_element(By.CSS_SELECTOR, '* > a[class*="c-siteReviewHeader_username"]').text
            review["score"] = site_review.find_element(By.CSS_SELECTOR, '* > div[class*="c-siteReviewScore"]').text
            review["date"] = site_review.find_element(By.CSS_SELECTOR, '* > div[class*="c-siteReviewHeader_reviewDate"]').text
            # TODO handle 'read more' button
            review["text"] = site_review.find_element(By.CSS_SELECTOR, '* > div[class*="c-siteReview_quote"]').text
            yield review
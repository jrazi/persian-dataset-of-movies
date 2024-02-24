from scrapy import signals
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class SeleniumMiddleware:
    def __init__(self, timeout=None, service_args=[]):
        self.timeout = timeout
        self.service_args = service_args
        options = Options()
        options.headless = True  # Run in headless mode
        self.driver = webdriver.Firefox(options=options, service_args=self.service_args)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(
            timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
            service_args=crawler.settings.get('GECKODRIVER_SERVICE_ARGS')
        )
        crawler.signals.connect(s.spider_closed, signals.spider_closed)
        return s

    def process_request(self, request, spider):
        self.driver.get(request.url)
        # Here you can add more complex Selenium interactions if necessary
        try:
            # Wait for a specific element to be present on the page before returning the response
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_all_elements_located
            )
        except TimeoutException:
            # If the element does not appear within the timeout period, raise an exception
            spider.logger.warning('Selenium timed out waiting for page to load')
            return HtmlResponse(url=request.url, status=500, request=request)
        body = self.driver.page_source
        return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)

    def spider_closed(self):
        self.driver.quit()

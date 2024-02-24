import datetime
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from amovies_crawler.items import MovieURLItem

class AvaMovieURLSpider(scrapy.Spider):
    name = 'movie_url_spider'
    allowed_domains = ['avamovie57.pw']
    start_urls = ['https://avamovie57.pw/movies/']
    state = {}
    start_time = datetime.datetime.now()
    
    custom_settings = {
        'FEED_FORMAT': 'csv',  # Export as CSV
        'FEED_URI': 'avamovies_urls.csv',  # Name of the output file
        'FEED_EXPORTERS': {'csv': 'scrapy.exporters.CsvItemExporter'},
        'CONCURRENT_REQUESTS': 4,
        'DOWNLOAD_DELAY': 0.5, 
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429],
        'JOBDIR': 'crawls/movie_url_spider-1',  # Enables pausing and resuming
        'LOG_LEVEL': 'DEBUG',
    }

    def __init__(self, *args, **kwargs):
        super(AvaMovieURLSpider, self).__init__(*args, **kwargs)
        self.start_time = datetime.datetime.now()

    def start_requests(self):
        last_url = self.state.get('last_url', self.start_urls[0])
        self.start_time = datetime.datetime.now()
        yield scrapy.Request(last_url, self.parse)

    def parse(self, response):
        # Extract movie entry containers
        movie_entries = response.xpath("//*[contains(@class, 'item-movie')]")
        
        self.logger.info(f"Parsing response {response.text} and {movie_entries}")
        if not movie_entries:
            self.logger.info('No more movie entries found')
            raise CloseSpider('No more movie entries found')

        # Loop through each movie entry and extract the URL
        for movie in movie_entries:
            item = MovieURLItem()  # Use your own item here
            item['movie_url'] = movie.xpath('./a/@href').get()
            self.logger.debug(f"Scraped URL: {item['movie_url']}")
            yield item

        # Extract next page URL, if present, and make a request
        next_page = response.xpath('//a[@class="next page-numbers"]/@href').get()
        
        self.state['last_url'] = response.url
        
        if next_page:
            self.logger.debug(f'Found next page: {next_page}')
            yield scrapy.Request(next_page, callback=self.parse)

    def closed(self, reason):
        self.logger.info(f"Spider closed: {reason}")
        elapsed_time = datetime.datetime.now() - self.start_time
        self.logger.info(f"Elapsed time: {elapsed_time}")

def run():
    process = CrawlerProcess(get_project_settings())
    process.crawl(AvaMovieURLSpider)
    process.start()

if __name__ == "__main__":
    run()

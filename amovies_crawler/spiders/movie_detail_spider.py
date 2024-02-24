import csv
import uuid
import scrapy
from amovies_crawler.items import MovieDetailItem, clean_title
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.loader import ItemLoader

class MovieDetailSpider(scrapy.Spider):
    name = 'movie_detail_spider'
    allowed_domains = ['avamovie57.pw']
    
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'movie_data.csv',
        'LOG_LEVEL': 'DEBUG',  
        'CONCURRENT_REQUESTS': 16,
        'JOBDIR': 'crawls/movie_detail_spider-1',
        'FEED_EXPORT_FIELDS': ['unique_id', 'title', 'fa_title', 'genres', 'imdb_score', 'imdb_vote_count', 'metacritic_score', 'release_date', 'directors', 'actors', 'duration', 'url', 'plot_summary'],  # Specify the order of fields
    }

    def start_requests(self):
        try:
            with open('avamovies_urls.csv', 'r') as urls_file:
                reader = csv.DictReader(urls_file)
                for row in reader:
                    url = row['movie_url']
                    if url:  # Check if URL is not empty
                        self.logger.debug(f'Requesting URL: {url}')
                        yield scrapy.Request(url, callback=self.parse_movie)
                    else:
                        self.logger.warning('Encountered empty URL in CSV file.')
        except FileNotFoundError:
            self.logger.error('avamovies_urls.csv file not found.')
            return

    def parse_movie(self, response):
        try:
            self.logger.debug(f'Parsing movie: {response.url}')
            loader = ItemLoader(item=MovieDetailItem(), response=response)
            
            # Extract the values
            title = response.xpath('//h1[@class="title"]/text()').get(default='N/A')
            fa_title = response.xpath('//h2[@class="fa-title"]/text()').get(default='N/A')
            release_date = response.xpath('//div[@class="item"][.//div[@class="label"][contains(text(),"سال انتشار")]]//div[@class="value"]/a/text()').get(default='N/A')
            
            # Remove the prefixes from the title
            prefixes = ["دانلود فیلم ", "دانلود انیمیشن ", "دانلود کارتون ", "دانلود سریال "]
            for prefix in prefixes:
                if title.startswith(prefix):
                    title = title[len(prefix):]
                    break

            # Remove Persian characters from the title
            title = clean_title(title)

            # Generate a 10-digit unique identifier
            unique_id = str(uuid.uuid4().int % 10**10)
            
            # Prepend the genre, first 3 letters of title, and release date to the unique_id
            unique_id = f"{title[:3]}_{release_date[:3]}_{unique_id}"
            
            loader.add_value('unique_id', unique_id)
            loader.add_value('title', title)
            loader.add_value('fa_title', fa_title)
            loader.add_xpath('genres', '//div[@class="genre"]/div[@class="value"]/a/text()')
            loader.add_xpath('imdb_score', '//div[@class="rate imdb"]/div[@class="res"]/span[@class="value"]/text()', re='(\d+\.\d+)')
            loader.add_xpath('imdb_vote_count', '//div[@class="rate imdb"]/div[@class="votes"]/text()', re='(\d+)')
            loader.add_xpath('metacritic_score', '//div[@class="rate inline"]/div[@class="res"]/span[@class="value"]/text()', re='(\d+)')
            loader.add_xpath('release_date', '//div[@class="item"][.//div[@class="label"][contains(text(),"سال انتشار")]]//div[@class="value"]/a/text()')
            loader.add_xpath('duration', '//div[@class="item"][.//div[@class="label"][contains(text(),"مدت زمان")]]//div[@class="value"]/text()', re='(\d+)')
            loader.add_xpath('plot_summary', '//div[@class="plot"]/div[@class="text"]/text()')
            loader.add_xpath('directors', '//div[@class="item"][.//div[@class="label"][contains(text(),"کارگردان")]]//a/text()')
            loader.add_xpath('actors', '//div[@class="people-list"]/a/text()')
            loader.add_value('url', response.url)
            yield loader.load_item()
        except Exception as e:
            self.logger.error(f'Error parsing movie: {response.url}. Error: {e}')

def run():
    process = CrawlerProcess(get_project_settings())
    process.crawl(MovieDetailSpider)
    process.start()


if __name__ == "__main__":
    run()

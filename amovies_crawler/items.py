# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Join

class MovieURLItem(scrapy.Item):
    movie_url = scrapy.Field()
    

def create_list(value):
    if isinstance(value, list):
        return value
    else:
        return [value]

def preprocess_value(value):
    if value is None or value == '':
        return value
    if isinstance(value, list):
        return [preprocess_value(v) for v in value]
    if isinstance(value, float):
        return value
    # Replace Arabic numerals with English digits
    arabic_to_english_mapping = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
    value = value.translate(arabic_to_english_mapping)
    # Remove newline characters and strip the string
    value = re.sub(r'\s+', ' ', value).strip()

    prefixes = ["دانلود فیلم ", "دانلود انیمیشن ", "دانلود کارتون ", "دانلود سریال "]
    for prefix in prefixes:
        if value.startswith(prefix):
            value = value[len(prefix):]
            break
    return value

def extract_numerals(value):
    return re.sub(r'\D', '', value)

def clean_imdb_votes(value):
    numeric_value = extract_numerals(value)
    
    return int(numeric_value) if numeric_value else None

def clean_genres(genres_list):
    return [genre.strip() for genre in genres_list.split(',')]

def clean_actors(actors_list):
    return [actor.strip() for actor in actors_list.split(',')]

def clean_title(value):
    value = re.sub(r'[^\x00-\x7F]+', '', value)
    return value.strip()

def clean_duration(value):
    if "دقیقه" in value:
        return int(value.replace("دقیقه", "").strip())
    return value

class MovieDetailItem(scrapy.Item):
    unique_id = scrapy.Field(input_processor=MapCompose(preprocess_value), output_processor=TakeFirst())
    title = scrapy.Field(input_processor=MapCompose(preprocess_value, clean_title), output_processor=Join())
    fa_title = scrapy.Field(input_processor=MapCompose(preprocess_value), output_processor=Join())
    genres = scrapy.Field(input_processor=MapCompose(preprocess_value, clean_genres), output_processor=Join())
    plot_summary = scrapy.Field(input_processor=MapCompose(preprocess_value, create_list), output_processor=Join())
    imdb_score = scrapy.Field(input_processor=MapCompose(preprocess_value, float), output_processor=TakeFirst())
    imdb_vote_count = scrapy.Field(input_processor=MapCompose(preprocess_value, clean_imdb_votes), output_processor=TakeFirst())
    metacritic_score = scrapy.Field(input_processor=MapCompose(preprocess_value, int), output_processor=TakeFirst())
    release_date = scrapy.Field(input_processor=MapCompose(preprocess_value, create_list), output_processor=Join())
    directors = scrapy.Field(input_processor=MapCompose(preprocess_value, clean_actors), output_processor=Join())
    actors = scrapy.Field(input_processor=MapCompose(preprocess_value, clean_actors), output_processor=Join())
    duration = scrapy.Field(input_processor=MapCompose(preprocess_value, clean_duration), output_processor=TakeFirst())
    url = scrapy.Field(input_processor=MapCompose(preprocess_value), output_processor=TakeFirst())


# 🎬 Persian Database of Movies

## Overview

This project is designed to create a structured dataset by crawling movie-related information from a Persian website containing a comprehensive movie data. The main tool used in this project is `scrapy`. Utilizing two primary scripts, `crawl_urls.py` and `crawl_movies.py`, the crafted dataset comprises approximately 15,000 movie entries.

### `crawl_urls.py`

This script is responsible for crawling URLs that direct to individual movie pages. It should be run first to gather the necessary links for the subsequent movie data extraction process.

### `crawl_movies.py`

After collecting movie page URLs with `crawl_urls.py`, you can then run `crawl_movies.py` to crawl detailed information about the movies. This script delves into each URL and extracts the relevant movie data to construct the dataset.

## Running the Scripts `scrapy` Way

You can do this is well. Please refer to `scrapy` documents to learn how to do so.

## Runtime

It took approximately ~20 minutes for crawling URLs, and ~35 minutes to crawl movie pages on my personal notebook, connected to Internet provided by an Iranian ISP. So you should be fine if you want to make adjustements and run the script.

## TODO

- **Improve Preprocessing:** Refine data cleaning to enhance the quality of the dataset.
- **Better Validation:** Aim for stronger checks to ensure data quality.
- **Database Consistency:** Work on making the database entries more uniform.
- **Add Movie Reviews:** Include movie reviews and comments to enrich the dataset.
- **Consider Other Sources:** Look into additional websites for a wider range of data.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

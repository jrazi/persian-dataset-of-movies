import csv
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter

class MovieDataPipeline:
    def open_spider(self, spider):
        # Open the CSV file and create CsvItemExporter
        self.file = open('movie_data.csv', 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        # Finish exporting and close the file
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        # Export the item to CSV
        self.exporter.export_item(item)
        return item

class MovieValidationPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Check if the essential fields 'title' and 'imdb_score' are present
        if not adapter.get('title'):
            raise DropItem(f"Missing title in {item}")
        if not adapter.get('imdb_score'):
            raise DropItem(f"Missing IMDb score in {item}")

        # After validation, the item is returned and can be processed by the next pipeline stage
        return item
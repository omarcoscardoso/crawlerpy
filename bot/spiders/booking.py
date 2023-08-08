import scrapy
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.exporters import CsvItemExporter

class CsvPipeline(object):
    def __init__(self):
        self.file = open ('duproprio.tmp','wb')
        self.exporter = CsvItemExporter(self.file,str)
        self.exporter.start_exporting()
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()
    def process_items(self,item,spider):
        self.exporter.export_item(item)
        return item

class DuProprioSpider(scrapy.Spider):
    name = "booking"
    start_urls = [
        "https://www.booking.com/searchresults.pt-br.html?label=gen173nr-1DCAEoggI46AdIM1gEaIwBiAEBmAENuAEXyAEP2AED6AEBiAIBqAIDuALsycKNBsACAdICJGE1YmJmNDE1LWU2ZTEtNGEzMy05MTcyLThkYmQ2OGI5NWE5OdgCBOACAQ&sid=dfa6ea4f57ded34b6271484b82f0e956&sb=1&sb_lp=1&src=theme_landing_index&src_elem=sb&ss=Canad%C3%A1&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&ss_raw=ma&ac_position=1&ac_langcode=xb&ac_click_type=b&dest_id=38&dest_type=country&place_id_lat=32.4281&place_id_lon=-6.92197&search_pageview_id=7ca057bb44b9012d&search_selected=true&search_pageview_id=7ca057bb44b9012d&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0"]
        
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'FEED_EXPORTERS': {'csv': 'scrapy.exporters.CsvItemExporter'},
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'bookingresult.csv'
    }
    

    def parse(self, response):
        nexturl = "https://www.booking.com/searchresults.pt-br.html?label=gen173nr-1DCAEoggI46AdIM1gEaIwBiAEBmAENuAEXyAEP2AED6AEBiAIBqAIDuALsycKNBsACAdICJGE1YmJmNDE1LWU2ZTEtNGEzMy05MTcyLThkYmQ2OGI5NWE5OdgCBOACAQ&sid=dfa6ea4f57ded34b6271484b82f0e956&sb=1&sb_lp=1&src=theme_landing_index&src_elem=sb&ss=Canad%C3%A1&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&ss_raw=ma&ac_position=1&ac_langcode=xb&ac_click_type=b&dest_id=38&dest_type=country&place_id_lat=32.4281&place_id_lon=-6.92197&search_pageview_id=7ca057bb44b9012d&search_selected=true&search_pageview_id=7ca057bb44b9012d&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0"
        all_names = response.xpath('//div[@data-testid="title"]/text()').getall()
        for name in all_names:
            yield {'nom_hotel': name}
        
    def parse_detail(self, response):
        nom_hotel = response.css('h2#hp_hotel_name.hp__hotel-name::text').getall()
        nom_hotel = ''.join(nom_hotel)
        yield{
            'nom_hotel': nom_hotel.strip()
        }
        
process = CrawlerProcess(
    {
     'USER_AGENT':'Mozilla/4.0 (comatible;MSIE 7.0;Window NT 5.1)'
     })
process.crawl(DuProprioSpider)
process.start()


# https://stackoverflow.com/questions/70277389/scraping-from-booking-website-using-scrapy-the-file-csv-is-empty
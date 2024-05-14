import re
import time
import json
import gzip
from selenium import webdriver
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

class DeliveryFeeCalculator:
    def __init__(self):
        self.base_fee = 5
        self.fee_per_km = 1

    def calculate_delivery_fee(self, distance, time):
        distance_value = float(distance.split()[0])
        time_value = float(time.split()[0])

        distance_fee = distance_value * self.fee_per_km
        time_fee = time_value

        total_fee = self.base_fee + distance_fee + time_fee
        return total_fee

class GrabFoodScraper:
    def __init__(self):
        # Initialize scraper with base URL, WebDriver, and other parameters
        self.base_url = "https://food.grab.com/sg/en/restaurants"
        self.driver = webdriver.Chrome()
        self.scroll_pause_time = 3
        self.screen_height = self.driver.execute_script("return window.screen.height;")
        self.delivery_fee_calculator = DeliveryFeeCalculator()

    def scroll_page(self):
        # Scroll down the page to load more content
        i = 1
        while True:
            self.driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=self.screen_height, i=i))
            i += 1
            time.sleep(self.scroll_pause_time)
            scroll_height = self.driver.execute_script("return document.body.scrollHeight;")
            if (self.screen_height) * i > scroll_height:
                break

    def scrape_restaurant_data(self, div):
        # Scrape restaurant data from each div
        restaurant_name = div.find('p', class_='name___2epcT').text.strip()
        restaurant_cuisine = div.find('div', class_='cuisine___T2tCh').text.strip()
        rating_element = div.find('div', class_='ratingStar')
        restaurant_rating = rating_element.next_sibling.strip() if rating_element else "N/A"

        delivery_info_element = div.find('div', class_='numbers___2xZGn').find_all('div', class_='numbersChild___2qKMV')
        delivery_info = [item.get_text(strip=True) for item in delivery_info_element] if delivery_info_element else []
        estimated_delivery_time = "N/A"
        restaurant_distance = "N/A"
        estimate_delivery_fee = "N/A"

        if len(delivery_info) >= 2:
            delivery_info_string = delivery_info[1]
            pattern = r'(\d+)\s+mins\s+•\s+(\d+\.\d+)\s+km'
            match = re.search(pattern, delivery_info_string)
            if match:
                estimated_delivery_time = match.group(1) + " mins"
                restaurant_distance = match.group(2) + " km"
                distance_value = match.group(2)
                time_value = match.group(1)
                estimate_delivery_fee = self.delivery_fee_calculator.calculate_delivery_fee(distance_value, time_value)

        is_promo_available = bool(div.find('div', class_='promoTag___IYhfm'))
        restaurant_id = div.find('a')['href'].split('/')[-1].rstrip('?')
        image_link = div.find('img')['src']
        latitude_longitude = None

        # Create a dictionary containing restaurant information
        restaurant_info = {
            'name': restaurant_name,
            'cuisine': restaurant_cuisine,
            'rating': restaurant_rating,
            'delivery_time': estimated_delivery_time,
            'distance': restaurant_distance,
            'promo_available': is_promo_available,
            'restaurant_id': restaurant_id,
            'image_link': image_link,
            'latitude_longitude': latitude_longitude,
            'delivery_fee': estimate_delivery_fee
        }
        return restaurant_info

    def scrape_and_save_restaurant_data(self):
        # Main function to scrape and save restaurant data
        self.driver.get(self.base_url)
        time.sleep(2)
        self.scroll_page()
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        divs = soup.find_all('div', class_='RestaurantListCol___1FZ8V')

        # Use ThreadPoolExecutor to scrape data concurrently
        restaurant_data = []
        with ThreadPoolExecutor() as executor:
            for div in divs:
                restaurant_info = self.scrape_restaurant_data(div)
                restaurant_data.append(restaurant_info)

        # Save data to JSON file and JSON Gzip file
        json_data = json.dumps(restaurant_data, indent=4) 
        with open('restaurant_data.json', 'w') as json_file:
            json_file.write(json_data)

        with gzip.open('restaurant_data.json.gz', 'wt') as json_file:
            for restaurant_info in restaurant_data:
                json.dump(restaurant_info, json_file)
                json_file.write('\n')

if __name__ == "__main__":
    start = time.time()
    scraper = GrabFoodScraper()
    scraper.scrape_and_save_restaurant_data()
    end = time.time()
    print("Time taken: ", end - start)

import re
import time
import json
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin

start = time.time()

headers = {
    'authority': 'scrapeme.live',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

driver = webdriver.Chrome() 

driver.get(
    "https://food.grab.com/sg/en/restaurants")  

time.sleep(2)  
scroll_pause_time = 3  
screen_height = driver.execute_script("return window.screen.height;")  
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break


# creating soup
soup = BeautifulSoup(driver.page_source, "html.parser")
divs = soup.find_all('div', class_='RestaurantListCol___1FZ8V')

print("printing parsed html...")

restaurant_data = []

for div in divs:
    # Extracting restaurant name
    restaurant_name = div.find('p', class_='name___2epcT').text.strip()

    # Extracting restaurant cuisine
    restaurant_cuisine = div.find('div', class_='cuisine___T2tCh').text.strip()

    # Extracting restaurant rating
    rating_element = div.find('div', class_='ratingStar')
    if rating_element:
        restaurant_rating = rating_element.next_sibling.strip()
    else:
        restaurant_rating = "N/A"


    delivery_info_element = div.find('div', class_='numbers___2xZGn').find_all('div', class_='numbersChild___2qKMV')
    delivery_info = [item.get_text(strip=True) for item in delivery_info_element] if delivery_info_element else []

    estimated_delivery_time = "N/A"
    restaurant_distance = "N/A"

    if len(delivery_info) >= 2:
        # estimated_delivery_time = delivery_info[1]
        # # print("test : " + estimated_delivery_time)
        # restaurant_distance = delivery_info[1]
        # print("test : " + restaurant_distance)

        delivery_info_string = delivery_info[1]

        print("printing delivery info string : " + delivery_info_string)


        # Define the regex pattern to match the delivery time and distance
        pattern = r'(\d+)\s+mins\s+•\s+(\d+\.\d+)\s+km'

        # Search for the pattern in the string
        match = re.search(pattern, delivery_info_string)

        # Check if a match is found
        if match:
            # Extract delivery time and distance from the matched groups
            estimated_delivery_time = match.group(1) + " mins"
            restaurant_distance = match.group(2) + " km"
        else:
            # Handle the case where no match is found
            estimated_delivery_time = "N/A"
            restaurant_distance = "N/A"




    # Checking if promotional offers are listed for the restaurant
    is_promo_available = bool(div.find('div', class_='promoBadge___3tVSE'))

    # Extracting restaurant ID
    restaurant_id = div.find('a')['href'].split('/')[-2]

    # Extracting image link of the restaurant
    image_link = div.find('img')['src']

    # Extracting latitude and longitude of the restaurant (if available)
    # You may need to modify this part based on how latitude and longitude are structured in the HTML
    latitude_longitude = None  # Placeholder for latitude and longitude extraction

    # Extracting estimate delivery fee (if available)
    estimate_delivery_fee = None  # Placeholder for estimate delivery fee extraction

    # You can add code here to extract latitude, longitude, and delivery fee if available

    # Creating a dictionary to store the extracted information
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

    # Appending the restaurant info to the list
    restaurant_data.append(restaurant_info)


# Creating the JSON array
json_data = json.dumps(restaurant_data, indent=4)  # Convert Python list to JSON string with indentation

# Writing JSON data to a file
with open('restaurant_data.json', 'w') as json_file:
    json_file.write(json_data)

# Printing the JSON data
# print(json_data)



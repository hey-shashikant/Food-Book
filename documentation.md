# Documentation

## Approach
The script aims to scrape data from the GrabFood website (specifically, the Singapore restaurants section) including restaurant names, cuisines, ratings, delivery times, distances, promotional offers availability, restaurant IDs, image links, and estimated delivery fees. The data is then saved to both a JSON file and a JSON Gzip file for further analysis or storage.

## Implementation Details
- **DeliveryFeeCalculator Class:** Defines a class to calculate delivery fees based on distance and time.
- **GrabFoodScraper Class:** Implements a class to scrape restaurant data from the GrabFood website.
- **Scrolling Functionality:** Utilizes Selenium WebDriver to scroll down the page and load more content dynamically.
- **Data Scraping Functionality:** Scrapes restaurant data from each div containing restaurant information, using BeautifulSoup.
- **Concurrency:** Employs ThreadPoolExecutor for concurrent scraping of restaurant data to improve efficiency.
- **Data Storage:** Saves scraped data to a JSON file and a JSON Gzip file.

## Quality Control (QC)
- **Data Integrity Check:** Ensures that the scraped data fields are correctly parsed and formatted.
- **Null Value Check:** Verifies that mandatory fields such as restaurant name and cuisine are not null.
- **Promotional Offers Handling:** Identifies restaurants with promotional offers and handles them accordingly.

## Data Stats
- **Total Count:** [281]

## Challenges Faced
- **Dynamic Content Loading:** The GrabFood website loads content dynamically as the user scrolls down the page, requiring the use of Selenium WebDriver for scrolling.
- **Data Parsing Complexity:** Extracting relevant data from the HTML source required careful inspection of the DOM structure and regular expression matching.

## Future Improvements
- **Proxy Rotation:** Integrate proxy rotation to mitigate IP blocking and improve reliability.
- **Optimized Scrolling:** Explore techniques for optimized scrolling to reduce page load times and improve performance.

## Execution Steps
1. Install Python (if not already installed) and the required dependencies specified in the requirements.txt file.
2. Download the Chrome WebDriver compatible with your Chrome browser version.
3. Update the Chrome WebDriver path in the script if necessary.
4. Run the script locally using a Python interpreter.
5. Monitor the console output for any errors or exceptions and review the generated JSON files containing the scraped data.

Feel free to adjust the documentation as needed to fit your specific requirements and preferences.

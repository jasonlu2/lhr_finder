# Marathon Time Analysis Tool

## Project Overview

Since its inception in 2010, Longhorn Run has become a campus tradition that unites students, faculty, staff, alumni, and the Austin community during the spring semester. Produced through the combined efforts of the Longhorn Run student committee and Recreational Sports, the race offers 5K and 10K courses that start on the UT campus and run through campus and surrounding areas. Proceeds from the race benefit the UT Student Government and Recreational Sports Excellence Funds.

This project scrapes marathon race times from MyChipTime, analyzes the data using binary search, and visualizes the results. Input your marathon time and category to see your ranking against other runners in different categories and distances.

## Features

- **Data Scraping**: Collect marathon race times from the specified website.
- **Binary Search**: Efficiently determine your placement based on your race time.
- **Data Visualization**: Plot the distribution of run times and highlight your race time.

## How It Works

1. **Scraping the Data**: 
   - Sends an HTTP GET request to the marathon results page specified in the `run_dict`.
   - Parses the HTML content to extract race times using BeautifulSoup.

2. **Processing the Data**:
   - Converts race times from strings to integers for easier analysis.
   - Splits the times into male and female categories.

3. **Binary Search**:
   - Uses binary search to find the placement of a given race time among the scraped times.

4. **Data Visualization**:
   - Uses Matplotlib and Seaborn to create a boxplot of the distribution of run times.
   - Highlights the user’s race time on the plot.

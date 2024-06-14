no financial advice. godspeed lol
# 4chan Market Analysis Tool

## Overview

The 4chan Market Analysis Tool is a desktop application designed to analyze the sentiment of posts on 4chan boards related to specific keywords. The tool leverages sentiment analysis and asynchronous data fetching to provide real-time insights and trends. It also fetches the current price of the keyword (if it's a cryptocurrency) and the latest news headlines related to the keyword.

## Features

- **Sentiment Analysis**: Analyzes the sentiment (positive, negative, neutral) of comments containing the specified keyword.
- **Real-Time Data**: Fetches posts from 4chan boards asynchronously to provide up-to-date information.
- **Cryptocurrency Price**: Retrieves the current price of the specified keyword if it corresponds to a cryptocurrency.
- **Latest News**: Provides the latest news headlines related to the keyword using Google News RSS feed.
- **Interactive GUI**: User-friendly graphical interface built with Tkinter.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Appreciatorof69/4chan-market-analysis-tool.git
    cd 4chan-market-analysis-tool
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```bash
    python 4chan_market_analysis_tool.py
    ```

2. Enter the desired 4chan board (e.g., `biz` for Business & Finance).

3. Enter the keyword you want to analyze (e.g., `btc` for Bitcoin).

4. Choose the display option (All Comments or Random Comments).

5. Click "Perform Analysis" to start the sentiment analysis and view the results.

## Dependencies

- `tkinter`: For the graphical user interface.
- `requests`: For fetching cryptocurrency prices and news headlines.
- `aiohttp`: For asynchronous HTTP requests to fetch 4chan posts.
- `textblob`: For performing sentiment analysis.
- `matplotlib`: For plotting sentiment trends.
- `feedparser`: For parsing RSS feeds from Google News.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

Free af. Idc lol. enjoy and hopefully profit. no financial advice. godspeed lol


## Acknowledgements

- The 4chan API for providing access to board data.
- CoinGecko API for cryptocurrency price information.
- Google News RSS feed for news headlines.
- The developers of TextBlob, aiohttp, and other libraries used in this project.

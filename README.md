no financial advice
# 4chan Market Analysis Tool

![grafik](https://github.com/Appreciatorof69/4chan-Market-Analysis-Tool/assets/124309106/57d7ac01-234a-4f96-8684-e5dad64bb5b3)



Features

    Keyword Extraction: Extracts comments containing certain keywords from specified 4chan boards.
    Crypto Price Check: Fetches current cryptocurrency prices from various exchanges.
    News Aggregation: Pulls relevant news articles related to the extracted keywords and cryptocurrencies.

Known Issues

    There is a known bug where the tool sometimes confuses keywords (e.g., using "BTC" instead of "bitcoin" or "solana" instead of "SOL"). I don't know why.

## Requirements

- Python 3.7+
- tkinter: GUI toolkit for Python standard library.
- messagebox: Part of tkinter for creating message boxes.
- ttk: Another part of tkinter for themed widgets.
- requests: HTTP library for making requests.
- Thread (from threading): For threading operations.
- asyncio: Asynchronous I/O, event loop, and coroutines.
- aiohttp: Asynchronous HTTP client/server framework.
- random: Python's built-in random number generator.
- pandas: Data analysis library for handling structured data.
- TextBlob: Library for processing textual data, including sentiment analysis.
- nltk: Natural Language Toolkit for various NLP tasks.
- matplotlib: Plotting library for creating visualizations.
- re: Regular expressions for pattern matching in strings.
- BeautifulSoup: Library for web scraping

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Appreciatorof69/4chan-market-analysis-tool.git
   cd 4chan-market-analysis-tool
   ```

2. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```sh
   python 4chan_market_analysis_tool.py
   ```

2. Enter the 4chan board name (e.g., `biz` for Business & Finance) and the keyword (e.g., `bitcoin` for Bitcoin) in the GUI.
3. Select the display option (either "All Comments" or "Random Comments").
4. Click on "Perform Analysis" to fetch and analyze the data.
5. The generated prompt for ChatGPT will be displayed in the text box at the bottom of the GUI.


## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- [4chan](https://www.4chan.org) for providing the data source.
- [CoinGecko](https://www.coingecko.com) for the cryptocurrency price API.
- [Google News](https://news.google.com) for the RSS feed.

Feel free to contribute to this project by opening issues or submitting pull requests on the [GitHub repository](https://github.com/yourusername/4chan-market-analysis-tool).

no financial advice
# 4chan Market Analysis Tool

This tool allows you to analyze 4chan boards for posts containing specific keywords, fetch the current price of the keyword (if it's a cryptocurrency), and retrieve the latest news about the keyword using Google News RSS feed. The results can be displayed in various formats, and a prompt is generated for ChatGPT evaluation.

## Features

- Asynchronously fetch and filter posts from a specified 4chan board.
- Retrieve the current price of a cryptocurrency keyword using the CoinGecko API.
- Fetch the latest news related to the keyword using Google News RSS feed.
- Display the filtered posts and generate a prompt for sentiment analysis using ChatGPT.

## Requirements

- Python 3.7+
- `tkinter`
- `requests`
- `aiohttp`
- `feedparser`

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/4chan-market-analysis-tool.git
   cd 4chan-market-analysis-tool
   ```

2. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```sh
   python main.py
   ```

2. Enter the 4chan board name (e.g., `biz` for Business & Finance) and the keyword (e.g., `btc` for Bitcoin) in the GUI.
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

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
from threading import Thread
import asyncio
import aiohttp
import random
import pandas as pd
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import sentiwordnet as swn
from nltk import download as nltk_download
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re
from bs4 import BeautifulSoup

# Ensure NLTK resources are downloaded
nltk_download('vader_lexicon')
nltk_download('sentiwordnet')
nltk_download('wordnet')

# Initialize VADER sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Function to get posts from a specific 4chan board using asynchronous requests
async def fetch_thread_data(session, url):
    async with session.get(url) as response:
        return await response.json()

async def get_posts_from_board_async(board, keyword):
    base_url = f'https://a.4cdn.org/{board}/catalog.json'
    async with aiohttp.ClientSession() as session:
        response = await session.get(base_url)
        if response.status != 200:
            return []

        threads = await response.json()
        filtered_posts = []

        thread_urls = [f'https://a.4cdn.org/{board}/thread/{thread["no"]}.json' for page in threads for thread in page['threads']]
        tasks = [fetch_thread_data(session, url) for url in thread_urls]

        for thread_data in await asyncio.gather(*tasks):
            for post in thread_data['posts']:
                if 'com' in post:
                    comment = post['com']
                    if keyword.lower() in comment.lower():
                        poster_id = post.get('id', 'N/A')  # Get poster ID if available
                        filtered_posts.append({
                            'date': post['now'],
                            'comment': comment,
                            'poster_id': poster_id
                        })

        return filtered_posts

# Function to fetch the current price of the keyword
def fetch_current_price(keyword):
    url = 'https://api.coingecko.com/api/v3/coins/list'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        coins = response.json()
        # Find the coin ID for the given keyword
        coin_id = None
        for coin in coins:
            if coin['symbol'].lower() == keyword.lower() or coin['id'].lower() == keyword.lower():
                coin_id = coin['id']
                break
        if not coin_id:
            return 'N/A'
        
        price_url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd'
        price_response = requests.get(price_url)
        price_response.raise_for_status()
        price_data = price_response.json()
        return price_data.get(coin_id, {}).get('usd', 'N/A')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching price: {e}")
        return 'N/A'

# Function to clean the text data
def clean_text(text):
    text = BeautifulSoup(text, "html.parser").get_text()  # Remove HTML tags
    text = text.lower()  # Convert to lowercase
    return text

# Function to analyze sentiments
def analyze_sentiments(posts):
    unique_posts = {post['poster_id']: clean_text(post['comment']) for post in posts}

    sentiment_results = {
        'Poster ID': [],
        'Comment': [],
        'TextBlob Sentiment': [],
        'VADER Sentiment': [],
        'SentiWordNet Sentiment': [],
        'Final Sentiment': []
    }

    for poster_id, comment in unique_posts.items():
        # TextBlob analysis
        tb_analysis = TextBlob(comment)
        if tb_analysis.sentiment.polarity > 0:
            tb_sentiment = 'Positive'
        elif tb_analysis.sentiment.polarity == 0:
            tb_sentiment = 'Neutral'
        else:
            tb_sentiment = 'Negative'

        # VADER analysis
        vader_scores = sid.polarity_scores(comment)
        if vader_scores['compound'] > 0.1:  # Adjusted threshold for positive sentiment
            vader_sentiment = 'Positive'
        elif -0.1 <= vader_scores['compound'] <= 0.1:  # Adjusted threshold for neutral sentiment
            vader_sentiment = 'Neutral'
        else:
            vader_sentiment = 'Negative'

        # SentiWordNet analysis
        senti_score = 0
        words = comment.split()
        for word in words:
            synsets = list(swn.senti_synsets(word))
            if synsets:
                senti_syn = synsets[0]
                senti_score += senti_syn.pos_score() - senti_syn.neg_score()
        if senti_score > 0.1:  # Adjusted threshold for positive sentiment
            senti_sentiment = 'Positive'
        elif -0.1 <= senti_score <= 0.1:  # Adjusted threshold for neutral sentiment
            senti_sentiment = 'Neutral'
        else:
            senti_sentiment = 'Negative'

        # Determine final sentiment by majority vote
        sentiments = [tb_sentiment, vader_sentiment, senti_sentiment]
        final_sentiment = max(set(sentiments), key=sentiments.count)

        # Append results
        sentiment_results['Poster ID'].append(poster_id)
        sentiment_results['Comment'].append(comment)
        sentiment_results['TextBlob Sentiment'].append(tb_sentiment)
        sentiment_results['VADER Sentiment'].append(vader_sentiment)
        sentiment_results['SentiWordNet Sentiment'].append(senti_sentiment)
        sentiment_results['Final Sentiment'].append(final_sentiment)

    df_results = pd.DataFrame(sentiment_results)
    return df_results

# Function to log keywords and their sentiments
def log_keywords_and_sentiment(board, keyword, posts, display_option):
    if not posts:
        messagebox.showerror("Error", "No posts found or failed to retrieve data.")
        return

    current_price = fetch_current_price(keyword)
    df = analyze_sentiments(posts)

    if display_option == 'All Comments':
        comments_summary = '\n'.join(f"[{post['poster_id']}] {clean_text(post['comment'])}" for post in posts)
    elif display_option == 'Random Comments':
        random_comments = random.sample(posts, min(len(posts), 5))  # Display up to 5 random comments
        comments_summary = '\n'.join(f"[{post['poster_id']}] {clean_text(post['comment'])}" for post in random_comments)
    else:
        comments_summary = 'Invalid display option.'

    prompt_text = (
        f"Evaluate the sentiment for the keyword '{keyword}'. "
        f"How many are positive, negative, neutral, off-topic? "
        f"The current price is {current_price}. "
        f"Here are the comments:\n{comments_summary}"
    )

    prompt_entry.delete('1.0', tk.END)
    prompt_entry.insert(tk.END, prompt_text)

    # Move the display_results function call to the main thread
    root.after(0, display_results, df)

# Function to display sentiment analysis results in table format
def display_results(df):
    sentiment_counts = {
        'TextBlob': df['TextBlob Sentiment'].value_counts(),
        'VADER': df['VADER Sentiment'].value_counts(),
        'SentiWordNet': df['SentiWordNet Sentiment'].value_counts(),
        'Final': df['Final Sentiment'].value_counts()
    }

    fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(20, 5))

    for i, (title, counts) in enumerate(sentiment_counts.items()):
        counts.plot(kind='bar', ax=axes[i], color=['green' if x == 'Positive' else 'red' if x == 'Negative' else 'grey' for x in counts.index])
        axes[i].set_title(f'{title} Sentiments')
        axes[i].set_xlabel('Sentiment')
        axes[i].set_ylabel('Count')

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=9, column=0, columnspan=2)

# Function to perform the analysis asynchronously
def perform_analysis_async():
    board = board_entry.get()
    keyword = keyword_entry.get()
    display_option = display_option_var.get()
    if not board or not keyword:
        messagebox.showerror("Error", "Please enter both board and keyword.")
        return
    
    # Show loading message
    loading_label.config(text="Loading...")
    analyze_button.config(state=tk.DISABLED)
    
    def analyze():
        try:
            # Get or create a new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            posts = loop.run_until_complete(get_posts_from_board_async(board, keyword))
            log_keywords_and_sentiment(board, keyword, posts, display_option)
        finally:
            # Hide loading message
            loading_label.config(text="")
            analyze_button.config(state=tk.NORMAL)
    
    # Start the analysis in a separate thread to avoid freezing the GUI
    thread = Thread(target=analyze)
    thread.start()

# Function to copy the prompt text to the clipboard
def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(prompt_entry.get("1.0", tk.END))
    messagebox.showinfo("Clipboard", "Text copied to clipboard!")

# GUI setup
root = tk.Tk()
root.title("4chan Market Analysis Tool")

# Main frame
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Grid configuration
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=3)

# Tooltips
def create_tooltip(widget, text):
    tooltip = tk.Toplevel(widget)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry("+0+0")
    label = tk.Label(tooltip, text=text, background="yellow", relief='solid', borderwidth=1, font=("Arial", 10, "normal"))
    label.pack()
    tooltip.withdraw()

    def enter(event):
        tooltip.deiconify()
        x = event.x_root + 20
        y = event.y_root
        tooltip.wm_geometry(f"+{x}+{y}")

    def leave(event):
        tooltip.withdraw()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

# Board entry
ttk.Label(main_frame, text="Enter board:").grid(row=0, column=0, sticky=tk.W, pady=5)
board_entry = ttk.Entry(main_frame)
board_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
create_tooltip(board_entry, "Enter the 4chan board name, e.g., 'biz' for Business & Finance")

# Keyword entry
ttk.Label(main_frame, text="Enter keyword:").grid(row=1, column=0, sticky=tk.W, pady=5)
keyword_entry = ttk.Entry(main_frame)
keyword_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
create_tooltip(keyword_entry, "Enter the keyword to search for, e.g., 'btc' for Bitcoin")

# Display option
ttk.Label(main_frame, text="Display option:").grid(row=2, column=0, sticky=tk.W, pady=5)
display_option_var = tk.StringVar(value="All Comments")
display_option_all = ttk.Radiobutton(main_frame, text="All Comments (Analyze all comments containing the keyword)", variable=display_option_var, value="All Comments")
display_option_random = ttk.Radiobutton(main_frame, text="Random Comments (Analyze a random sample of comments containing the keyword)", variable=display_option_var, value="Random Comments")
display_option_all.grid(row=2, column=1, sticky=tk.W, pady=2)
display_option_random.grid(row=3, column=1, sticky=tk.W, pady=2)

# Loading label
loading_label = ttk.Label(main_frame, text="", foreground="red")
loading_label.grid(row=4, column=0, columnspan=2, pady=5)

# Analysis button
analyze_button = ttk.Button(main_frame, text="Perform Analysis", command=perform_analysis_async)
analyze_button.grid(row=5, column=0, columnspan=2, pady=20)

# Prompt entry
ttk.Label(main_frame, text="Generated Prompt for ChatGPT:").grid(row=6, column=0, columnspan=2, pady=5)
prompt_entry = tk.Text(main_frame, height=10, width=80)
prompt_entry.grid(row=7, column=0, columnspan=2, pady=5)

# Copy to clipboard button
copy_button = ttk.Button(main_frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=8, column=0, columnspan=2, pady=5)

# Run the application
root.mainloop()

# Steam Games Dashboard: Data Cleaning & ETL Pipeline

I am building an interactive market analysis dashboard using a massive dataset of Steam games (updated March 2025). 

However, raw platform data is notoriously messy and huge. Before loading anything into Power BI or Tableau, I needed to build a Python pipeline to clean the data, fix formatting issues, and drop gigabytes of unnecessary text bloat so the dashboard runs smoothly.

Here is a breakdown of how I prepared the data.

---

## 1. Trimming the Fat (Dropped Columns)

The original dataset had 47 columns. I dropped 30 of them to keep the file lightweight and focused entirely on macro business and player metrics. 

Here is what I removed and why:
* **Massive Text Blocks:** `detailed_description`, `about_the_game`, `short_description`, `reviews`, and `notes`. These are huge paragraphs of text that crash BI tools and can't be charted anyway.
* **Web Links & Media:** `header_image`, `website`, `support_url`, `screenshots`, etc. 
* **Niche Hardware Specs:** `windows`, `mac`, `linux`, `supported_languages`. I am focusing on global market trends, not hardware compatibility.
* **Old 2-Week Snapshots:** `average_playtime_2weeks`, `pct_pos_recent`, etc. Since I am going to connect this dashboard to live Steam APIs later, I didn't want these static 14-day snapshots clashing with my live real-time data.
* **Redundant Scores:** `metacritic_score` and `user_score`. Steam's total review percentage is a much more accurate representation of how players feel about a game.

---

## 2. The Core Data (What I Kept)

I narrowed the dataset down to 17 essential columns that map directly to my target dashboard pages:

* **Identifiers:** `appid` (this will be my key to connect live API data later) and `name`.
* **Financials:** `release_date`, `price`, and `estimated_owners` to map revenue trends.
* **Market Share:** `developers`, `publishers`, `categories`, `genres`, and `tags` to build market category charts.
* **Player Retention:** `average_playtime_forever`, `median_playtime_forever`, and `peak_ccu` to track historical engagement.
* **Sentiment:** `positive`, `negative`, `pct_pos_total`, and `num_reviews_total` to build a "Hidden Gem" discovery filter.

---

## 3. Data Cleaning & Python Fixes

Loading the raw CSV directly would have caused a ton of errors due to bad formatting. I wrote a Pandas script to process the data in chunks and fix these three major issues:

### Fixing the "Estimated Owners" Text Ranges
The original file listed owners as text strings like `100000000 - 200000000` or `50,000 .. 100,000`. You cannot do math on text. I wrote a custom parser to strip out the punctuation, find the high and low numbers, and calculate the true midpoint (e.g., `150000000`). This allows my dashboard to actually calculate estimated gross revenue.

### Cleaning Up the Array Brackets
Columns like genres and developers were formatted as raw lists of code (e.g., `['Action', 'Free To Play']`). If I left this alone, the dashboard drop-down menus would literally show the brackets. I added a quick sanitization step to strip those out into clean text (e.g., `Action, Free To Play`).

### Fixing the Missing Review Scores (-1)
Games that were too new to have a review score were assigned a `-1` in the data. If left alone, these negative numbers would completely warp the platform-wide averages. I added a mask to replace all `-1` flags with `0`.

---

## Next Steps
* [x] **Step 1:** Clean the raw CSV, fix data types, and export a lightweight file.
* [ ] **Step 2:** Import `games_march2025_small.csv` into the BI tool and build the 5-page dashboard layout.
* [ ] **Step 3:** Write a Python script using the `requests` library to ping the Steam Web API and SteamSpy, grabbing live player counts for these specific `appid`s.
# 🎵 Eska Rap 20 - Spotify Bot

A Python bot designed to automatically update a Spotify playlist based on the weekly **Eska Rap 20** chart ranking from the Polish radio station Eska. It scrapes the current chart, finds the corresponding tracks on Spotify, and updates the playlist with the latest top songs.

Built with **Python**, **BeautifulSoup4**, and **Spotipy**.

## 🚀 Features

- 📈 Scrapes the current Eska Rap 20 chart from [Eska's website](https://www.eska.pl/rap20/).
- 🔍 Searches for the scraped tracks on Spotify using the Spotipy library.
- 🔄 Automatically updates a specified Spotify playlist with the latest top 20 tracks.
- ⚙️ Configurable via environment variables for secure API key handling.
- 📅 Designed to be scheduled for regular automatic updates (e.g., weekly).

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/SzymLeg/spotify-bot-eska-rap-20.git](https://github.com/SzymLeg/spotify-bot-eska-rap-20.git)
    cd eska-rap-20-spotify-bot
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Setup Spotify API credentials:**
    * Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
    * Log in and create a new application.
    * Note down your **Client ID** and **Client Secret**.
    * Edit the settings of your app and add `http://localhost:8888/callback` as a **Redirect URI**.
    * Create a file named `.env` in the root directory of the project and add the following lines, replacing the placeholders with your credentials:
        ```ini
        SPOTIPY_CLIENT_ID=your_client_id
        SPOTIPY_CLIENT_SECRET=your_client_secret
        SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
        SPOTIPY_PLAYLIST_ID=your_playlist_id # Optional: If you want to use an existing playlist ID
        ```
        *Note: Replace `your_playlist_id` with the ID of the Spotify playlist you want to update. If left empty or omitted, the script might create a new playlist.*

5.  **Run the bot for the first time:**
    ```bash
    python main.py
    ```
    This will initiate the Spotify authentication flow in your browser. After successful authentication, the script will proceed to fetch the chart, search for songs, and update/create the playlist.

## 📅 Scheduling Updates

To keep your playlist automatically updated weekly, you can schedule the `main.py` script to run regularly using a system task scheduler:

* **Linux/macOS:** Use `cron`.
    ```bash
    crontab -e
    ```
    Add a line like this to run the script every Monday at 23:30 (adjust the path to your project directory):
    ```cron
    30 23 * * 1 /path/to/your/venv/bin/python /path/to/your/eska-rap-20-spotify-bot/main.py
    ```
* **Windows:** Use Task Scheduler. Create a basic task that runs weekly, pointing to your Python executable in the virtual environment and the `main.py` script.

## ❓ Troubleshooting

* **Authentication Issues:** Double-check your `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`, and `SPOTIPY_REDIRECT_URI` in the `.env` file against your Spotify Developer Dashboard. Ensure the redirect URI exactly matches the one in your app settings.
* **Song Not Found:** The bot relies on Spotify's search functionality. Some tracks from the chart might not be available on Spotify or the search query might not yield the correct result.
* **Scraping Errors:** If Eska changes the structure of their "Rap 20" webpage, the web scraping logic in the bot might fail. You may need to update the scraping code (`beautifulsoup4` part) to match the new website structure.
* **Playlist Updates:** Ensure the Spotify account used for authentication has the necessary permissions to modify the target playlist. If using `SPOTIPY_PLAYLIST_ID`, make sure the ID is correct and belongs to the authenticated user's account.

## 📁 Project Structure

```bash
eska-rap-20-spotify-bot/
├── main.py           # Main script to run the bot logic
├── requirements.txt  # List of project dependencies
├── .env              # Environment file for API credentials (add to .gitignore!)
└── README.md         # Project documentation
```

## 🛡️ License
This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and share this project with proper attribution.

## ℹ️ About Me

Hi there! I'm **Szymon Legierski**, also known as **SzymLeg**. I'm an IT student and passionate about Data Engineering!

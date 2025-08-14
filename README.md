# SpotifyToYTMusic

A Python script to copy selected playlists from Spotify to YouTube Music.

## Description

This script allows users to transfer their Spotify playlists to YouTube Music. It retrieves all playlists from a Spotify account, prompts the user to select which ones to copy, and creates equivalent playlists in YouTube Music by matching tracks as closely as possible.

## Setup Instructions

1. **Obtain Spotify Credentials**:
   - Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
   - Log in with your Spotify account and click "Create an App."
   - Provide random details (name, description, etc.).
   - Add `http://localhost:8888/callback` as a Redirect URI in the app settings and save.
   - Note your **Client ID** and **Client Secret** for use when prompted by the script.

2. **YouTube Music Authentication**:
   - Install `ytmusicapi`: `pip install ytmusicapi`.
   - Run `ytmusicapi browser` in your terminal and paste the YouTube `/youtubei/v1/log_event` headers as prompted.
   - This generates a `browser.json` file. Place it in the same directory as the script or specify its path when prompted.

3. **Requirements**:
   - Python 3.6 or higher.
   - Install dependencies
   - A Spotify account with playlists.
   - A Google account for YouTube Music.
   

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/SpotifyToYTMusic.git
   cd SpotifyToYTMusic
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have a `browser.json` file for YouTube Music authentication (see setup instructions above).

## Usage

1. Run the script:
   ```bash
   python yt.py
   ```

2. Follow the prompts:
   - Enter your Spotify **Client ID** and **Client Secret**.
   - Specify the path to your YouTube Music `browser.json` file (or press Enter to use the default `browser.json` in the script's directory).
   - The script will list all your Spotify playlists with their track counts.
   - For each playlist, enter `y` to copy it to YouTube Music or `n` to skip it.

3. The script will:
   - Authenticate with Spotify and YouTube Music.
   - Create a private playlist in YouTube Music for each selected Spotify playlist.
   - Match tracks using song title and artist, adding them to the new playlist.
   - Report any tracks that could not be matched.

## Example Output

```
Spotify to YouTube Music (by K43M1S)

This script copies selected playlists from Spotify to YouTube Music.

Setup Instructions:
[...]

Enter your Spotify and YouTube Music credentials:
Spotify Client ID: your_client_id_here
Spotify Client Secret: your_client_secret_here
Path to YouTube Music browser.json (default: browser.json): browser.json
[*] Authenticating with Spotify...
[*] Spotify authentication successful.
[*] Authenticating with YouTube Music...
[*] YouTube Music authentication successful.
[*] Found 3 playlists on Spotify:
  1. My Favorites (25 tracks)
  2. Chill Vibes (10 tracks)
  3. Workout Jams (15 tracks)

Do you want to copy playlist 'My Favorites' (25 tracks)? (y/n): y
[*] Copying playlist: My Favorites
[+] Matched: Song 1 - Artist A
[!] Could not match: Song 2 - Artist B
...
[*] Added 20 tracks to My Favorites.
[!] 5 tracks could not be matched: Song 2 - Artist B, ...

Do you want to copy playlist 'Chill Vibes' (10 tracks)? (y/n): n
[*] Skipped: Chill Vibes

Do you want to copy playlist 'Workout Jams' (15 tracks)? (y/n): y
...

[*] Playlist copy process finished.
```

## Notes

- **Authentication Cache**: Spotify authentication tokens are stored in a `.spotify_cache` file. If you encounter authentication issues, delete this file and rerun the script.
- **Rate Limits**: The script includes a 0.5-second delay between track searches to avoid API rate limits. If you encounter `429 Too Many Requests` errors, increase the `time.sleep(0.5)` value in the `copy_playlist` function.
- **Track Matching**: The script uses `python-Levenshtein` for fuzzy matching of song titles. If you prefer not to install it, modify the `search_song_ytmusic` function to use the first search result, though this may reduce accuracy.
- **YouTube Music Auth**: Ensure `browser.json` is valid. If authentication fails, rerun `ytmusicapi browser` to regenerate the file.
- **Redirect URI**: The Spotify Redirect URI (`http://localhost:8888/callback`) must match exactly in the Spotify Developer Dashboard and the script.

## Troubleshooting

- **Invalid Client Secret**: Verify your Client ID and Client Secret in the Spotify Developer Dashboard. Copy them exactly, avoiding extra spaces.
- **Redirect URI Error**: Ensure `http://localhost:8888/callback` is listed in your Spotify app’s Redirect URIs.
- **YouTube Music Auth Error**: If `browser.json` is missing or invalid, rerun `ytmusicapi browser`.
- **No Playlists Found**: Confirm your Spotify account has playlists (private playlists are included with the `playlist-read-private` scope).

## Contributing

Contributions are welcome! Please submit a pull request or open an issue on GitHub to suggest improvements or report bugs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Created by K43M1S.
- Built with [spotipy](https://spotipy.readthedocs.io/) and [ytmusicapi](https://ytmusicapi.readthedocs.io/).

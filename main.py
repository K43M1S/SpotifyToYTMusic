import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
from difflib import get_close_matches
import time
import sys
import os

def print_introduction():
    print("""
Spotify to YouTube Music (by K43M1S)

This script copies selected playlists from Spotify to YouTube Music.

Setup Instructions:

1. Obtain Spotify Credentials:
   - Visit Spotify Developer Dashboard: https://developer.spotify.com/dashboard
   - Log in with your Spotify account and click "Create an App."
   - Provide random details (name, description, etc.).
   - Add http://localhost:8888/callback as a Redirect URI in the app settings and save.
   - When prompted by this script, enter your Client ID and Client Secret.

2. YouTube Music Authentication:
   - Run `ytmusicapi browser` in your terminal and paste youtube "/youtubei/v1/log_event" haeders.
   - This generates an browser.json file. Place it in the same directory as this script or specify its path when prompted.

3. Requirements:
   - pip install spotipy ytmusicapi python-Levenshtein
   - Python 3.6 or higher
   - A Spotify account with playlists
   - A Google account for YouTube Music

Usage:
Run the script, enter your Spotify Client ID, Client Secret, and YouTube Music auth file path when prompted.
The script will list all your Spotify playlists and ask if you want to copy each one to YouTube Music.
""")

def initialize_spotify_client(client_id, client_secret, redirect_uri, scope):
    try:
        print("[*] Authenticating with Spotify...")
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            cache_path=".spotify_cache"  # Store OAuth token for reuse
        ))
        # Test authentication
        sp.current_user()
        print("[*] Spotify authentication successful.")
        return sp
    except Exception as e:
        print(f"[!] Spotify authentication failed: {e}")
        sys.exit(1)

def initialize_youtube_music_client(auth_file):
    try:
        print("[*] Authenticating with YouTube Music...")
        if not os.path.exists(auth_file):
            print(f"[!] YouTube Music auth file '{auth_file}' not found. Run 'ytmusicapi setup' to create it.")
            sys.exit(1)
        yt = YTMusic(auth_file)
        print("[*] YouTube Music authentication successful.")
        return yt
    except Exception as e:
        print(f"[!] YouTube Music authentication failed: {e}")
        sys.exit(1)

def get_all_spotify_playlists(sp):
    try:
        playlists = []
        results = sp.current_user_playlists(limit=50)
        while results:
            playlists.extend(results["items"])
            if results["next"]:
                results = sp.next(results)
            else:
                break
        return playlists
    except Exception as e:
        print(f"[!] Error fetching Spotify playlists: {e}")
        return []

def get_spotify_playlist_tracks(sp, playlist_id):
    try:
        tracks = []
        results = sp.playlist_tracks(playlist_id, fields="items(track(name,artists(name),id)),next")
        while results:
            tracks.extend(results["items"])
            if results["next"]:
                results = sp.next(results)
            else:
                break
        return tracks
    except Exception as e:
        print(f"[!] Error fetching tracks for playlist {playlist_id}: {e}")
        return []

def search_song_ytmusic(yt, title, artist):
    try:
        query = f"{title} {artist}"
        search_results = yt.search(query, filter="songs", limit=10)
        if not search_results:
            search_results = yt.search(title, filter="songs", limit=10)

        if not search_results:
            print(f"[!] No match found for: {title} - {artist}")
            return None

        candidate_titles = [song["title"] for song in search_results]
        best_matches = get_close_matches(title, candidate_titles, n=1, cutoff=0.6)

        if best_matches:
            match_title = best_matches[0]
            for song in search_results:
                if song["title"] == match_title:
                    return song["videoId"]
        else:
            return search_results[0]["videoId"]
    except Exception as e:
        print(f"[!] Error searching YouTube Music for {title} - {artist}: {e}")
        return None

def copy_playlist(sp, yt, playlist):
    playlist_name = playlist["name"]
    playlist_id = playlist["id"]
    print(f"\n[*] Copying playlist: {playlist_name}")

    try:
        yt_playlist_id = yt.create_playlist(
            title=playlist_name,
            description=f"Copied from Spotify: {playlist_name}",
            privacy_status="PRIVATE"
        )
        if not yt_playlist_id:
            print(f"[!] Failed to create YouTube Music playlist: {playlist_name}")
            return

        tracks = get_spotify_playlist_tracks(sp, playlist_id)
        yt_video_ids = []
        unmatched_tracks = []

        for item in tracks:
            track = item.get("track")
            if not track or not track.get("name") or not track.get("artists"):
                continue
            title = track["name"]
            artist = track["artists"][0]["name"]

            video_id = search_song_ytmusic(yt, title, artist)
            if video_id:
                yt_video_ids.append(video_id)
                print(f"[+] Matched: {title} - {artist}")
            else:
                unmatched_tracks.append(f"{title} - {artist}")
                print(f"[!] Could not match: {title} - {artist}")

            time.sleep(0.5)

        if yt_video_ids:
            try:
                yt.add_playlist_items(yt_playlist_id, yt_video_ids)
                print(f"[*] Added {len(yt_video_ids)} tracks to {playlist_name}.")
                if unmatched_tracks:
                    print(f"[!] {len(unmatched_tracks)} tracks could not be matched: {', '.join(unmatched_tracks)}")
            except Exception as e:
                print(f"[!] Error adding tracks to YouTube Music playlist {playlist_name}: {e}")
        else:
            print(f"[!] No tracks added to {playlist_name} (no matches found).")

    except Exception as e:
        print(f"[!] Error copying playlist {playlist_name}: {e}")


########## MAIN ##########
if __name__ == "__main__":

    #Intro
    print_introduction()
    input("Press Enter to continue...")

    # Get user credentials
    print("Enter your Spotify and YouTube Music credentials:")
    spotify_client_id = input("Spotify Client ID: ").strip()
    spotify_client_secret = input("Spotify Client Secret: ").strip()
    spotify_redirect_uri = "http://localhost:8888/callback"
    spotify_scope = "playlist-read-private"
    ytmusic_auth_file = input("Path to YouTube Music browser.json (default: browser.json): ").strip() or "browser.json"

    sp = initialize_spotify_client(spotify_client_id, spotify_client_secret, spotify_redirect_uri, spotify_scope)
    yt = initialize_youtube_music_client(ytmusic_auth_file)

    # Fetch playlists
    playlists = get_all_spotify_playlists(sp)
    if not playlists:
        print("[!] No playlists found or error occurred. Exiting.")
        sys.exit(1)
    
    print(f"[*] Found {len(playlists)} playlists on Spotify:")
    for i, playlist in enumerate(playlists, 1):
        print(f"  {i}. {playlist['name']} ({playlist['tracks']['total']} tracks)")

    # Copy selected playlists
    for playlist in playlists:
        try:
            choice = input(f"\nDo you want to copy playlist '{playlist['name']}' ({playlist['tracks']['total']} tracks)? (y/n): ").strip().lower()
            if choice == "y":
                copy_playlist(sp, yt, playlist)
            else:
                print(f"[*] Skipped: {playlist['name']}")
        except KeyboardInterrupt:
            print("\n[!] User interrupted the process. Exiting.")
            sys.exit(0)
        except Exception as e:
            print(f"[!] Error processing playlist {playlist['name']}: {e}")

    print("\n[*] Playlist copy process finished.")

import aiohttp
import http
from bs4 import BeautifulSoup
import asyncio
import requests
import pandas as pd
import re, time
import pickle
import json
import steam_tags_f as stf


def add_appid (df, dict):
    df2 = df.copy()
    for index, row in df2.iterrows():
        title = row[0]  
        app_id = dict.get(title.strip())
        if app_id:
            df2.at[index, df2.columns[1]] = app_id
        else:
            df2.at[index, df2.columns[1]] = "Not Found"
    return df2


def check_multiplayer_single(game_id):
    response = requests.get(f"http://store.steampowered.com/api/appdetails?appids={game_id}")
    game = response.json()
    categories = game[game_id]["data"]["categories"]
    mp_list = []
    mp_dict= {}
    # Check if "Multi-player" is in the categories
    for category in categories:
        if category["description"] == "Multi-player":
            mp_list.append("Multi-player")
        elif category["description"] == "Co-op":
            mp_list.append("Co-op")
    mp_dict[game_id] = mp_list
    return mp_dict


def get_tags(app_id_list, delay=1):
    tag_dict = {}
    
    for appid in app_id_list:
        # Make the API request
        response = requests.get(f"http://store.steampowered.com/api/appdetails?appids={appid}")

        # Check if the request was successful
        if response.status_code == 200:
            game = response.json()
            
            # Check if the app ID is in the response and if it was successful
            if str(appid) in game and game[str(appid)].get("success", False):
                # Check if 'data' and 'genres' exist
                if "data" in game[str(appid)] and "genres" in game[str(appid)]["data"]:
                    tags = [genre["description"] for genre in game[str(appid)]["data"]["genres"]]
                    tag_dict[appid] = tags
                else:
                    tag_dict[appid] = []  # No genres available
            else:
                tag_dict[appid] = []  # Assign empty list if the app ID was not found
        elif response.status_code == 429:
            print(f"Rate limit exceeded for app ID {appid}. Waiting for {delay} seconds.")
            time.sleep(delay)  # Sleep before trying again
            continue  # Retry the same app ID
        else:
            print(f"Error: Received status code {response.status_code} for app ID {appid}.")
            tag_dict[appid] = []  # Handle request failure by assigning an empty list

        time.sleep(delay)  # Optional: sleep after each successful request

    return tag_dict


def add_tags(df, tag_dict):
    df2 = df.copy()
    for index, row in df2.iterrows():
        id = row[1]
        tags = tag_dict.get(id)
        if tags:
            df2.at[index, df2.columns[2]] = ', '.join(tags)
        else:
            df2.at[index, df2.columns[2]] = "Not Found"
    
    return df2


def check_multiplayer(app_id_list, api_key, delay=1):
    mp_dict = {}
    
    for appid in app_id_list:
        mp_list = []
        # Set up the API URL and parameters
        url = "http://store.steampowered.com/api/appdetails"
        params = {
            'appids': appid,
            'key': api_key
        }

        # Make the API request
        response = requests.get(url, params=params)

        
        # Check if the request was successful
        if response.status_code == 200:
            game = response.json()
            
            # Check if the app ID is in the response and if it was successful
            if str(appid) in game and game[str(appid)].get("success", False):
                if "data" in game[str(appid)] and "categories" in game[str(appid)]["data"]:

                    for category in game[str(appid)]["data"]["categories"]:
                        if category["description"] == "Multi-player":
                            mp_list.append("Multi-player")
                        elif category["description"] == "Co-op":
                            mp_list.append("Co-op")

                    mp_dict[appid] = mp_list
                else:
                    mp_dict[appid] = []  # No genres available
            else:
                mp_dict[appid] = []  # Assign empty list if the app ID was not found
        elif response.status_code == 429:
            print(f"Rate limit exceeded for app ID {appid}. Waiting for {delay} seconds.")
            time.sleep(delay)  # Sleep before trying again
            continue  # Retry the same app ID
        else:
            print(f"Error: Received status code {response.status_code} for app ID {appid}.")
            mp_dict[appid] = []  # Handle request failure by assigning an empty list

        time.sleep(delay)  # Optional: sleep after each successful request

    return mp_dict


def add_mp(df, mp_dict):
    df2 = df.copy()
    for index, row in df2.iterrows():
        id = row[1]  
        mp = mp_dict.get(id)  
        
        if mp:  
            current_value = df2.at[index, df2.columns[2]] 
            if current_value:  
                # Append the new multiplayer info to the existing string
                df2.at[index, df2.columns[2]] = f"{current_value}, {', '.join(mp)}"
            else:
                # If column[2] is empty, just set it to the multiplayer info
                df2.at[index, df2.columns[2]] = ', '.join(mp)
        else:
            # If there's no multiplayer info, keep "Not Found"
            df2.at[index, df.columns[2]] = "Not Found"
    
    return df2

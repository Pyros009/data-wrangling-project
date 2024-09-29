import aiohttp, http, asyncio, requests, re, time, os, json, pickle, functools, random
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import steam_tags_f as stf
from dotenv import load_dotenv


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

def add_tags_df (df, dict):
    df2 = df.copy()
    for col in df2.columns:
        if col in dict.keys():
            df2.at[0, col] = dict[col]
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

    return df2

def get_url(url, headers=None, params=None, type="ws"):
    """
    Args:
        url (str): pass on url
        type (str): define "ws" (webscrapping) or "api" (for API/json output), default is ws
        headers (str, optional): Defaults to None.
        params (dict, optional): Defaults to None.

    Returns:
        stat , response: outputs stat code and response content, either soup or json type.
    """
    response = requests.get(url,headers=headers, params=params)
    stat = response.status_code
    if type.lower() == "ws":
        soup = BeautifulSoup(response.content, 'html.parser')
    elif type.lower() == "api":
        soup = response.json()
    time.sleep(1)
    
    return stat, soup

def fetch_dict(soup, gameid):
    k_value = 0
    players = soup.find("tbody")
    play = re.split(r"[\n\t]+",players.get_text().strip())
    player_game = {} 

    for i in range(0, len(play), 5):
        # Date
        date = play[i]
        # Peak players
        average = play[i+1]  
        # Average players
        peak = play[i +4]
        player_game[k_value]={"Date": date,
                            "Avg Players":average,
                            "Peak Players":peak,
        }
        
        k_value += 1
        
    return player_game

def overall_fetch(list_id):
    error_list =[]
    game_id_dict = {}
    for gameid in list_id:
        gameid = str(gameid)
        url = f'https://steamcharts.com/app/{gameid}'
        headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
        try:
            stat, soup = get_url(url, headers=headers, params=gameid)
            if stat == 200:
                print(f"Webcode status is : {stat} for {gameid} id. ")
                player_game = fetch_dict(soup, gameid)
                game_id_dict[gameid] = player_game.copy()
            else:
                error_list.append((gameid, stat))
                print(f"Appid: {gameid} reported an error {stat}, skipping it for now")    
        except Exception as e:  # Catch specific exceptions
            error_list.append((gameid, stat))
            print(f"App ID: {gameid} reported an error: {str(e)}, skipping it for now.")
            
    
    return game_id_dict, error_list



# Graphic Display

def t_plot(df, lines,llegend,yx):
    # Set theme and palette
    sns.set_theme(style="darkgrid")
    sns.set_palette("viridis")

    # plots lines
    plt.figure(figsize=(12, 6))  # Adjust figure size

    for l in lines:
        colors = sns.color_palette("colorblind", 10)
        coloration = random.randint(0,9)
        sns.lineplot(data=df[1:], x=df.index[1:], y=l, marker='o', linestyle='--', linewidth=2, label=l, color=colors[coloration])

    legend = plt.legend(title=llegend, loc='upper left', bbox_to_anchor=(1, 1))
    plt.xlabel('Index')
    plt.ylabel('Values')
    
    # Covid related lines
    plt.axvline(x="November 2019", color='orange', linestyle='--', linewidth=1)
    plt.axvline(x="January 2020", color='red', linestyle='--', linewidth=1)
    plt.axvline(x="June 2020", color='green', linestyle='--', linewidth=1)
    plt.axvline(x="November 2020", color='orange', linestyle='--', linewidth=1)
    plt.axvline(x="November 2021", color='green', linestyle='--', linewidth=1)
    if yx == "y":
        coord = 500000
        plt.text(x="November 2019", y = coord, s='Nov19: China warns about Covid', color='orange', fontsize=10, ha='right', rotation=90)
        plt.text(x="January 2020",  y = coord, s='Jan20: WHO acknoledges Covid', color='red', fontsize=10, ha='right', rotation=90)
        plt.text(x="June 2020",  y = coord, s='Jun20: End of first big lockdown period', color='green', fontsize=10, ha='right', rotation=90)
        plt.text(x="November 2020",  y = coord, s='Nov20: Second Wave', color='orange', fontsize=10, ha='right', rotation=90)
        plt.text(x="November 2021",  y = coord, s='Nov21: Fourth Wave', color='green', fontsize=10, ha='right', rotation=90)
        
    # Game related lines
    #plt.axvline(x="December 2017", color='cyan', linestyle='--', linewidth=1)
    #plt.axvline(x="December 2020", color='cyan', linestyle='--', linewidth=1)
    #plt.axvline(x="September 2021", color='cyan', linestyle='--', linewidth=1)
    #plt.axvline(x="February 2021", color='cyan', linestyle='--', linewidth=1)
    #plt.axvline(x="March 2019", color='cyan', linestyle='--', linewidth=1)


    #plt.text(x="December 2017", y=coord, s="PUBG goes live", color='cyan', fontsize=10, ha='right', rotation=90)
    #plt.text(x="December 2020", y=coord, s="Cyberpunk goes live", color='cyan', fontsize=10, ha='right', rotation=90)
    #plt.text(x="September 2021", y=coord, s="New World goes live", color='cyan', fontsize=10, ha='right', rotation=90)
    #plt.text(x="February 2021", y=coord, s="Valheim goes live", color='cyan', fontsize=10, ha='right', rotation=90)
    #plt.text(x="March 2019", y=coord, s="Sekiro goes live", color='cyan', fontsize=10, ha='right', rotation=90)


    ### Graphic formatting
    dates = df[1:].index
    tick_interval = 3
    tick_indices = range(0, len(dates), tick_interval)

    # Format the date on the x-axis
    plt.xticks(tick_indices, dates[tick_indices], rotation=45, ha="right")

    #Limit x-axis onto a specific interval 
    plt.xlim('August 2022', 'August 2018')  # Specify the limits as strings
    plt.gca().invert_xaxis() # inverts the x-axis (more suited for dates as it grows from left to right)

    # Set titles and labels
    plt.title(llegend)
    plt.xlabel('Date')
    plt.ylabel('Average players per type')

# Z Normalization definition

def z_norm(column):
    mean = column.mean()
    std_dev = column.std()
    return (column - mean) / std_dev

# creates a dataframe of a specific genre with a single column that contains the specified value 
def make_type(df, substring):
    df2 = df.copy()
    columns_to_keep = df2.columns[df2.iloc[0].astype(str).str.strip().str.contains(substring)]
    output = df2[columns_to_keep]
    output[substring]=0
    output.loc[output.index[1:], substring] = output.iloc[1:, :].sum(axis=1)
    output = output.filter(like=substring, axis=1)
       
    return output 
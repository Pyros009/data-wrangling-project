# Project-3
Team Berlin: Henning Claussen & Ricardo Morgado

**"Video Gaming Behavior during COVID"**

## Intro:
During Covid-19 pandemic, restrictions forced people into confinement by either total lockdowns or outdoor activities, decreasing socialization.
Games were then one of the solutions to hang-out with friends. Steam is one of the biggest retailers/distribution gaming platforms, so by using their data
we aim to provide some insights on our ideas.

## Data Sources:
In order to find out if there was a fluctuation on players in games, we focused on Steam data as Steam is one of the biggest distributors/retailers/hub platform for games.

We aimed to try and get data from SteamAPI [http://store.steampowered.com/api/] but unfortunatelly they lacked historical background. They do however contain the required tags we needed to check for the game's genre together with some other informations (appids, etc).

We aimed to use webscrapping on SteamDB's website [https://steamdb.info/] to fetch the historical data, but the website proved uncooperative to webscrapping. It was however, a good source to manually grab the information and storing into a basic dataframe to narrow our field of search, since Steam holds more than 280.000 games/objects. As such, we grabbed the top 1.000 all-time peak activity games using SteamDB's ranking at [https://steamdb.info/charts/].

To grab historical background, we relied on SteamCharts [https://steamcharts.com/] which proven much more webscrapping-friendly.

## Hypothesis and methodology: 

### **1. People were playing more video games during the pandemics.**
We cleaned our assembled dataframe from games that were too recent to be insightful during pandemics. 
To get insights on this hypothesis, we compared Total average players (so the sum of average players on all games) on the COVID's timeframe (August 2018 - August 2022).

**Observing the plot output, it's showing notorious peaks during lockdown/heavy restriction phases indicating there was an increased average player per game.**

### **2. Some game genres had more popularity during the COVID pandemics**
Using the tag row, we grouped games by genre summing the average players, and visualized the information.

**We can observe a notorious peak from multiple genres, but the most pronounced are Action (which is a generic title most games have) together with multi-player and co-op during the lockdown phases and decreasing short after it's lifting. This supports our hypothesis that instead of a generalized rise in average player, people focused on specific genres such as Action, Multiplayer and Co-op games. Also quite curious was the peak post-lockdown on Casual games, which may point either towards some new players remaining gaming but on a much slower and casual pace or the release of a new popular casual game.**

### **3. People turned into Multiplayer and Co-operative (Co-op) games to gap the lack of socialization**
We split the total average players into groups: Multiplayer and non Multiplayer and visualized the information. 

**Again we see the same trend when Multiplayer show's a clear peak during lockdown phases, while non Multi-player games showed no peak at those times. This seems to further reinforce the hypothesis that indeed people were playing multiplayer and Co-op games to socialize virtually.**

## Conclusions & Business case

Analysing the data from prior to the pandemics (August 2018) to after the pandemic period (August 2022), we can conclude that indeed there was a big affluence of players into multiplayer/co-op genres during the pandemic lockdowns without finding any particular reason (such as releases of new games). We can also see some of the genres being prefered over others (so Action as opposite to Simulation), specially if the genre had multiplayer option. Although we can acknoledge that new games may explain some player outbreaks, we found that there was no big title released on the time frame that could explain the data pattern. So it seems there's a direct relation between the lockdown phases during the pandemics and increased average player counts in games, specially those that are multiplayer/cooperative.

## Deliverables
Kanban - **(https://trello.com/b/2n1p42zJ)**
Presentation - **(https://prezi.com/view/8sh0U2AUlRXUeLVF8QTz/)**


###
Modularize Code: Create reusable functions and classes, and place them in separate .py files. Import them into your notebooks or main scripts to maintain a clean and organized codebase.
Use a “main cleaning function” in “cleaning.py” (or similar) that calls all the smaller cleaning functions in a specific order to perform the entire cleaning process at once.
Naming Conventions: Use clear and descriptive names for variables, functions, and classes. Follow language-specific naming conventions to enhance readability.
Remove Unused Code: Eliminate any unused imports, variables, or lines of code. Keep the codebase clean and focused on what is necessary.
Comments and Documentation: Add meaningful comments and documentation to explain complex or crucial parts of the code. It aids understanding and future maintenance.
Logical Organization: Group related functionalities together and maintain a coherent flow within your scripts or notebooks.
Regular Refactoring: Review and refactor the code periodically to remove redundancies, enhance efficiency, and ensure alignment with current best practices and project needs.
Respectful Data Collection: Adhering to the terms of use of APIs and websites.


###
Deliverables
You must submit the following deliverables in order for the project to be deemed complete:

A new repository with the name data-wrangling-project on your GitHub account.
A working code that meets all technical requirements, built by you.
At least 1 Jupyter notebook is required
Include your functions in .py files
Additional needed files for your work


###
Storing an API key directly in your code can expose sensitive information, especially if your code is publicly available (e.g., on a public GitHub repository). The best practice for saving and loading an API key in your code involves the following steps:

1. **Storing the API Key**:
    - **Use Environment Variables**: Store your API key in an environment variable on your system. This keeps the key out of your codebase and allows you to change it without altering your code.


    - **Create a .env File**: If you prefer, you can create a `.env` file (just call it `.env` nothing else before the `.`) in your project directory to store the API key. Inside this file, you would have something like:
   
       ```
       API_KEY=your-api-key-here
       ```

        - **Add .env to .gitignore**: If you're using a version control system like Git, make sure to add the `.env` file to your `.gitignore` file. This prevents the `.env` file (and therefore your API key) from being uploaded to any public repositories. We'll talk about Git and .gitignore in more detail soon.

2. **Load the Key in Your Code**: 

    You can use libraries like `python-dotenv` to load the key into your code. 
    You would need to install `python-dotenv` first.
    ```python 
    !pip install python-dotenv

    from dotenv import load_dotenv
    import os

    load_dotenv()
    api_key = os.getenv("API_KEY")
    ```

       
    Now, `api_key` contains the value of your API key, and you can use it to authenticate your requests to the API.
       

       
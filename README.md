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
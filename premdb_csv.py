import requests
import json
import pandas as pd
import sqlalchemy

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
j = requests.get(url).json()

player_df = pd.DataFrame(j['elements'])
player_df = player_df.set_index('id')
player_df = player_df[['web_name', 'team', 'element_type', 'form', 'points_per_game', 'selected_by_percent',
                       'now_cost', 'minutes', 'transfers_in', 'transfers_out',  'value_season', 'total_points',
                       'goals_scored', 'assists', 'clean_sheets']]

player_df.to_csv('players.csv')
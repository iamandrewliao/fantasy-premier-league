import requests
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy
import os

os.environ['premdb'] = 'postgresql://postgres:postgres@fpl.c5aqdxmdgobi.us-east-1.rds.amazonaws.com:5432/postgres'
endpoint = os.environ.get('premdb')
#initialize a sqlalchemy.engine object
engine = create_engine(endpoint)

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r_json = requests.get(url).json()

# load up elements key into player df
player_df = pd.DataFrame(r_json['elements'])
# set id as the index

player_df = player_df.set_index('id')
# take only useful columns and filter rest out

player_df = player_df[['web_name', 'team', 'element_type', 'form', 'points_per_game', 'selected_by_percent',
                       'now_cost', 'minutes', 'transfers_in', 'transfers_out',  'value_season', 'total_points',
                       'goals_scored', 'assists', 'clean_sheets']]

# first drop the players table if it exists
sql = "DROP TABLE IF EXISTS players;"

print(engine.execute(sql))
# cast certain columns to decimal rather than text
sql_type = {'web_name': sqlalchemy.types.Text(), 'team': sqlalchemy.Integer, 'element_type': sqlalchemy.Integer,
            'form': sqlalchemy.DECIMAL, 'points_per_game': sqlalchemy.DECIMAL, 'selected_by_percent': sqlalchemy.DECIMAL,
            'now_cost': sqlalchemy.Integer, 'minutes': sqlalchemy.Integer, 'transfers_in': sqlalchemy.Integer,
            'transfers_out': sqlalchemy.Integer, 'value_season': sqlalchemy.DECIMAL, 'total_points': sqlalchemy.Integer,
            'goals_scored': sqlalchemy.Integer, 'assists': sqlalchemy.Integer, 'clean_sheets': sqlalchemy.Integer
            }

player_df.to_sql('players', con=engine, dtype=sql_type)

# selected by % should be float
# print(player_df.head())
sql = "SELECT * FROM players limit 50;"
print(engine.execute(sqlalchemy.text(sql)).fetchall())
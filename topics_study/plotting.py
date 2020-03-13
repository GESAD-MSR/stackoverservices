import plotly.offline as py
import plotly.graph_objs as go
import os
import pandas as pd

DATA_FOLDER = os.path.join(
    os.path.dirname(__file__), 'data/microservices/')

QUESTIONS_FILE = DATA_FOLDER + 'raw/questions.csv'

questions = pd.read_csv(QUESTIONS_FILE, parse_dates=['CreationDate'])

first_year = questions['CreationDate'].min().year
last_year = questions['CreationDate'].max().year

years = list(range(first_year, last_year+1))

labels = list(map(str, years))

data = [
    go.Bar(
        x=labels,
        y=[
            len(
                [row['Id'] for idx, row in questions.iterrows() 
                    if row['CreationDate'].year == year]
            )
            for year in years
        ],
    )
]

fig = go.Figure(
    data=data, layout={"title": "Microsservices Questions over Years"})
py.plot(fig, filename='post_by_year')

import pandas as pd
import numpy as np
import altair as alt


set_width = 1500
set_height = 350


data = pd.read_csv('minard-data.csv')
cities = data[["LONC", "LATC", "CITY"]].copy()
cities = cities.dropna()


temperatures = data[["LONT", "TEMP", "DAYS", "MON", "DAY"]].copy()
temperatures = temperatures.dropna()


troops = data[["LONP", "LATP", "SURV" , "DIR", "DIV"]].copy()
troops = troops.dropna()
troops = troops.sort_values(by=["DIV", "SURV"], ascending=False)


troop_graph = alt.Chart(troops, title='Napoleon\'s March on Russia (A Minard Recreation)').mark_trail().encode(
    longitude='LONP',
    latitude='LATP',
    size=alt.Size('SURV', scale=alt.Scale(range=[1, 100]), legend=None),
    detail='DIV',
    color=alt.Color('DIR', scale=alt.Scale(domain=['A', 'R'],range=['#A2DB34', '#FF0000'])),
).properties(width=set_width,height=set_height)


city_graph = alt.Chart(cities).mark_text().encode(
    longitude='LONC',
    latitude='LATC',
    text='CITY',
)


every_second_troop_num = troops.iloc[::2, :].copy()
every_second_troop_num["LONP"] += 0.05
every_second_troop_num["LATP"] += every_second_troop_num["DIR"].replace({"A": 0.05, "R": -0.05})


troop_numbers_graph = alt.Chart(every_second_troop_num).mark_text().encode(
    longitude='LONP',
    latitude='LATP',
    text='SURV'
)


temperatures['LATT']=40


temp_graph = alt.Chart(temperatures, title='Temperature During Retreat').mark_line().encode(
    x=alt.X('LONT', title='', axis=alt.Axis(labels=False)),
    y=alt.Y('TEMP', title='Temp')
).properties(
    height=100
)


combo_graph = troop_graph+city_graph+troop_numbers_graph


minard_graph = alt.vconcat(combo_graph, temp_graph).configure_view(
    width=set_width,
    height=set_height,
).configure_axis(
    grid=True,
)


minard_graph.show()

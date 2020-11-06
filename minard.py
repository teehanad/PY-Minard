import pandas as pd
import numpy as np
import altair as alt

#Setting witdh info for chart
set_width = 1500
set_height = 350

#Reading in the data and breaking it into 3 categories for Troops, Cities and Temps
data = pd.read_csv('minard-data.csv')
cities = data[["LONC", "LATC", "CITY"]].copy()
cities = cities.dropna()
temperatures = data[["LONT", "TEMP", "DAYS", "MON", "DAY"]].copy()
temperatures = temperatures.dropna()
troops = data[["LONP", "LATP", "SURV" , "DIR", "DIV"]].copy()
troops = troops.dropna()
troops = troops.sort_values(by=["DIV", "SURV"], ascending=False)


#Initial graph drawing troop lines
troop_graph = alt.Chart(troops, title='Napoleon\'s March on Russia (A Minard Recreation)').mark_trail().encode(
    longitude='LONP',
    latitude='LATP',
    size=alt.Size('SURV', scale=alt.Scale(range=[1, 100]), legend=None),
    detail='DIV',
    color=alt.Color('DIR', scale=alt.Scale(domain=['A', 'R'],range=['#F0C575', '#000000'])),
).properties(width=set_width,height=set_height)


#Graph plotting city names to be overlayed on troop graph
city_graph = alt.Chart(cities).mark_text(angle=360, size = 15,color ='#F8F8FF').encode(
    longitude='LONC',
    latitude='LATC',
    text='CITY',
)


#Simple selection of every second troop survivor number as using all of them over crowds the graph
every_second_troop_num = troops.iloc[::2, :].copy()
every_second_troop_num["LONP"] += 0.05
every_second_troop_num["LATP"] += every_second_troop_num["DIR"].replace({"A": 0.08, "R": -0.2})


#Graph plotting troop survivor numbers to be overlayed on first graph
troop_numbers_graph = alt.Chart(every_second_troop_num).mark_text(angle=360, align='center', size = 13,color ='#F8F8FF').encode(
    longitude='LONP',
    latitude='LATP',
    text='SURV',
    detail='DIV',
    color=alt.Color('DIV', type='ordinal',scale=alt.Scale(domain=[1, 2, 3],range=['#05E9FF', '#0EBFE9', '#009ACD']))
)


#Adding a latitude to temp data so that it is plotted in line with the above graph of retreat but just below it
temperatures['LATT']=40

#Graph of temperature during retreat
temp_graph = alt.Chart(temperatures, title='Temperature During Retreat').mark_line().encode(
    x=alt.X('LONT', title='', axis=alt.Axis(labels=False)),
    y=alt.Y('TEMP', title='Temp'),
    color=alt.ColorValue('red')
).properties(
    height=100
)

combo_graph = alt.layer(
    troop_graph, city_graph, troop_numbers_graph
).resolve_scale(
    color='independent'
)

#combinng all layers of the Troop/Cities graph



#Vertical concatination of the Troop/City graph and the Temp graph
minard_graph = alt.vconcat(combo_graph, temp_graph, background='grey').configure_view(
    width=set_width,
    height=set_height
).configure_axis(
    grid=True,
).configure_legend(
    titleColor='black', 
    titleFontSize=14, 
    columnPadding=10,
    symbolSize = 800,
    symbolStrokeWidth=20
) 


minard_graph.show()

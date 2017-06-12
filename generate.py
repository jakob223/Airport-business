import plotly

import csv
import sys
import plotly.plotly as py
import plotly.graph_objs as go


def to_four(str):
    return '0' * (4 - len(str)) + str

def rotate(l, n):
    return l[-n:] + l[:-n]

airports = ['PHX', 'LAS', 'CLT', 'SFO', 'DEN', 'JFK', 'DFW', 'ORD', 'LAX', 'ATL']

hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09'] + [str(x) for x in range(10, 24)]
minutes = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09'] + [str(x) for x in range(10, 60)]
time_list = []
for h in hours:
    for m in minutes:
        time_list.append(h + m)
time_list = time_list[1:] + ['2400']

z = []

for airport in airports:
    data = open('data.csv')
    print(airport, end=": ")
    heat = {k: 0 for k in time_list}
    reader = csv.reader(data)
    for row in reader:
        if row[16] == airport and row[4] != 'NA':
            heat[to_four(row[4])] += 1
    z.append(rotate(list(heat.values()), 1))
    print(sum(list(heat.values())))
    data.close()


for i in range(0, len(time_list)):
    time_list[i] = time_list[i][:2] + ':' + time_list[i][2:]

del(time_list[-1])
time_list = ['00:00'] + time_list

data = [
    go.Heatmap(
        z=z,
        x=time_list,
        y=airports,
        colorscale='Viridis',
    )
]

layout = go.Layout(
    title='Takeoffs per minute',
    xaxis = dict(ticks='', nticks=24, type='category'),
    yaxis = dict(ticks='' )
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='takeoffs')

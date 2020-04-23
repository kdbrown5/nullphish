import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pysqlcipher3 import dbapi2 as sqlite
from collections import OrderedDict 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



app = dash.Dash()

def templatestats():
    business = 'nullphish'
    template = 'Lyft'
    con = sqlite.connect('db/db1.db')
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('PRAGMA key = '+dbkey+';')
    cur.execute('select * from phishsched where business = (?);', (business,))
    tempstats = cur.fetchall()
    con.close()
    return tempstats

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d    

tempstats = templatestats()
tempx = []
tempy = []
for i in tempstats:
    for k, v in i.items():
        if k == 'template':
            tempy.append(1)
            tempx.append(v)

print('tempx',tempx)
print('tempy',tempy)


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Graph(
        id='Graph1',
        figure={
            'data': [
                {'x': tempx, 'y': tempy, 'type': 'bar', 'name': 'Templates sent'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
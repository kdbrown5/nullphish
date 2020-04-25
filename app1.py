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

app = dash.Dash(
        __name__,
        external_stylesheets=external_stylesheets,
        requests_pathname_prefix='/app1/'
        )

def templatestats():
    business = 'nullphish'
    con = sqlite.connect('db/db1.db')
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('PRAGMA key = '+dbkey+';')
    cur.execute('select * from phishsched where business = (?) and activetime != "none";', (business,))
    tempstats = cur.fetchall()
    cur.execute('select * from phishsched where business = (?) and activetime = "none";', (business,))
    notphished = cur.fetchall()
    cur.execute('select * from phishsched where business = (?) and sentdate != "none";', (business,))
    sentline = cur.fetchall()
    con.close()
    return tempstats, notphished, sentline

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d    

tempstats, notphished, sentline = templatestats()
tempx = []
tempy = []
notphishedx = []
notphishedy = []
totalopened = 0
totalunopened = 0

linephish = tempstats
linenophish = notphished

xa = []
xb = []
xc = 0
xd = []
#for i in sentline:
#    for k, v in i.items():
#        if k == 'date'
#    print(i)


for i in sentline:
    for k, v in i.items():
        if k == 'sentdate':
            xa.append(v)
        if k == 'activetime':
            if v == "none":
                print('activetime-v', v)
                xb.append(-1)
                xc = xc-1
                xd.append(xc)
            if v != "none":
                xb.append(1)
                xc = xc+1
                xd.append(xc)

print('xa', xa)
print('xb', xb)

for i in tempstats:
    totalopened = totalopened+1
    for k, v in i.items():
        if k == 'template':
            tempy.append(1)
            tempx.append(v)
            
for i in notphished:
    totalunopened = totalunopened+1
    for k, v in i.items():
        if k == 'template':
            notphishedy.append(1)
            notphishedx.append(v)

totalsent = totalopened+totalunopened
#print('tempx',tempx)
#print('tempy',tempy)
#print('totalsent', totalsent)
#print('totalopened', totalopened)
#print('totalunopened', totalunopened)




colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Templates sent',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='---', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Graph(
        id='Graph1',
        figure={
            'data': [
                {'x': 'Total Sent', 'y': [totalsent], 'type': 'bar', 'name': 'Total Sent'},
                {'x': 'Total Opened', 'y': [totalopened], 'type': 'bar', 'name': 'Total Opened'},
                {'x': 'Total Unopened', 'y': [totalunopened], 'type': 'bar', 'name': 'Total Unopened'},
                {'x': tempx, 'y': tempy, 'type': 'bar', 'name': 'Opened'},
                {'x': notphishedx, 'y': notphishedy, 'type': 'bar', 'name': u'Not opened'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),
    dcc.Graph(
        id='Graph2',
        figure={
            'data': [
                {'x': xa, 'y': xb, 'type': 'bar', 'name': 'Opened'},
                {'x': xa, 'y': xd, 'type': 'line', 'name': 'Opened'},
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
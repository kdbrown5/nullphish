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

def userstats():
    business = 'nullphish'
    con = sqlite.connect('db/db1.db')
    con.row_factory = sqlite.Row
    cur = con.cursor()
    cur.execute('PRAGMA key = '+dbkey+';')
    cur.execute('select * from phishsched where business = (?) and type = "email" and sentdate != "none";', (business,))
    userstat = cur.fetchall()
    return userstat


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def mutatetempstats(tempstats):
    tempx = []
    tempy = []
    for i in tempstats:
        #totalopened = totalopened+1
        for k, v in i.items():
            if k == 'template':
                tempy.append(1)
                tempx.append(v)
    return tempx, tempy

def mutateuserstat():
    business = 'nullphish'
    con = sqlite.connect('db/db1.db')
    con.row_factory = sqlite.Row
    cur = con.cursor()
    cur.execute('PRAGMA key = '+dbkey+';')
    cur.execute('select * from phishsched where business = (?) and type = "email" and sentdate != "none";', (business,))
    userstat = cur.fetchall()
    con.close()
    xid = []
    xtemplate = []
    xmailname = []
    xbitly = []
    xsentdate = []
    xdepartment = []
    xactivetime = []
    for i in userstat:
        xid.append(i['id'])
        xtemplate.append(i['template'])
        xmailname.append(i['mailname'])
        xbitly.append(i['bitly'])
        xsentdate.append(i['sentdate'])
        xdepartment.append(i['department'])
        xactivetime.append(i['activetime'])
    return xid, xtemplate, xmailname, xbitly, xsentdate, xdepartment, xactivetime

def unique(inputlist):
    unique_list = []
    #newdatesent = []
    for x in inputlist:
        if x not in unique_list:
            unique_list.append(x)
    for x in unique_list:
        x = x.replace(' ','_')
        print(x)

def makecounters(sentline, notphished):
    xa = []
    xb = []
    xc = 0
    xd = []
    xe = 0
    notphishedx = []
    notphishedy = []
    for i in sentline:
        for k, v in i.items():
            if k == 'sentdate':
                xa.append(v)
            if k == 'activetime':
                if v == "none":
                    xe = xe+1
                    xb.append(-1)
                    xc = xc-1
                    xd.append(xc)
                if v != "none":
                    xe = xe+1
                    xb.append(1)
                    xc = xc+1
                    xd.append(xc)
    for i in notphished:
        #totalunopened = totalunopened+1
        for k, v in i.items():
            if k == 'template':
                notphishedy.append(1)
                notphishedx.append(v)
    return xa, xb, xc, xd, xe, notphishedx, notphishedy

def make_layout():
    userstat = userstats()
    xid, xtemplate, xmailname, xbitly, xsentdate, xdepartment, xactivetime = mutateuserstat()
    tempstats, notphished, sentline = templatestats()
    xa, xb, xc, xd, xe, notphishedx, notphishedy = makecounters(sentline, notphished)
    tempx, tempy = mutatetempstats(tempstats)
    none = None
    colors = {
        'background': '#111111',
        'text': '#7FDBFF'
    }
    return html.Div(style={'backgroundColor': colors['background']}, children=[
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
                    {'x': xsentdate, 'y': xd, 'type': 'line', 'name': 'Sent'},
                    {'x': xsentdate, 'y': xtemplate, 'type': 'line', 'name': 'Opened'},
                    #{'x': xactivetime, 'y': [xtemplate], 'type': 'line', 'name': 'Opened'},
                ],
                'layout': {
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    }
                }
            }
        )]
    )
    
app.layout = make_layout
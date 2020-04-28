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
    return unique_list

def makecounters(sentline, notphished):
    xa = []
    xb = []
    xc = 0
    xd = []
    xe = 0
    xavg = 0
    xavglist = []
    notphishedx = []
    notphishedy = []
    xsum = 0
    for i in sentline:
        for k, v in i.items():
            if k == 'sentdate':
                xa.append(v)
            if k == 'activetime':
                if v == "none":
                    xe = xe+1
                    xb.append(0)
                    xc = xc-1
                    xd.append(xc)
                    xsum = xsum+0
                if v != "none":
                    xe = xe+1
                    xb.append(1)
                    xc = xc+1
                    xd.append(xc)
                    xsum = xsum+1
                xavgprelist = xsum/len(xb)
                xavglist.append(xavgprelist)
    for i in notphished:
        #totalunopened = totalunopened+1
        for k, v in i.items():
            if k == 'template':
                notphishedy.append(1)
                notphishedx.append(v)
    return xa, xb, xc, xd, xe, notphishedx, notphishedy, xavglist

def listtemplate():
    templatelist = []
    business = 'nullphish'
    con = sqlite.connect('db/db1.db')
    cur = con.cursor()
    cur.execute('PRAGMA key = '+dbkey+';')
    cur.execute('select distinct template from phishsched where template != "" and business = (?);', (business,))
    for i in cur.fetchall():
        templatelist.append(i[0])
    a0 = []
    a0f = []
    a0g = []
    a1 = []
    a1f = []
    a1g = []
    a2f = []
    a2g = []
    a3f = []
    a3g = []
    a4f = []
    a4g = []
    a5f = []
    a5g = []
    a6f = []
    a6g = []
    a7f = []
    a7g = []
    a8f = []
    a8g = []
    a9f = []
    a9g = []
    a10f = []
    a10g = []
    a2 = []
    a3 = []
    a4 = []
    a5 = []
    a6 = []
    a7 = []
    a8 = []
    a9 = []
    a10 = []
    try:
        for row in cur.execute('select sentdate from phishsched where template = (?) and business = (?);', (templatelist[0], business,)):
            a0.append(row[0])
        for row in cur.execute('select activetime from phishsched where template = (?) and business = (?);', (templatelist[0], business,)):
            if 'none' in row:
                a0f.append(0)
            else:
                a0f.append(1)
        a0g = converttoavg(a0g, a0f)
        for row in cur.execute('select sentdate from phishsched where template = (?) and business = (?);', (templatelist[1], business,)):
            a1.append(row[0])
        for row in cur.execute('select activetime from phishsched where template = (?) and business = (?);', (templatelist[1], business,)):
            if 'none' in row:
                a1f.append(0)
            else:
                a1f.append(1)
        a1g = converttoavg(a1g, a1f)
        for row in cur.execute('select sentdate from phishsched where template = (?) and business = (?);', (templatelist[2], business,)):
            a2.append(row[0])
        for row in cur.execute('select activetime from phishsched where template = (?) and business = (?);', (templatelist[2], business,)):
            if 'none' in row:
                a2f.append(0)
            else:
                a2f.append(1)
        a2g = converttoavg(a2g, a2f)
        for row in cur.execute('select sentdate from phishsched where template = (?) and business = (?);', (templatelist[3], business,)):
            a3.append(row[0])
        for row in cur.execute('select activetime from phishsched where template = (?) and business = (?);', (templatelist[3], business,)):
            if 'none' in row:
                a3f.append(0)
            else:
                a3f.append(1)
        a3g = converttoavg(a3g, a3f)
        for row in cur.execute('select sentdate from phishsched where template = (?) and business = (?);', (templatelist[4], business,)):
            a4.append(row[0])
        for row in cur.execute('select activetime from phishsched where template = (?) and business = (?);', (templatelist[4], business,)):
            if 'none' in row:
                a4f.append(0)
            else:
                a4f.append(1)
        a4g = converttoavg(a4g, a4f)
        for row in cur.execute('select sentdate from phishsched where template = (?) and business = (?);', (templatelist[5], business,)):
            a5.append(row[0])
        for row in cur.execute('select activetime from phishsched where template = (?) and business = (?);', (templatelist[5], business,)):
            if 'none' in row:
                a5f.append(0)
            else:
                a5f.append(1)
        a5g = converttoavg(a5g, a5f)
        for row in cur.execute('select sentdate from phishsched where template = (?) and business = (?);', (templatelist[6], business,)):
            a6.append(row[0])
        for row in cur.execute('select activetime from phishsched where template = (?) and business = (?);', (templatelist[6], business,)):
            if 'none' in row:
                a6f.append(0)
            else:
                a6f.append(1)
        a6g = converttoavg(a6g, a6f)
        for row in cur.execute('select sentdate from phishsched where template = (?) and business = (?);', (templatelist[7], business,)):
            a7.append(row[0])
        for row in cur.execute('select activetime from phishsched where template = (?) and business = (?);', (templatelist[7], business,)):
            if 'none' in row:
                a7f.append(0)
            else:
                a7f.append(1)
        a7g = converttoavg(a7g, a7f)
        for row in cur.execute('select sentdate from phishsched where template = (?) and business = (?);', (templatelist[8], business,)):
            a8.append(row[0])
        for row in cur.execute('select activetime from phishsched where template = (?) and business = (?);', (templatelist[8], business,)):
            if 'none' in row:
                a8f.append(0)
            else:
                a8f.append(1)
        a8g = converttoavg(a8g, a8f)
        for row in cur.execute('select sentdate from phishsched where template = (?) and business = (?);', (templatelist[9], business,)):
            a9.append(row[0])
        for row in cur.execute('select activetime from phishsched where template = (?) and business = (?);', (templatelist[9], business,)):
            if 'none' in row:
                a9f.append(0)
            else:
                a9f.append(1)
        a9g = converttoavg(a9g, a9f)
        for row in cur.execute('select sentdate from phishsched where template = (?) and business = (?);', (templatelist[10], business,)):
            a10.append(row[0])
        for row in cur.execute('select activetime from phishsched where template = (?) and business = (?);', (templatelist[10], business,)):
            if 'none' in row:
                a10f.append(0)
            else:
                a10f.append(1)
        a10g = converttoavg(a10g, a10f)
    except:
        pass
    con.close()
    return templatelist, a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a0g, a1g, a2g, a3g, a4g, a5g, a6g, a7g, a8g, a9g, a10g

def converttoavg(newlist, oldlist):
    stepping = 0
    tempsum = 0
    for i in oldlist:
        stepping = stepping+1
        tempsum = tempsum+i
        domath = tempsum/stepping
        newlist.append(domath)
    return newlist


def make_layout():
    userstat = userstats()
    xid, xtemplate, xmailname, xbitly, xsentdate, xdepartment, xactivetime = mutateuserstat()
    tempstats, notphished, sentline = templatestats()
    xa, xb, xc, xd, xe, notphishedx, notphishedy, xavglist = makecounters(sentline, notphished)
    tempx, tempy = mutatetempstats(tempstats)
    templatelist, a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a0g, a1g, a2g, a3g, a4g, a5g, a6g, a7g, a8g, a9g, a10g = listtemplate()
    print(templatelist[0], 'a0 -', a0, a0g)
    print(templatelist[1], 'a1 -', a1, a1g)
    print(templatelist[2], 'a2 -', a2, a3g)
    print(templatelist[3], 'a3 -', a3, a3g)
    print(templatelist[4], 'a4 -', a4, a4g)
    print(templatelist[5], 'a5 -', a5, a5g)
    print(templatelist[6], 'a6 -', a6, a6g)
    print(templatelist[7], 'a7 -', a7, a7g)
    print(templatelist[8], 'a8 -', a8, a8g)
    colors = {
        'background': '#111111',
        'text': '#7FDBFF'
    }
    return html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        #children='Templates sent',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='Opened / Not Opened by Template', style={
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
                    },
                    'height':300,
                }
            }
        ),
    html.Div(children='(Avg) Click Rate (%) over time (all sent items)', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
        dcc.Graph(
            id='Graph2',
            figure={
                'data': 
                [
                    {'x': xsentdate, 'y': xavglist, 'type': 'line', 'name': u'Combined (All)', 'line': {'width':4},},
                    {'x': a0, 'y': a0g, 'type': 'line', 'name': templatelist[0], 'line': {'width':1},},
                    {'x': a1, 'y': a1g, 'type': 'line', 'name': templatelist[1], 'line': {'width':1},},
                    {'x': a2, 'y': a2g, 'type': 'line', 'name': templatelist[2], 'line': {'width':1},},
                    {'x': a3, 'y': a3g, 'type': 'line', 'name': templatelist[3], 'line': {'width':1},},
                    {'x': a4, 'y': a4g, 'type': 'line', 'name': templatelist[4], 'line': {'width':1},},
                    {'x': a5, 'y': a5g, 'type': 'line', 'name': templatelist[5], 'line': {'width':1},},
                    {'x': a6, 'y': a6g, 'type': 'line', 'name': templatelist[6], 'line': {'width':1},},
                    {'x': a7, 'y': a7g, 'type': 'line', 'name': templatelist[7], 'line': {'width':1},},
                    {'x': a8, 'y': a8g, 'type': 'line', 'name': templatelist[8], 'line': {'width':1},},
                    #{'x': a9, 'y': a9g, 'type': 'line', 'name': templatelist[9], 'line': {'width':1},},
                    #{'x': a10, 'y': a10g, 'type': 'line', 'name': templatelist[10], 'line': {'width':1},},
                ],
                'layout': {
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    },
                }
            }
        )]
    )

    
app.layout = make_layout
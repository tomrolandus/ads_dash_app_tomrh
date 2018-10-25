import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

#READ THE DATA USING REGEX TO HANDLE TABS AND COMMMAS
data = pd.read_csv('nama_10_gdp.tsv',sep=r'\,|\t', engine='python')


#MELT TO TURN THE YEAR COLS INTO ROWS
df = pd.melt(data, id_vars=["unit", "na_item","geo\\time"], var_name="Year", value_name="Value")

#SOME RENAMING REARANGING
df = df[['na_item','geo\\time','Value','Year','unit']]
df.rename(columns={'na_item':'Indicator Name','geo\\time':'Country Name'}, inplace=True)
df['Year'] = df['Year'].astype('int')

app = dash.Dash()

#POSSIBLE VALUES FOR THE INDICATORS AND COUNTRIES
available_indicators = df['Indicator Name'].unique()
available_countries = df['Country Name'].unique()

app.layout = html.Div([
    
    #top part of the page -> taken from previous ex
    html.Div([
        html.Div([

            html.Div([
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='B1G'
                )
            ],
            style={'width': '50%', 'display': 'inline-block','float' : 'middle'}),

            html.Div([
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='P3'
                )
            ],style={'width': '50%', 'display': 'inline-block','float' : 'middle'})
        ]),


        dcc.Graph(id='indicator-graphic'),
        
        dcc.Slider(
            id='year--slider',
            min=df['Year'].min(),
            max=df['Year'].max(),
            value=df['Year'].max(),
            step=None,
            marks={str(year): str(year) for year in df['Year'].unique()}
        )
    ],style={'width': '100%', 'display': 'inline-block', 'margin':'auto', 'padding' :20}),
    
    
    #bottom half of the page
    html.Div([
        html.Div([

            html.Div([
                dcc.Dropdown(
                    id='country',
                    options=[{'label': i, 'value': i} for i in available_countries],
                    value='UK'
                )
            ],
            style={'width': '50%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='yaxis-column2',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='B1G'
                )
            ],style={'width': '50%', 'display': 'inline-block'})
        ]),


        dcc.Graph(id='indicator-graphic2'),
        
       
    ],style={'width': '100%', 'display': 'inline-block','padding':20}) #end of bottom side of page
])


#FIRST GRAPH, MAINLY TAKEN FROM PREVIOUS EX
@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    dff = df[df['Year'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' 
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' 
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
            
        )
    }

#SECOND GRAPH
@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('country', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value')])
def update_graph2(country, yaxis_column_name):
    dfg = df[df['Country Name'] == country]
    
    return {
        'data': [go.Scatter(
            #HERE I HARD CODE TO SELECT A CERTAIN UNIT, WOULD BE BETTER TO ADD A DROPDOWN FOR THAT
            x=dfg[(dfg['Indicator Name'] == yaxis_column_name) & (dfg['unit'] == dfg[dfg['Indicator Name'] == yaxis_column_name]['unit'].unique()[0])]['Year'],
            y=dfg[(dfg['Indicator Name'] == yaxis_column_name) & (dfg['unit'] == dfg[dfg['Indicator Name'] == yaxis_column_name]['unit'].unique()[0])]['Value'],
            text=dfg[dfg['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': country,
                'type': 'linear' 
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' 
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
            
        )
    }



if __name__ == '__main__':
    app.run_server()

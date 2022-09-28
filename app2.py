from datetime import date
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_table import DataTable


today = datetime.today().strftime('%Y-%m-%d')

## layout
ts_layout = go.Layout(
    xaxis={
        "rangeslider": {"visible": True}, 
        "rangeselector": {  
            "buttons": [
                {"label": "15j", "step": "day", "count": 15},  
                {"label": "30j", "step": "day", "count": 30},
                {"step": "all"},  
            ]
        },
    }
)

## READ THE DATA
code_by_day = pd.read_excel('code_by_day.xlsx')
produit_by_day = pd.read_excel('produit_by_day.xlsx')

#=========================================START APP===============================================
# stylesheet with the .dbc class
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])
server = app.server

app.layout = html.Div([
    html.H1("Rapport de NAMIA", style={"textAlign":"center", 'backgroundColor': '#45E3E9'}),
    html.H5('Choisi la date:'),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        display_format='DD/MM/YYYY',
        min_date_allowed=date(2022, 7, 2),
        max_date_allowed=today,
        initial_visible_month= today ,
        start_date = date(2022, 7, 2),
        end_date=today,
        start_date_placeholder_text='du',
        day_size=30,
        first_day_of_week=1,
        
    ),
    html.Br(),
    html.Br(),

    # Flex container
#     html.Div([
    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', 
             children=[
    dcc.Tab(label='Produit', value='tab-1-example-graph',
           children=[
               html.Div([ 
               html.Div([
        dcc.Graph(id='barh_produit', style={'width': '120vh', 'height': '90vh',
                                       'display': 'inline-block'
                                       }),

        ], style={'width': '60%', 'display': 'inline-block'
               }),

        # Table container
        html.Div([
        html.Div(id='data-table1', style={'display': 'inline-block', 'width': '80vh', 'height': '110vh',
                                          'margin-left': '25px', 'margin-top': 100})
                                ], style={'width': '20%'}),
           ],  style={'display': 'flex'} ),
               
        dcc.Graph(id='produit_graph', style={'height': '100vh'}),
       ]) ,
    
    ## -------------------------------------------------------------------------------------   
    ## TAB 'CODE'
    dcc.Tab(label='Code', value='tab-2-example-graph',
           children=[
               html.Div([ 
               html.Div([
        dcc.Graph(id='barh_code', style={'width': '120vh', 'height': '80vh',
                                       'display': 'inline-block',
                                        "maxHeight": "600px", "overflowY": "scroll"} ),

        ], style={'width': '60%', 'display': 'inline-block'} ),

        # Table container
        html.Div([
        html.Div(id='data-table2', style={'display': 'inline-block', 'width': '80vh', 'height': '110vh',
                                           'margin-left': '75px', 'margin-top': 100})
                                ], style={'width': '20%'} ),
        ], style={'display': 'flex' } ),
        
        dcc.Graph(id='code_graph'),
       ])
    ])
], style={'maxWidth': '100%',  'overflowX': 'hidden'})

## ===========================================Produit Callback============================================
@app.callback(
    Output('barh_produit', 'figure'),
    Output('data-table1', 'children'),
    Output('produit_graph', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('tabs-example-graph', 'value'),
)
def update_produit(start, end, tab):
    
    if tab == 'tab-1-example-graph':
        
        ## FILTER THE DATE
        produit_date = produit_by_day[produit_by_day['DATE'].between(start, end)]

        ## products sorted by quantity
        pro_quantity = produit_date.groupby('PRODUIT')[['QUANTITE']].sum().sort_values('QUANTITE', ascending=False).reset_index()
        pro_quantity['PERCENTAGE'] = pro_quantity['QUANTITE'].map(lambda x: round(x*100/pro_quantity['QUANTITE'].sum(),2))
        ## STANDART SORT (PRODUIT)
        custom_dict = {'T03':0, 'T04':1, 'T05':2, "T06":3, "T07":4, "T08":5, "PR1":6, "PR2":7, "PR3":8, "PR":9}
        pro_quantity = pro_quantity.sort_values(by=['PRODUIT'], key=lambda x: x.map(custom_dict))

        # --------------------------------TABLE------------------------------------------------------------
        table_produit = DataTable(columns = [{'name': col, 'id': col} 
                                     for col in pro_quantity.columns],
                          data = pro_quantity.to_dict('records'),
                          page_size = 10,
                          style_header={'whiteSpace': 'normal'},
                          fixed_rows={'headers': True},
                          virtualization=True,
                          style_table={'height': 500, 'width': 440},

                          sort_action='native',
                          filter_action='native',
                          column_selectable="single",
                          export_format='xlsx',
                          ),

        # ------------------------------------------------barh--------------------------------------------------
        ## barh 'PRODUIT'
        barh_produit = go.Figure()
        barh_produit.add_trace(go.Bar(x = pro_quantity['QUANTITE'], y = pro_quantity['PRODUIT'],
                           orientation='h',
                           name='',                   
                           hovertemplate='<br>'.join([
                            'Q: %{x}'])
                       )),

        barh_produit.update_layout(title= {'text': '<b>Produit par Quantite <b>', 'y':0.95, 'x':0.5},
                               xaxis_title="Quantite",
                               yaxis_title="Produit", font=dict(
                                    family="Ubuntu",
                                    size=18,
                                    color="RebeccaPurple"),
            yaxis= {'categoryarray':['T03', 'T04', 'T05', 'T06', 'T07', 'T08', 'PR1', 'PR2', 'PR3', 'PR']})

        # ------------------------------------------------BAR-----------------------------------------------
        ## BAR 'PRODUIT'
        fig_produit = px.bar(produit_date, x='DATE', y="QUANTITE", color='PRODUIT', height=700,
                        color_discrete_sequence=px.colors.qualitative.Light24)
        fig_produit = fig_produit.update_xaxes(tickangle=50, nticks=40)
        fig_produit = fig_produit.update_layout(ts_layout)
        fig_produit = fig_produit.update_layout(title={'text': '<b>Produit par Jour<b>', 'y':0.95, 'x':0.5 })

    
        return  barh_produit , table_produit, fig_produit
    
    else:
        return dash.no_update, dash.no_update, dash.no_update
    

    
    
## ====================================Code Callback==================================================
@app.callback(
    Output('barh_code', 'figure'),
    Output('data-table2', 'children'),
    Output('code_graph', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('tabs-example-graph', 'value'),
)

def update_code(start, end, tab):     
    if tab == 'tab-2-example-graph':
        
        ## FILTER THE DATE
        code_date = code_by_day[code_by_day['DATE'].between(start, end)]

        ## Percentage for Code
        code_perct = code_date.groupby('CODE')[['QUANTITE']].sum().sort_values('QUANTITE', ascending=False).reset_index()
        code_perct['PERCENTAGE'] = code_perct['QUANTITE'].map(lambda x: round(x*100/code_perct['QUANTITE'].sum(),2))


        ## ============================= code =================================================================
        ## TABLE 2
        table_code = DataTable(columns = [{'name': col, 'id': col} 
                                     for col in code_perct.columns],
                          data = code_perct.to_dict('records'),

                          style_header={'whiteSpace': 'normal'},
                          fixed_rows={'headers': True},
                          virtualization=True,
                          style_table={'height': 400, 'width': 430},

                          sort_action='native',
                          filter_action='native',
                          column_selectable="single",
                          export_format='xlsx',
                          ),

        ## barh 'CODE'
        barh_code = go.Figure()
        barh_code.add_trace(go.Bar(x = code_perct['QUANTITE'], y = code_perct['CODE'],
                           orientation='h',
                           name='',                   
                           hovertemplate='<br>'.join([
                            'Q: %{x}'])
                       )),

        barh_code.update_layout(title= {'text': '<b>Code par Quantite <b>', 'y':0.95, 'x':0.5},
                               xaxis_title="Quantite",
                               yaxis_title="Code", font=dict(
                                    family="Ubuntu",
                                    size=15,
                                    color="RebeccaPurple"),
                               yaxis=dict(dtick=1, categoryorder='total ascending'),
                               height=1100, width=900)


       ## BAR 'CODE'
        fig_code = px.bar(code_date, x='DATE', y="QUANTITE", color='CODE', height=740,
                        color_discrete_sequence=px.colors.qualitative.Light24)
        fig_code = fig_code.update_xaxes(tickangle=50, nticks=40)
        fig_code = fig_code.update_layout(ts_layout)
        fig_code = fig_code.update_layout(title={'text': '<b>Code par Jour<b>', 'y':0.95, 'x':0.5 })


        return  barh_code , table_code, fig_code
    else:
        return dash.no_update, dash.no_update, dash.no_update
    
# =======================================================================================================

if __name__ == '__main__':
    app.run_server( port=3610)

from datetime import date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash 
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, register_page, callback
from dash.dash_table import DataTable
from dash.dash_table.Format import Format, Scheme, Group

register_page(__name__, path="/", name='Rapport Namia', title='Rapport', order=0, description='Namia Rapport Analysis')


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
code_by_day = pd.read_excel('./assets/namia/code_by_day.xlsx')
code_by_day.loc[:, 'CODE'] = code_by_day.loc[:, 'CODE'].astype('str')
produit_by_day = pd.read_excel('./assets/namia/produit_by_day.xlsx')

reception = pd.read_excel('./assets/namia/produit_by_day.xlsx')
mep = pd.read_excel('./assets/namia/mep_rapport.xlsx')
rapprochement = pd.read_excel('./assets/namia/rapprochement_rapport.xlsx')

#=========================================START APP===============================================
# stylesheet with the .dbc class
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css], 
#     meta_tags=[
#         {"name": "viewport", "content": "width=device-width, initial-scale=1"},
#         ])

# server = app.server
# app.title = "Rapport"

# navbar = dbc.NavbarSimple(
#     [
#         dbc.Button("NAMIA", href="/", color="secondary", className="me-1"),
#         dbc.Button("ASMAC", href="/stocks/AAPL", color="secondary"),
#     ],
#     brand="Rapport NAMIA",
#     color="primary",
#     dark=True,
#     className="mb-2",
# )

layout = html.Div([
    # html.H1("Rapport de NAMIA", style={"textAlign":"center", 'backgroundColor': '#45E3E9'}),
    # html.H5('Date', className='bg-light col-sm-1 row justify-content-md-center'),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        display_format='DD/MM/YYYY',
        min_date_allowed=date(2022, 7, 2),
        max_date_allowed=date(2022,9, 30),
        initial_visible_month= date(2022, 9, 30) ,
        start_date = date(2022, 7, 2),
        end_date=date(2022,9, 30),
        start_date_placeholder_text='du',
        day_size=30,
        first_day_of_week=1,
        
    ),
    html.Br(),
    html.Br(),

    ## $$$$$$$$$$$$$$$$$$$$$$$$$ PRODUIT TAB $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # Flex container
    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', 
             children=[
    dcc.Tab(label='Produit', value='tab-1-example-graph',
           children=[
               # dcc.Store stores the produit store
               dcc.Store(id='store-produit'),
               dcc.Store(id='produit-date-data'),
               html.Div([ 
               html.Div([
        dcc.Graph(id='barh_produit', style={'width': '120vh', 'height': '90vh',
                                       'display': 'inline-block'
                                       }),

        ], style={'width': '60%', 'display': 'inline-block'
               }),

        # Table container
        html.Div(id='data-table1', style={'display': 'inline-block', 'width': '80vh', #'height': '110vh',
                                          'margin-left': '25px', 'margin-top': 100})
           ],  style={'display': 'flex', 'height': '100vh'} ),
               
        dcc.Graph(id='produit_graph', style={'height': '100vh'}),
        
        html.A([html.H6('Feedback')], title ='email_me', href='mailto:abderahmanah605@gmail.com', target='_blank',
                      style={'position':'absolute', 'right':'10px'})
       ]) ,
    
    ## $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ CODE TAB $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 

    dcc.Tab(label='Code', value='tab-2-example-graph',
           children=[
               # dcc.Store stores the code store
               dcc.Store(id='store-code'),
               dcc.Store(id='code-date-data'),
               html.Div([ 
               html.Div([
        dcc.Graph(id='barh_code', style={'width': '120vh', 'height': '90vh',
                                       'display': 'inline-block',
                                        "maxHeight": "600px", "overflowY": "scroll", "overflowX": 'hidden'} ),

        ], style={'width': '60%', 'display': 'inline-block'} ),

        # Table container
        html.Div([
        html.Div(id='data-table2', style={'display': 'inline-block', 'width': '60vh', "overflowX": 'hidden',
                                            # 'height': '100vh',
                                            #"overflowY": "hidden",
                                           'margin-left': '75px', 'margin-top': 100
                                           })
                                ], style={'width': '20%'} ),
        ], style={'display': 'flex' ,'height': '100vh'} ),
        
        dcc.Graph(id='code_graph'),
        html.A([html.H6('Feedback')], title ='email_me', href='mailto:abderahmanah605@gmail.com', target='_blank',
                style={'position':'absolute', 'right':'10px'})
       ]),
    
        ## $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Tableau TAB $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        dcc.Tab(label='MEP-Reception', value='tab-3-example-graph',
           children=[
               # dcc.Store stores the produit store
               dcc.Store(id='store-tableau'),
               dcc.Store(id='store-moyenne'),

        html.Br(),
        html.Br(),       
        html.Div(id='moyenne-data'),
        html.Br(),

        
        html.Div([ 
        html.H4('Rapprochement-MEP-Reception', style={'margin-left': '25px'}, className='text-light bg-secondary'),
        html.Div(id='data-table3', style={'margin-left': '55px', 'margin-top': 40
                                          })
           ],   style={ 'height': '70vh', 'width':'90%'} 
           ),
        
        html.A([html.H6('Feedback')], title ='email_me', href='mailto:abderahmanah605@gmail.com', target='_blank',
                style={'position':'absolute', 'right':'10px'})
       ])
    ]),

], style={'maxWidth': '100%',  'overflowX': 'hidden'})


## ====================================START (store data) =============================================================
@callback(
    Output('store-produit', 'data'),
    Output('store-code', 'data'), 
    Output('produit-date-data', 'data'),
    Output('code-date-data', 'data'),
    Output('store-tableau', 'data'),
    Output('store-moyenne', 'data'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date') )
def clean_data(start, end):
    # some expensive data processing step
    ## FILTER THE DATE
    produit_date = produit_by_day[produit_by_day['DATE'].between(start, end)]
    code_date = code_by_day[code_by_day['DATE'].between(start, end)]

    ## products sorted by quantity
    pro_quantity = produit_date.groupby('PRODUIT')[['QUANTITE']].sum(numeric_only=True).sort_values('QUANTITE', ascending=False).reset_index()
    pro_quantity['POURCENTAGE'] = pro_quantity['QUANTITE'].map(lambda x: round(x*100/pro_quantity['QUANTITE'].sum(),2))
    ## STANDART SORT (PRODUIT)
    custom_dict = {'T03':0, 'T04':1, 'T05':2, "T06":3, "T07":4, "T08":5, "PR1":6, "PR2":7, "PR3":8, "PR":9}
    pro_quantity = pro_quantity.sort_values(by=['PRODUIT'], key=lambda x: x.map(custom_dict))

    ## POURCENTAGE for Code
    code_perct = code_date.groupby('CODE')[['QUANTITE']].sum(numeric_only=True).sort_values('QUANTITE', ascending=False).reset_index()
    code_perct['POURCENTAGE'] = code_perct['QUANTITE'].map(lambda x: round(x*100/code_perct['QUANTITE'].sum(),2))

    ## -------------------- tableau TAB ---------------------------------------------------------------
    mep_dff = mep[mep['DATE'].astype('str').between(start,end)]
    mep_dff = pd.DataFrame( {'PRODUIT': mep_dff[mep_dff.columns[1:-1]].sum().index, 'MEP': mep_dff[mep_dff.columns[1:-1]].sum().values})
    
    ## ***********************************************************************************************
    ## select date and group by produit
    rec_dff = reception[reception['DATE'].between(start, end)]
    rec_dff = rec_dff.groupby('PRODUIT').sum(numeric_only=True).reset_index()
    rec_dff.rename(columns = {'QUANTITE': 'RECEPTION'}, inplace=True)
    rec_dff = rec_dff.reindex([4,5,6,7,8,1,2,3])
    
    ## Calcul of Moyenne
    moyenne_dff = reception.set_index(['DATE', 'PRODUIT'])['QUANTITE'].unstack().reset_index()
    ## selected date
    moyenne_dff = moyenne_dff[moyenne_dff['DATE'].between(start, end)]
    ## drop T08 and PR
    moyenne_dff.drop(['PR', 'T08'], axis=1, inplace=True)
    ## ADD TOTAL ROW
    moyenne_dff.loc['Total'] = moyenne_dff.sum(numeric_only=True)
    ##   ___________________________________
    
    ## ***********************************************************************************************
    rapprochement_dff = rapprochement[rapprochement['DATE'].between(start, end)] 
    rapprochement_dff = pd.DataFrame(columns = ['MEP (Kg)'], data = rapprochement_dff.sum(axis=0, numeric_only=True)).reset_index().rename(columns={'index':'PRODUIT'})    

    ## ===============================================================================================
    ## MERGE ALL DFs together
    FINAL_DF = mep_dff.merge(rec_dff.merge(rapprochement_dff, on='PRODUIT'), on='PRODUIT')
    FINAL_DF['DIFFERENCE'] = FINAL_DF['MEP (Kg)'] - FINAL_DF['RECEPTION']
    ## ALL 'TOTAL' ROW
    FINAL_DF.loc['Total'] = FINAL_DF.sum(numeric_only=True)

    # more generally, this line would be
    # json.dumps(cleaned_df)
    return [pro_quantity.to_json(date_format='iso', orient='split'), 
            code_perct.to_json(date_format='iso', orient='split'),
            produit_date.to_json(date_format='iso', orient='split'),
            code_date.to_json(date_format='iso', orient='split'),
            FINAL_DF.to_json(date_format='iso', orient='split'),
            moyenne_dff.to_json(date_format='iso', orient='split')
            ]



## =========================================START Produit Callback============================================
@callback(
    Output('barh_produit', 'figure'),
    Output('data-table1', 'children'),
    Output('produit_graph', 'figure'),
    Input('tabs-example-graph', 'value'),
    Input('store-produit', 'data'),
    Input('produit-date-data', 'data'),
)
def update_produit(tab, cleaned_data, produit_date):
    
    if tab == 'tab-1-example-graph':

        dff = pd.read_json(cleaned_data, orient='split')
        produit_date_df = pd.read_json(produit_date, orient='split')

        # --------------------------------TABLE------------------------------------------------------------
        formatted = Format()
        formatted = formatted.scheme(Scheme.fixed).precision(0).group(Group.yes).group_delimiter(' ')
        cols = [dict(name = 'PRODUIT', id = 'PRODUIT'),
                dict(name =  'QUANTITE', id = 'QUANTITE', type = 'numeric', format = formatted),
                dict(name = 'POURCENTAGE', id = 'POURCENTAGE', type = 'numeric')   
                                            ]
                                            
        table_produit = DataTable(columns = cols,
                          data = dff.to_dict('records'),
                          style_data_conditional=([
                            {
                                'if': {
                                    'filter_query': '{{POURCENTAGE}} = {}'.format(i),
                                    
                                },
                                'backgroundColor': '#6bf249'
                            } for i in dff['POURCENTAGE'].nlargest(3)
                          ]),
                          style_header={'whiteSpace': 'normal', 'fontWeight': 'bold'},
                          fixed_rows={'headers': True},
                          style_table={ 'width': 440, },
                          sort_action='native',
                          filter_action='native',
                          #column_selectable="multi",
                          #row_selectable='multi',
                          selected_columns=[],
                          selected_rows=[],
                          export_format='xlsx',
                          ),

        # ------------------------------------------------barh--------------------------------------------------
        ## barh 'PRODUIT'
        barh_produit = go.Figure()
        barh_produit.add_trace(go.Bar(x = dff['QUANTITE'], y = dff['PRODUIT'],
                           orientation='h',
                           name='',
                           text=dff['QUANTITE'],
                           textposition='auto'                   
                       )),
        barh_produit.update_xaxes(tickformat="digit")
        barh_produit.update_layout(title= {'text': '<b>Produit par Quantite <b>', 'y':0.95, 'x':0.5},
                               xaxis_title="Quantite",
                               yaxis_title="Produit", font=dict(
                                    family="Ubuntu",
                                    size=18,
                                    color="RebeccaPurple"),
            yaxis= {'categoryarray':['PR', 'PR3', 'PR2', 'PR1', 'T08', 'T07', 'T06', 'T05', 'T04', 'T03']})
            # 'T03', 'T04', 'T05', 'T06', 'T07', 'T08', 'PR1', 'PR2', 'PR3', 'PR'
        # ------------------------------------------------BAR-----------------------------------------------
        ## BAR 'PRODUIT'
        fig_produit = px.bar(produit_date_df, x='DATE', y="QUANTITE", color='PRODUIT', height=700,
                        color_discrete_sequence=px.colors.qualitative.Light24)
        fig_produit = fig_produit.update_xaxes(tickangle=50, nticks=40)
        fig_produit = fig_produit.update_yaxes(tickformat="digit")
        fig_produit = fig_produit.update_layout(ts_layout)
        fig_produit = fig_produit.update_layout(title={'text': '<b>Produit par Jour<b>', 'y':0.95, 'x':0.5})

    
        return  barh_produit, table_produit, fig_produit
    
    else:
        return dash.no_update, dash.no_update, dash.no_update
    
    ## =================================END PRODUIT Callabck ==============================================
    
    
## ====================================START Code Callback==================================================
@callback(
    Output('barh_code', 'figure'),
    Output('data-table2', 'children'),
    Output('code_graph', 'figure'),
    Input('tabs-example-graph', 'value'),
    Input('store-code', 'data'),
    Input('code-date-data', 'data')
)

def update_code(tab, cleaned_data, code_date):     
    if tab == 'tab-2-example-graph':
        
        dff = pd.read_json(cleaned_data, orient='split')
        dff.loc[:, 'CODE'] = dff.loc[:, 'CODE'].astype('str')

        code_date_df = pd.read_json(code_date, orient='split')
        code_date_df.loc[:, 'DATE'] = code_date_df.loc[:, 'DATE'].astype('str')
        code_date_df.loc[:, 'CODE'] = code_date_df.loc[:, 'CODE'].astype('str')

        ## TABLE 2
        formatted = Format()
        formatted = formatted.scheme(Scheme.fixed).precision(0).group(Group.yes).group_delimiter(' ')
        cols = [dict(name = 'CODE', id = 'CODE'),
                dict(name =  'QUANTITE', id = 'QUANTITE', type = 'numeric', format = formatted),
                dict(name = 'POURCENTAGE', id = 'POURCENTAGE', type = 'numeric')   
                                            ]
        table_code = DataTable(columns = cols,
                          data = dff.to_dict('records'),
                          style_data_conditional=([
                            {
                                'if': {
                                    'filter_query': '{{POURCENTAGE}} = {}'.format(i),
                                    
                                },
                                'backgroundColor': '#6bf249' 
                            } for i in dff['POURCENTAGE'].nlargest(3)
                          ]),

                          page_size=12,
                          style_cell={
                                # all three widths are needed to fix columns' width
                                'minWidth': '65px', 'width': '65px', 'maxWidth': '65px',
                                'whiteSpace': 'normal' },
                          style_header={'whiteSpace': 'normal', 'fontWeight': 'bold'},
                          fixed_rows={'headers': True},
                          sort_action='native',
                          filter_action='native',
                          #column_selectable="multi",
                          #row_selectable='multi',
                          selected_columns=[],
                          selected_rows=[],
                          export_format='xlsx',
                          ),

        ## barh 'CODE'
        barh_code = go.Figure()
        barh_code.add_trace(go.Bar(x = dff['QUANTITE'], y = dff['CODE'],
                           orientation='h',
                           name='',
                           text=dff['QUANTITE'],
                           textposition='outside'                   
                       )),
        barh_code.update_xaxes(tickformat="digit")
        barh_code.update_layout(title= {'text': '<b>Code par Quantite <b>', 'y':0.95, 'x':0.5},
                               xaxis_title="Quantite",
                               yaxis_title="Code", font=dict(
                                    family="Ubuntu",
                                    size=15,
                                    color="RebeccaPurple"),
                               yaxis=dict(dtick=1, categoryorder='total ascending'),
                               height=1100, width=900)


       ## BAR 'CODE'
        fig_code = px.bar(code_date_df, x='DATE', y="QUANTITE", color='CODE', height=740,
                        color_discrete_sequence=px.colors.qualitative.Light24)
        fig_code = fig_code.update_xaxes(tickangle=50, nticks=40)
        fig_code = fig_code.update_yaxes(tickformat="digit")
        fig_code = fig_code.update_layout(ts_layout)
        fig_code = fig_code.update_layout(title={'text': '<b>Code par Jour<b>', 'y':0.95, 'x':0.5 })

        return barh_code, table_code, fig_code
    else:
        return dash.no_update, dash.no_update, dash.no_update
## ===================================== END code Callback ================================================

## ==========================START Tabeau TAB callback ===================================================
@callback(
    Output('data-table3', 'children'),
    Output('moyenne-data', 'children'),
    Input('tabs-example-graph', 'value'),
    Input('store-tableau', 'data'),
    Input('store-moyenne', 'data'),
)

def tableau(tab, final_data, moyenne_data):
    if tab == 'tab-3-example-graph':
        final_df = pd.read_json(final_data, orient='split')
        moyenne_df = pd.read_json(moyenne_data, orient='split')

        ## TABLEAU
        formatted = Format()
        formatted = formatted.scheme(Scheme.fixed).precision(2).group(Group.yes).group_delimiter(' ')

        tableau = DataTable(columns = [{'name': col, 'id': col}
                                    if col == 'PRODUIT' or col == 'MEP'
                                    else {'name': col, 'id': col, 'type': 'numeric', 'format': formatted}  
                                    for col in final_df.columns],
                          data = final_df.to_dict('records'),
                          style_data_conditional=([
                            {
                                'if': {
                                    'filter_query': '{DIFFERENCE} < 0',
                                    'column_id': 'DIFFERENCE'
                                },
                                'color': 'tomato',
                                'fontWeight': 'bold'
                            },
                            {
                                'if': {
                                    'filter_query': '{PRODUIT} is blank'
                                },
                                'fontWeight': 'bold'
                            }
                          ]),

                          style_header={'whiteSpace': 'normal', 'fontWeight': 'bold'},
                          fixed_rows={'headers': True},
                          sort_action='native',
                          filter_action='native',
                          export_format='xlsx',
                          ),

        ## moyenne
        # total
        total = moyenne_df.loc['Total', moyenne_df.columns[1:].to_list()].sum()
        # moyenne europe
        moy_europe = round(moyenne_df.loc['Total', ['PR1', 'T03', 'T04', 'T05', 'T06']].sum()*100/total, 2).astype('str')+'%'
        # moyenne japon
        moy_japon = round(moyenne_df.loc['Total', ['PR2', 'PR3', 'T07']].sum()*100/total, 2).astype('str')+'%'

        moyenne = [html.Ul([
               html.Li(dcc.Markdown(f'Moyenne Japon: **{moy_japon}**')),
               html.Li(dcc.Markdown(f'Moyenne Europe: **{moy_europe}**')),
                ]) ]
            
        return tableau, moyenne
    else:
        return dash.no_update, dash.no_update
    
    ## ======================== END TABLEAU TAB Callback =====================================================
    
# =======================================================================================================

# if __name__ == '__main__':
#     app.run_server(port=9131)

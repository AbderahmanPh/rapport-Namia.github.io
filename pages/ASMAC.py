import dash
from dash import dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px


# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
dash.register_page(__name__, path='/asmac', title='ASMAC Analysis', name='MEP asmac', order=1 )


df = pd.read_excel("assets/asmac/journal_mep.xlsx")


layout = html.Div([
  
      html.H2('ASMAC'),
    dbc.Row(
            [
        dbc.Col([ 
        dcc.Dropdown(
        options=[
            {"label": "Journal MEP", "value": "mep"},
            {"label": "Journal par Moi", "value": "moi"},
            {"label": "Journal par Espece", "value": "espece"},
        ],
        id="dropdown_download",
        placeholder="Choisissez fichier à télécharger",
      ) ], xs=7, sm=5, md=4, lg=3, xl=2 ), 

      dbc.Col([

        html.Button(
          "Télécharger", id="btn_csv",
          className='btn-class',
        ),
      ], xs=2, sm=6, md=6, lg=6, xl=6 ),

    ]),

  
    html.Br(),
    html.Br(),

    dcc.Download(id="download"),

    ## ====================================== Tabs =================================================
    dcc.Tabs([
      ##------------------------------------Production-Bateau ------------------------------------
      dcc.Tab([
      dcc.Loading([
        dcc.Dropdown(
          id = 'dropdown',
          value = 'Date',
          options = ['Date', 'Espece'],
          clearable=False ,
          style={'font-size': '15px', 'width': '240px'}
        ),
      dcc.Graph(id="bar-graph", config={'displayModeBar': False}),
        ], color="#119DFF", fullscreen=False, type='dot'),

      html.A('Feedback', title ='Email_me', href='mailto:abderahmanah605@gmail.com?subject=Feedback from rapport-asmac (tab: Production-Bateau)', target='_blank',
                className='feedback-btn'),

      ], label="Production-Bateau"),


    ##------------------------------------- Tab Espece-Date -----------------------------------------
    dcc.Tab([
      dcc.Loading([
        dcc.Graph(id="line-graph", config={'displayModeBar': False}), 
      ], color="#119DFF", fullscreen=False, type='dot'),

        html.A('Feedback', title ='Email_me', href='mailto:abderahmanah605@gmail.com?subject=Feedback from rapport-asmac (Tab: Espece-Date)', target='_blank',
                className='feedback-btn'),

      ], label="Espece-Date"),

    ## -------------------------------------------Tab Tableau -----------------------------------------
    dcc.Tab([
      html.Br(),
      dcc.Loading([
      html.Div([
      html.Div(id='table-id', style={'margin-left': '7px', 'margin-top': 30, 'height': '86vh'})
      ], style={ 'width':'90%'} ),
      ], color="#119DFF", fullscreen=False, type='dot'),

      html.A('Feedback', title ='Email_me', href='mailto:abderahmanah605@gmail.com?subject=Feedback from rapport-asmac (Tab: Tableau)', target='_blank',
                className='feedback-btn'),
    ], 
    label="Tableau"),

  ])
    
])

##========================================== callbacks ==========================================================
@callback(
    Output('bar-graph', 'figure'),
    Output("line-graph", "figure"),
    Output('table-id', 'children'),  
    Input('dropdown', 'value'),
)

def mep_graph(value):
  dff0 = df

  ## fill na with 0
  dff0.fillna(0, inplace=True)
  ## columns
  cols = dff0.columns.to_list()

  ## convert cols to int
  dff0[cols[2:]] = dff0[cols[2:]].astype('int')

  ## ============================================= Tableau ===========================================================
  table_data = dff0.groupby([dff0['Date'].dt.strftime('%B'), 'Espece'], sort=False)[cols].sum(numeric_only=True).reset_index()
  ## replace eng months names with the french ones
  table_data.replace(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
                inplace=True)
  ### ADD TOTAL COL AND ROW
  table_data['Total'] = table_data.sum(axis=1, numeric_only=True)
  table_data.loc['Total'] = table_data.sum(axis=0, numeric_only=True)

  table = dash_table.DataTable(
    # id="table",
    columns=[{"name": str(i), "id": str(i)} for i in table_data.columns],
    data=table_data.to_dict("records"),
    style_data_conditional=([
                            {
                                'if': {
                                    # 'filter_query': '{Total}',
                                    'column_id': 'Total'
                                },
                                'fontWeight': 'bold'
                            },
                            {
                                'if': {
                                    'filter_query': '{{Total}} = {}'.format(table_data[table_data['Espece'] == 'POULPE']['Total'].max())
                                },
                                'backgroundColor': '#6bf249'
                            },
                            {
                                'if': {
                                    'filter_query': '{{Total}} = {}'.format(table_data[table_data['Espece'] == 'CALAMAR']['Total'].max())
                                },
                                'backgroundColor': '#6bf249'
                            },
                                                        {
                                'if': {
                                    'filter_query': '{{Total}} = {}'.format(table_data[table_data['Espece'] == 'SEICHE']['Total'].max())
                                },
                                'backgroundColor': '#6bf249'
                            },
                            ## ======== STYLE min() =======================================
                            {
                                'if': {
                                    'filter_query': '{{Total}} = {}'.format(table_data[table_data['Espece'] == 'POULPE']['Total'].min())
                                },
                                'backgroundColor': 'tomato'
                            },
                            {
                                'if': {
                                    'filter_query': '{{Total}} = {}'.format(table_data[table_data['Espece'] == 'CALAMAR']['Total'].min())
                                },
                                'backgroundColor': 'tomato'
                            },
                                                        {
                                'if': {
                                    'filter_query': '{{Total}} = {}'.format(table_data[table_data['Espece'] == 'SEICHE']['Total'].min())
                                },
                                'backgroundColor': 'tomato'
                            },
                            {
                                'if': {
                                    'filter_query': '{Date} is blank'
                                },
                                'fontWeight': 'bold'
                            }
                          ]),

    style_header={'whiteSpace': 'normal', 'fontWeight': 'bold'},
    # style_table={'maxHeight':'80vh','height':'80vh'},
    filter_action="native",
    sort_action="native",
  )

  #-------------------------------------- Bar chart -----------------------------------------------------------------
  df_date = dff0.groupby([dff0['Date'].dt.strftime('%B')], sort=False)[cols].sum(numeric_only=True).reset_index()
  df_date = df_date.melt(id_vars=['Date'], value_vars=cols[2:], var_name='Asmac', value_name='Quantite')
  df_date.replace(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                  ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
                  inplace=True)

  df_espece = dff0.groupby(['Espece'], sort=False)[cols].sum(numeric_only=True).reset_index()
  df_espece = df_espece.melt(id_vars=['Espece'], value_vars=cols[2:], var_name='Asmac', value_name='Quantite')
  
  if value == 'Date':
    fig = px.bar(df_date, x="Quantite", y="Asmac", color=f"{value}", title="MEP 2eme Trimestre", height=500, orientation='h', text_auto=True)
    fig.update_layout(title= {'text': '<b>Journal MEP<b>', 'y':0.95, 'x':0.5},
                       xaxis_title="Quantite",
                       yaxis_title="Asmac", font=dict(
                            family="Ubuntu",
                            size=15,
                            color="RebeccaPurple"),
                          height=500, margin=dict(pad=6))

  else:
    fig = px.bar(df_espece, x="Quantite", y="Asmac", color=f"Espece", title="MEP 2eme Trimestre", height=500, orientation='h', text_auto=True)
    fig.update_layout(title= {'text': '<b>Journal MEP<b>', 'y':0.95, 'x':0.5},
                       xaxis_title="Quantite",
                       yaxis_title="Asmac", font=dict(
                            family="Ubuntu",
                            size=15,
                            color="RebeccaPurple"),
                          height=500, margin=dict(pad=6))

  ## ============================== line chart ====================================================================
  df_vs = table_data.melt(id_vars=cols[:2], value_vars=cols[2:], var_name='Asmac', value_name='Quantite')
  df_vs = df_vs.groupby(['Date', 'Espece'], sort=False).sum(numeric_only=True).reset_index()


  line_fig = px.line(df_vs, x="Date", y="Quantite", color=f"Espece", title="MEP 2eme Trimestre", height=700, markers=True)
  line_fig.update_layout(title= {'text': '<b>Journal MEP<b>', 'y':0.95, 'x':0.5},
                        xaxis_title="Date",
                        yaxis_title="Quantite", font=dict(
                              family="Ubuntu",
                              size=15,
                              color="RebeccaPurple"),
                            height=500,
                      margin=dict(pad=6),
                      # margin=dict(l=20, r=40)
                  )
  line_fig.update_yaxes(tickformat="digit")
  
  return fig, line_fig, table

##============================================== download button =================================================
@callback(
  Output("download", "data"),
  Input("btn_csv", "n_clicks"),
  State("dropdown_download", "value"),
  prevent_initial_call=True,
)
def download(clicks, download_file):  
  dff = df

  ## fill na with 0
  dff.fillna(0, inplace=True)
  ## columns
  cols = dff.columns.to_list()

  ## convert cols to int
  dff[cols[2:]] = dff[cols[2:]].astype('int')

  if download_file == 'mep': 
    final_dff = dff.groupby([dff['Date'].dt.strftime('%B'), 'Espece'], sort=False)[cols].sum().reset_index()
    ## replace eng months names with the french ones
    final_dff.replace(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                  ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
                  inplace=True)
    ### ADD TOTAL COL AND ROW
    final_dff['Total'] = final_dff.sum(axis=1, numeric_only=True)
    final_dff.loc['Total'] = final_dff.sum(axis=0, numeric_only=True)

    return dcc.send_data_frame(final_dff.to_excel, 'journal de la peche.xlsx', index=False)

  elif download_file == 'moi':
    dff_date = dff.groupby([dff['Date'].dt.strftime('%B')], sort=False)[cols].sum().reset_index()
    dff_date.replace(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                  ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
                  inplace=True)
    ### ADD TOTAL COL AND ROW
    dff_date['Total'] = dff_date.sum(axis=1, numeric_only=True)
    dff_date.loc['Total'] = dff_date.sum(axis=0, numeric_only=True)

    return dcc.send_data_frame(dff_date.to_excel, 'journal par Moi.xlsx', index=False)

  if download_file == 'espece':
    dff_espece = dff.groupby(['Espece'], sort=False)[cols].sum().reset_index()
    ### ADD TOTAL COL AND ROW
    dff_espece['Total'] = dff_espece.sum(axis=1, numeric_only=True)
    dff_espece.loc['Total'] = dff_espece.sum(axis=0, numeric_only=True)

    return dcc.send_data_frame(dff_espece.to_excel, 'journal par Espece.xlsx', index=False)

# if __name__=='__main__':
#   app.run_server(debug=True, port=7261)
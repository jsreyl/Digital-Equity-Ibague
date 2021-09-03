# Import required libraries
import pickle
import copy
import pathlib
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import os
import geopandas
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import dash_leaflet as dl
import json
import haversine as hs
import geopy
from geopy.distance import geodesic
import geocoder

#import scripts to connect aws database
from connector import get_Usabilidad
from connector import get_conexiones
from connector import get_Variables_Censo
from connector import get_Data_Zonas
from connector import get_Data_Manzanas
from connector import get_Ubicacion_Zonas
from connector import get_df_model



app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.SLATE],
                meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)




#Data
DATA_DIR = "data"
#df_path = os.path.join(DATA_DIR, "data_zonas.csv")
#df = pd.read_csv(df_path)
df=get_Data_Zonas()
geo_path=os.path.join(DATA_DIR, "MGN_ANM_MANZANA_IBAGUE.geojson")
ibague_mzn = geopandas.read_file(geo_path, driver="GeoJson")
ibague_mzn['porc_con_internet']=(ibague_mzn['TP19_INTE1']/ibague_mzn['TVIVIENDA'])*100
ibague_mzn2 = ibague_mzn[["LATITUD","LONGITUD","TP19_INTE1","TVIVIENDA","TP16_HOG",'TP34_1_EDA','TP34_2_EDA','TP34_3_EDA','TP34_4_EDA','TP34_5_EDA','TP34_6_EDA','TP34_7_EDA','TP34_8_EDA','TP34_9_EDA']]
#var_path=os.path.join(DATA_DIR, "Variables_Censo.csv")
#df_var=pd.read_csv(var_path)
df_var=get_Variables_Censo()
df_id=df.iloc[:, 1]
df_id=df_id.sort_values()
#modelo_path=os.path.join(DATA_DIR, "df_model.csv")
#modelo=pd.read_csv(modelo_path)
modelo=get_df_model()
ibague_mzn['PORC_VIVIENDA']=(ibague_mzn['TP9_1_USO']/ibague_mzn['TVIVIENDA'] )*100 
ibague_mzn['PORC_OTROSUSOS']=100-ibague_mzn['PORC_VIVIENDA'] 
ibague_mzn['PORC_ENERGIA']=(ibague_mzn['TP19_EE_1']/ibague_mzn['TVIVIENDA'] )*100
ibague_mzn['PORC_E1']=(ibague_mzn['TP19_EE_E1']/ibague_mzn['TVIVIENDA'] )*100
ibague_mzn['PORC_E2']=(ibague_mzn['TP19_EE_E2']/ibague_mzn['TVIVIENDA'] )*100
ibague_mzn['PORC_E3']=(ibague_mzn['TP19_EE_E3']/ibague_mzn['TVIVIENDA'] )*100
ibague_mzn['PORC_E4']=(ibague_mzn['TP19_EE_E4']/ibague_mzn['TVIVIENDA'] )*100
ibague_mzn['PORC_E5']=(ibague_mzn['TP19_EE_E5']/ibague_mzn['TVIVIENDA'] )*100
ibague_mzn['PORC_E6']=(ibague_mzn['TP19_EE_E6']/ibague_mzn['TVIVIENDA'] )*100
ibague_mzn['PORC_ACUE']=(ibague_mzn['TP19_ACU_1']/ibague_mzn['TVIVIENDA'] )*100
ibague_mzn['PORC_ALC']=(ibague_mzn['TP19_ALC_1']/ibague_mzn['TVIVIENDA'] )*100
ibague_mzn['PORC_GAS']=(ibague_mzn['TP19_GAS_1']/ibague_mzn['TVIVIENDA'] )*100
ibague_mzn['PORC_INTE']=(ibague_mzn['TP19_INTE1']/ibague_mzn['TVIVIENDA'] )*100
ibague_mzn['PORC_BAS']=(ibague_mzn['TP19_RECB1']/ibague_mzn['TVIVIENDA'] )*100
ibague_mzn['TP27_PERSO']=ibague_mzn['TP27_PERSO']
ibague_mzn['PORC_H']=(ibague_mzn['TP32_1_SEX']/ibague_mzn['TP27_PERSO'] )*100
ibague_mzn['PORC_M']=(ibague_mzn['TP32_2_SEX']/ibague_mzn['TP27_PERSO'] )*100
ibague_mzn['PORC_0_9']=(ibague_mzn['TP34_1_EDA']/ibague_mzn['TP27_PERSO'] )*100
ibague_mzn['PORC_10_19']=(ibague_mzn['TP34_2_EDA']/ibague_mzn['TP27_PERSO'] )*100
ibague_mzn['PORC_20_29']=(ibague_mzn['TP34_3_EDA']/ibague_mzn['TP27_PERSO'] )*100
ibague_mzn['PORC_30_39']=(ibague_mzn['TP34_4_EDA']/ibague_mzn['TP27_PERSO'] )*100
ibague_mzn['PORC_40_49']=(ibague_mzn['TP34_5_EDA']/ibague_mzn['TP27_PERSO'] )*100
ibague_mzn['PORC_50_59']=(ibague_mzn['TP34_6_EDA']/ibague_mzn['TP27_PERSO'] )*100
ibague_mzn['PORC_60_69']=(ibague_mzn['TP34_7_EDA']/ibague_mzn['TP27_PERSO'] )*100
ibague_mzn['PORC_70_79']=(ibague_mzn['TP34_8_EDA']/ibague_mzn['TP27_PERSO'] )*100
ibague_mzn['PORC_80']=(ibague_mzn['TP34_9_EDA']/ibague_mzn['TP27_PERSO'] )*100
ibague_mzn['PORC_PREE']=(ibague_mzn['TP51PRIMAR']/ibague_mzn['TP27_PERSO'] )*100
ibague_mzn['PORC_SEC']=(ibague_mzn['TP51SECUND']/ibague_mzn['TP27_PERSO'] )*100
ibague_mzn['PORC_0_TP']=(ibague_mzn['TP51SUPERI']/ibague_mzn['TP27_PERSO'] )*100
ibague_mzn['PORC_POST']=(ibague_mzn['TP51POSTGR']/ibague_mzn['TP27_PERSO'] )*100
ibague_mzn['PORC_NIN']=(ibague_mzn['TP51_13_ED']/ibague_mzn['TP27_PERSO'] )*100



#Plot connections
#Bar plot
#usos_path = os.path.join(DATA_DIR, "Usabilidad_Zonas.csv")
#df_u = pd.read_csv(usos_path)
df_u=get_Usabilidad()

#Scatter Map
lats=df["Latitud"] 
lons=df["Longitud"]
h_name=df['ZONAS VIBRA']
total=len(df['ZONAS VIBRA'])


#Pin ID
MAP_ID = "map-id"
COORDINATE_CLICK_ID = "coordinate-click-id"



#map model2
modelo['prob_logit']=modelo['prob_logit']*100
modelo = modelo[['COD_DANE_A', 'prob_logit']]
ibague_mzn = pd.merge(ibague_mzn, modelo, how="left", on=["COD_DANE_A"])
potencial=ibague_mzn[ibague_mzn['prob_logit']>75]
lats2=potencial["LATITUD"] 
lons2=potencial["LONGITUD"]

map3 = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="prob_logit",
                    height=600,
                    color_continuous_scale="YlOrRd",
                    labels={'prob_logit':'%'},
                           )

map3.add_scattermapbox( lat=lats, lon=lons, 
                      mode = 'markers', 
                      marker_size=6,
                      marker_color='#13c6e9', name="Zonas Vibra")
map3.add_scattermapbox( lat=lats2, lon=lons2, 
                      mode = 'markers', 
                      marker_size=8,
                      marker_color='#00FF00', hoverinfo='none', name="Manzanas potenciales",
                     opacity=0.7,
                     )



map3.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
map3.update_layout(
            transition_duration=500,
            legend=dict(x=0,y=1,font=dict(size=15,color="white"),
            bgcolor='rgba(255, 255, 255, 0.5)',
                       ))

map3.update_layout(transition_duration=500)
map3['layout'].update(
            margin=dict(l=0,r=0,b=0,t=0), 
            showlegend=True, 
            height=500)
map3.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
        )
map3['layout'].update(margin=dict(l=0,r=0,b=0,t=0))


# Create app layout
app.layout = html.Div(
    [
        html.Div(id="output-clientside"),
        
        
        html.Div(
            [
                html.Div(
                    [
                        html.Img(src=app.get_asset_url("logo_administracion.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "10px",
                            },
                        )
                    ],
                    className="two columns",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H1(
                                    "Zonas Vibra Ibagué",
                                    style={"margin-bottom": "10px"},
                                ),
                                
                            ]
                        )
                    ],
                    className="eight columns",
                    id="title",
                ),

            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "10px"},
        ),
        html.Div([html.Div(html.H3("  "),className="two columns"),
            
        html.Div(
            [dbc.Tabs(
                [
                    dbc.Tab(label='ESTADÍSTICAS', tab_id='estad', id='estad-tab',label_style={"font-size": '23px', 'border-radius': '6px', "margin-right":"10px", "width":"190px", "text-align":"center" }),
                    dbc.Tab(label='DEMOGRAFÍA', tab_id='demograf', id='estad-tab3',label_style={"font-size": '23px', 'border-radius': '6px',"margin-right":"10px" , "width":"190px", "text-align":"center" }),
                    dbc.Tab(label='PROYECCIÓN', tab_id='modelo', id='estad-tab2',label_style={"font-size": '23px', 'border-radius': '6px',"margin-right":"10px" , "width":"190px", "text-align":"center" }),
                    dbc.Tab(label='POTENCIAL', tab_id='potencial', label_style={"font-size": '23px', 'border-radius': '6px', "width":"190px", "text-align":"center" })
                ],
                id='tabs_id',
                active_tab='estad',
                style={ 'border': 'rgba(0, 0, 0, 0)', 'padding-top':'7px', 'padding-bottom':'10px'}
            
            ),], style={"display": "flex", "justify-content": "center", }, className="eight columns"
        ),
                 ]
        
        ),
        
        
 
    
        dcc.Loading(html.Div(className="row flex-display", id='midContainer2'), color='#13c6e9'),
        html.Div(className="row flex-display", id='midContainer')
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


modal = html.Div(
    [
        dbc.Button("Open modal", id="open"),
        dbc.Modal(
            [
                dbc.ModalHeader("HEADER"),
                dbc.ModalBody("BODY OF MODAL"),
                dbc.ModalFooter(
                    dbc.Button("CLOSE BUTTON", id="close", className="ml-auto")
                ),
            ],
            id="modal",
        ),
    ]
)







# Create callbacks

#Tabs
@app.callback(
    [Output('midContainer','children'),
    Output('midContainer2','children')],
    Input('tabs_id', 'active_tab')
)
def change_tab(active):
    if active=='modelo':
        container= [
            html.Div([
                        
                            dbc.Card([
                                dbc.CardHeader(html.H3("Dirección")),
                                dbc.CardBody(html.Div(id=COORDINATE_CLICK_ID))
                            ]),
                            dbc.Card([
                                dbc.CardHeader(html.H5(["Probabilidad de utilización", html.Img(id="show-model1-modal", src="assets/help.png", n_clicks=0, style={
                                "height": "15px",
                                "width": "auto",
                                "margin-left": "5px",
                            })])),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader("Probabilidad de utilización"),
                                        dbc.ModalBody("Este indicador muestra la probabilidad de que las personas en el área de cobertura (300 metros alrededor) se conecten al menos dos veces al día a una Zona Vibra localizada en el punto seleccionado"),
                                       
                                    ],
                                    id="modal2",
                                    centered=True,
                                    is_open=False,
                                ),
                                dbc.CardBody(html.H3(id='modelo-1'))
                            ]),
                            dbc.Card([
                                dbc.CardHeader(html.H5(["Probabilidad de no proximidad", html.Img(id="show-model2-modal", src="assets/help.png", n_clicks=0, style={
                                "height": "15px",
                                "width": "auto",
                                "margin-left": "5px",
                            })])),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader("Probabilidad de no proximidad"),
                                        dbc.ModalBody("Este indicador muestra la probabilidad de estar ubicado alejado de una Zona Vibra según las características demográficas de la manzana"),
                                        
                                    ],
                                    id="modal3",
                                    centered=True,
                                    is_open=False,
                                ),
                                dbc.CardBody(html.H3(id='modelo-2'))
                            ])
                            
                
                
            ]
            ,className="pretty_container three columns",  style={'height':'500px'}
            ),
        
            html.Div(
               [
                html.H3("Proyección de localización de nuevas Zonas Vibra"),
                dcc.Loading(children=[ dl.Map(
                    id=MAP_ID,
                    style={'width': '500', 'height': '500px'}, 
                    center=[4.435011513227277, -75.20078393517075], 
                    zoom=13, 
                    children=[dl.TileLayer(url='https://api.mapbox.com/styles/v1/carlosruiz/ckry7q3tk08pi17pdhos24xsf/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow'), dl.LayerGroup(id="layer"), dl.LayerGroup(id="layer-2")])], color='#13c6e9'    ),
                
                
            ],className="pretty_container six columns"
        ),
             html.Div([
                            dbc.Card([
                                dbc.CardHeader(html.H5(["Características demográficas", html.Img(id="show-demog-modal", src="assets/help.png", n_clicks=0, style={
                                "height": "15px",
                                "width": "auto",
                                "margin-left": "5px",
                            })])),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader("Características demográficas"),
                                        dbc.ModalBody("Se muestran indicadores con base en el Censo Nacional de Población y Vivienda 2018 de las manzanas en un radio de 300 metros alrededor del punto seleccionado"),
                                        
                                    ],
                                    id="modal4",
                                    centered=True,
                                    is_open=False,
                                ),
                                dbc.Modal(
                                    [
                                        dbc.ModalBody(html.H4("Seleccione un punto en el mapa para conocer las proyecciones al instalar una nueva Zona Vibra")),
                                       
                                    ],
                                    id="modal5",
                                    centered=True,
                                    is_open=False,
                                ),
                                html.H6('Población', style={'padding-left':'15px'}),
                                html.Div(id='personas', style={'padding-left':'25px'}),
                                html.Div(id='hombres', style={'padding-left':'35px'}),
                                html.Div(id='mujeres', style={'padding-left':'35px'}),
                               
                                html.H6('Vivienda', style={'padding-left':'15px', 'padding-top':'5px'}),
                                html.Div(id='viviendas', style={'padding-left':'25px'}),
                                html.Div(id='otros', style={'padding-left':'25px'}),
                                html.Div(id='estrato', style={'padding-left':'25px'}),
                                html.Div(id='con-int', style={'padding-left':'25px'}),
                                
                                html.H6('Edad', style={'padding-left':'15px', 'padding-top':'5px'}),
                                html.Div(id='ed1', style={'padding-left':'25px'}),
                                html.Div(id='ed2', style={'padding-left':'25px'}),
                                html.Div(id='ed3', style={'padding-left':'25px'}),
                                html.Div(id='ed4', style={'padding-left':'25px'}),
                                html.Div(id='ed5', style={'padding-left':'25px'}),
                                html.Div(id='ed6', style={'padding-left':'25px'}),
                                
                                html.H6('Educación', style={'padding-left':'15px', 'padding-top':'5px'}),
                                html.Div(id='edu1', style={'padding-left':'25px'}),
                                html.Div(id='edu2', style={'padding-left':'25px'}),
                                html.Div(id='edu3', style={'padding-left':'25px'}),
                                html.Div(id='edu4', style={'padding-left':'25px'}),
                            ])
                            
                
                
            ]
            ,className="pretty_container three columns"
            )
        ]
        
       
        return container,""
    elif active=='estad':
        container= [
            html.Div([
                             
                html.Div([
                    html.Img(id="show-estad-modal", src="assets/help.png", n_clicks=0, 
                             style={"height": "25px", 'padding-top':'5px','padding-right':'5px','padding-bottom':'5px', "position":"absolute","right":0}),
                    html.H3('Comuna', style={'padding-top':'30px'}),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Filtros"),
                            dbc.ModalBody("Puede filtrar las Zonas Vibra actuales por Comuna y por Zonas Vibra individuales, puede ocultar las Zonas Vibra haciendo click en la leyenda del mapa ubicada arriba a la izquierda"),
                           
                        ],
                        id="modal",
                        centered=True,
                        is_open=False,
                    ),
                    
                    
                    dcc.Dropdown(
                    id='drop-comunas',
                    options=[
                        {'label':'TODAS', 'value':'total'},
                        {'label':'COMUNA 1', 'value':'COMUNA 1'},
                        {'label':'COMUNA 2', 'value':'COMUNA 2'},
                        {'label':'COMUNA 3', 'value':'COMUNA 3'},
                        {'label':'COMUNA 4', 'value':'COMUNA 4'},
                        {'label':'COMUNA 5', 'value':'COMUNA 5'},
                        {'label':'COMUNA 6', 'value':'COMUNA 6'},
                        {'label':'COMUNA 7', 'value':'COMUNA 7'},
                        {'label':'COMUNA 8', 'value':'COMUNA 8'},
                        {'label':'COMUNA 9', 'value':'COMUNA 9'},
                        {'label':'COMUNA 10', 'value':'COMUNA 10'},
                        {'label':'COMUNA 11', 'value':'COMUNA 11'},
                        {'label':'COMUNA 12', 'value':'COMUNA 12'},
                        {'label':'COMUNA 13', 'value':'COMUNA 13'},
                        {'label':'OTRAS', 'value':'OTROS'},                        
                    ], style={'font-size': '12px'},
                    value='total',
                    clearable=False
                ),
                    html.H3('Zona Vibra', style={'padding-top':'30px'}),
                    dcc.Dropdown(
                    id='drop-zona',
                    
                    
                ),
                         
                ],
                        ),
                html.Div(dcc.Graph( id='gauge', style={'padding-top':'95px'}),  ),
                
            ]
            ,className="pretty_container three columns"
            ),
        
            html.Div(dcc.Loading(html.Div(id='main-map')),
                className="pretty_container six columns", ), 
            html.Div(
                    [
                        html.H4('Conexiones por mes', id='fig2-title'),
                        html.Div(dcc.Graph(
                            id='graph-2'), id='graph_2'),
                        html.H4('Tipos de uso', id='fig3-title', style={'padding-top':'15px'}),
                        html.Div(dcc.Graph(
                            id='graph-3'), id='graph_3'),
                        
                        
                    ]
                    ,
                    className="pretty_container three columns",
                )
                
  
                
        ]
        return container,""
    elif active=='demograf':
        container= [
            html.Div([
                             
                html.Div([
                    html.Img(id="show-demograf-modal", src="assets/help.png", n_clicks=0, 
                             style={"height": "25px", 'padding-top':'5px','padding-right':'5px','padding-bottom':'5px', "position":"absolute","right":0}),
                    
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Filtro"),
                            dbc.ModalBody("Puede crear un mapa de calor con variables demográficas del Censo Nacional de Población y Vivienda 2018, puede ocultar las Zonas Vibra haciendo click en la leyenda del mapa ubicada arriba a la izquierda"),
                           
                        ],
                        id="modal6",
                        centered=True,
                        is_open=False,
                    ),
                    
                     html.H3('Variable del CNPV 2018',style={'padding-top':'15px'} ),
                dcc.Dropdown(
                    id='type-variable',
                    options=[{'label': i, 'value':i} for i in df_var[df_var['INCLUIR']=='SI']['DESCRIPCIÓN']],
                    style={'font-size': '12px'},
                    clearable=False,
                    value='NINGUNA'
                )],
                        ),
                
                
            ]
            ,className="pretty_container three columns", style={'height':'120px'}
            ),
        
            html.Div(dcc.Loading(html.Div(id='main-map2')),
                className="pretty_container nine columns", ),
            
                
  
                
        ]
        return container,""
    else:
        container= [
            html.Div([
                        
                        
                            dbc.Card([
                            dbc.CardHeader(html.H3("Potencial en zona urbana", className="card-title"),),
                            dbc.CardBody(
                                [
                                    
                                    html.H5(
                                        "Este mapa indica la probabilidad que una manzana de la ciudad esté alejada de una Zona Vibra según sus características demográficas",
                                        className="card-text",
                                    ),
                                ]
                            ),
                            ]
                                , color="primary"),
                            html.Br(),
                            
                
                
            ]
            ,className="pretty_container three columns", style={'height':'260px'}
            ),
        
            html.Div(
               [
                
                dcc.Graph(figure=map3, id='map-h2'),
                
                
            ],className="pretty_container nine columns", 
        ), ]
        
       
        return "",container

#


#Capture coordinates on map
@app.callback([
    Output(COORDINATE_CLICK_ID, 'children'), 
    Output('layer', 'children'),
    Output('modelo-1', 'children'),
    Output('modelo-2', 'children'),
    Output('layer-2', 'children'),
    Output('personas', 'children'),
    Output('hombres', 'children'),
    Output('mujeres', 'children'),
    Output('estrato', 'children'),
    Output('otros', 'children'),
    Output('con-int', 'children'),
    Output('viviendas', 'children'),
    Output('ed1', 'children'),
    Output('ed2', 'children'),
    Output('ed3', 'children'),
    Output('ed4', 'children'),
    Output('ed5', 'children'),
    Output('ed6', 'children'),
    Output('edu1', 'children'),
    Output('edu2', 'children'),
    Output('edu3', 'children'),
    Output('edu4', 'children'),
],
        
    [Input(MAP_ID, 'click_lat_lng')])
def click_coord(e):
    if e is not None:
        loc1=e
        loc2=zip(ibague_mzn2["LATITUD"],ibague_mzn2["LONGITUD"])
        distancia=[]
        for i in loc2:
            distancia.append(hs.haversine(loc1,i)*1000)

        ibague_mzn2["dist"]=distancia
        df=ibague_mzn2[ibague_mzn2["dist"]<=300]

        df2=df.sum(axis = 0, skipna = True).reset_index()
        df2.columns=['Variable', 'Value']
        df2=df2.T
        df2.columns = df2.iloc[0]
        df2=df2.drop(['Variable'])    
        df2['pct_30_39']=      df2['TP34_4_EDA']/df2[['TP34_1_EDA','TP34_2_EDA','TP34_3_EDA','TP34_4_EDA','TP34_5_EDA','TP34_6_EDA','TP34_7_EDA','TP34_8_EDA','TP34_9_EDA']].sum(axis=1)
        df2['pct_internet']=df2['TP19_INTE1']/df2['TVIVIENDA']
        df2['hogares_vivienda']=df2['TP16_HOG']/df2['TVIVIENDA']
        probability2 = 19.7964-(4.9049*df2['pct_internet'])-(13.1793*df2['hogares_vivienda'])-(41.7552*df2['pct_30_39'])
        probability2 = str(round(math.exp(probability2)/(1+math.exp(probability2))*100,0)) + " %"
        
        distance_min = 500
        for i in range (0, len(ibague_mzn.index)):
            loc_block = (ibague_mzn['LATITUD'][i],ibague_mzn['LONGITUD'][i])
            distance = geodesic(loc_block, e).km
            if distance < distance_min:
                distance_min = distance
                closest_block = i
        prob_logit=str(round(ibague_mzn.iloc[closest_block]['prob_logit'],0)) + " %"
        g=geocoder.mapbox(e, method='reverse', key='pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow')
        location=g.address
        
        max_lat=e[0]+0.002702702
        min_lat=e[0]-0.002702702
        max_lon=e[1]+0.002702702
        min_lon=e[1]-0.002702702
        df=ibague_mzn[
            (ibague_mzn['LATITUD']>min_lat)&
            (ibague_mzn['LATITUD']<max_lat)&
            (ibague_mzn['LONGITUD']>min_lon)&
            (ibague_mzn['LONGITUD']<max_lon)
                     ]
        personas=str(round(df['TP27_PERSO'].sum())) + " personas"
        hombres=str(round((df['TP32_1_SEX'].sum()/df['TP27_PERSO'].sum())*100,1)) + "% hombres"
        mujeres=str(round((df['TP32_2_SEX'].sum()/df['TP27_PERSO'].sum())*100,1)) + "% mujeres"
        viviendas=str(round((df['TP9_1_USO'].sum()/df['TVIVIENDA'].sum())*100,1)) + "% de viviendas" 
        otros=str(round(100-(df['TP9_1_USO'].sum()/df['TVIVIENDA'].sum())*100,1)) + "% de otros usos" 
        
        e1=df['TP19_EE_E1'].sum()
        e2=df['TP19_EE_E2'].sum()
        e3=df['TP19_EE_E3'].sum()
        e4=df['TP19_EE_E4'].sum()
        e5=df['TP19_EE_E5'].sum()
        e6=df['TP19_EE_E6'].sum()
        est=pd.DataFrame(['Estrato 1', 'Estrato 2','Estrato 3','Estrato 4','Estrato 5','Estrato 6'])
        est['num']=[e1,e2,e3,e4,e5,e6]
        ind=est.num.idxmax()
        max_e=est[0][ind]
        estrato=max_e + " (" + str(round((est['num'][ind]/est['num'].sum())*100,1)) + "% de las viviendas)"
        con_int=str(round((df['TP19_INTE1'].sum()/df['TVIVIENDA'].sum())*100,1)) + "% de viviendas con internet"
        ed1=str(round((df['TP34_1_EDA'].sum()/df['TP27_PERSO'].sum())*100,1)) + "% de personas entre 0-9 años"
        ed2=str(round((df['TP34_2_EDA'].sum()/df['TP27_PERSO'].sum())*100,1)) + "% de personas entre 10-19 años"
        ed3=str(round((df['TP34_3_EDA'].sum()/df['TP27_PERSO'].sum())*100,1)) + "% de personas entre 20-29 años"
        ed4=str(round(((df['TP34_4_EDA'].sum()+df['TP34_5_EDA'].sum())/df['TP27_PERSO'].sum())*100,1)) + "% de personas entre 30-49 años"
        ed5=str(round(((df['TP34_6_EDA'].sum()+df['TP34_7_EDA'].sum())/df['TP27_PERSO'].sum())*100,1)) + "% de personas entre 50-69 años"
        ed6=str(round(((df['TP34_8_EDA'].sum()+df['TP34_9_EDA'].sum())/df['TP27_PERSO'].sum())*100,1)) + "% de personas con más de 70 años"
        
        edu1=str(round((df['TP51PRIMAR'].sum()/df['TP27_PERSO'].sum())*100,1)) + "% con nivel educativo primaria"
        edu2=str(round((df['TP51SECUND'].sum()/df['TP27_PERSO'].sum())*100,1)) + "% con nivel educativo secundaria"
        edu3=str(round((df['TP51SUPERI'].sum()/df['TP27_PERSO'].sum())*100,1)) + "% con nivel educativo universitario"
        edu4=str(round((df['TP51POSTGR'].sum()/df['TP27_PERSO'].sum())*100,1)) + "% con nivel educativo posgrado"
            
             
        
        return location, dl.Marker(position=e), probability2, prob_logit, dl.Circle(center=e, radius=300, color='#13c6e9'), personas, hombres, mujeres, estrato, otros, con_int, viviendas, ed1, ed2, ed3, ed4, ed5, ed6, edu1, edu2, edu3, edu4
    else:
        
            
        return "-", "-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-"

#Filter Comunas
@app.callback(
    [
        Output('main-map', 'children'),
        Output('graph-2', 'figure'),
        Output('graph-3', 'figure'), 
        Output('gauge', 'figure')
        
    ],
    [
        Input('drop-comunas', 'value'),
        Input('drop-zona', 'value'),
        
    ]
)
def update_mainmap_comuna(comuna, zonas):
    
    if (comuna=='total') & (len(zonas)==0) :
        lats=df["Latitud"] 
        lons=df["Longitud"]
        h_name=df['ZONAS VIBRA']
        y=(df['Latitud'].max()+df['Latitud'].min())/2
        x=(df['Longitud'].max()+df['Longitud'].min())/2
        fig3=go.Figure(go.Scattermapbox(
            lat=lats, 
            lon=lons, 
            marker=go.scattermapbox.Marker(
                size=6,
                color='#13c6e9',
                opacity=1),
            text=h_name,
            hoverinfo='text',
            name="Zonas Vibra")
                      )
        fig3.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 9.8,
                'center' : {"lat": y, "lon":x}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
        ) 
        fig3.update_layout(
            transition_duration=500,
            legend=dict(x=0,y=1,font=dict(size=15,color="white"),
            bgcolor='rgba(255, 255, 255, 0.5)',
                       )
        )
        fig3['layout'].update(
            margin=dict(l=0,r=0,b=0,t=0), 
            showlegend=True, 
            height=500)
        container_2=[
            html.H4('Localización', id='map_title' ),
            dcc.Graph(figure=fig3, id='var_censo'),
        ]
        
        df_last=df.iloc[: , -12:]
        df_last['Total']=df_last.iloc[: , -12:].sum(1)
        df_mes=df_last.sum(axis = 0, skipna = True).reset_index()
        df_mes = df_mes.rename(columns={'index': 'Mes', 0: 'Conexiones'})
        df_mes=df_mes[0:12]
        meses=df_mes['Mes']
        figa = px.line(df_mes, x="Mes", y="Conexiones", )
        figa.update_traces(line=dict(width=6, color='#13c6e9'))
        figa.add_scatter(x=df_mes['Mes'], y=df_mes['Conexiones'],marker_color='#13c6e9', marker_size=12)
        figa['layout'].update(margin=dict(l=0,r=0,b=0,t=0), showlegend=False, paper_bgcolor='rgba(0, 0, 0, 0)', height=220, font={'color':'#aaa'}, plot_bgcolor='rgba(0, 0, 0, 0)')
        figa.update_yaxes(title=None, )
        figa.update_xaxes(title=None, showgrid=False)
        figa.update_yaxes(tickfont=dict(size=8)),
        figa.update_layout(transition_duration=500)
        fig=figa
        figb = px.treemap(df_u, path=['USO'], values='PROMEDIO', color_discrete_sequence=px.colors.qualitative.G10, )
        figb.update_layout(margin = dict(t=0, l=0, r=0, b=0),paper_bgcolor='rgba(0, 0, 0, 0)', height=220 )
        figb.data[0].textinfo = 'label+text+value' 
        figb.layout.hovermode = False
        figb.update_layout(transition_duration=3000)
        fig2=figb
        fig4 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = len(df.index),
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Instaladas",  },
        gauge = {'axis': {'range': [None, total]}, 'bar': {'color': "#13c6e9"},}))
        fig4.update_layout(transition_duration=500)
        fig4['layout'].update(margin=dict(l=0,r=0,b=0,t=0),  paper_bgcolor='rgba(0, 0, 0, 0)', height=200, font={'color':'#aaa'} )
        figg=fig4
        
    elif (comuna!='total'):
        if comuna=='OTROS':
            zoom=9.8
        else:
            zoom=13
        df_2=df[df['COMUNA']==comuna]
        lats=df_2["Latitud"] 
        lons=df_2["Longitud"]
        h_name=df_2['ZONAS VIBRA']
        y=(df_2['Latitud'].max()+df_2['Latitud'].min())/2
        x=(df_2['Longitud'].max()+df_2['Longitud'].min())/2
        
        fig3=go.Figure(go.Scattermapbox(
            lat=lats, 
            lon=lons, 
            marker=go.scattermapbox.Marker(
                size=9,
                color='#13c6e9',
                opacity=1),
            text=h_name,
            hoverinfo='text',
            name="Zonas Vibra")
                      )
        fig3.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': zoom,
                'center' : {"lat": y, "lon":x}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
        ) 
        fig3.update_layout(
            transition_duration=500,
            legend=dict(x=0,y=1,font=dict(size=15,color="white"),
            bgcolor='rgba(255, 255, 255, 0.5)',
                       )
        )
        fig3['layout'].update(
            margin=dict(l=0,r=0,b=0,t=0), 
            showlegend=True, 
            height=500)
        container_2=[
            html.H4('Localización', id='map_title' ),
            dcc.Graph(figure=fig3, id='var_censo'),
        ]
        
        df_last=df_2.iloc[: , -12:]
        df_last['Total']=df_last.iloc[: , -12:].sum(1)
        df_last
        df_mes=df_last.sum(axis = 0, skipna = True).reset_index()
        df_mes = df_mes.rename(columns={'index': 'Mes', 0: 'Conexiones'})
        df_mes=df_mes[0:12]
        meses=df_mes['Mes']
        figa = px.line(df_mes, x="Mes", y="Conexiones", )
        figa.update_traces(line=dict(width=6, color='#13c6e9'))
        figa.add_scatter(x=df_mes['Mes'], y=df_mes['Conexiones'],marker_color='#13c6e9', marker_size=12)
        figa['layout'].update(margin=dict(l=0,r=0,b=0,t=0), showlegend=False, paper_bgcolor='rgba(0, 0, 0, 0)', height=220, font={'color':'#aaa'}, plot_bgcolor='rgba(0, 0, 0, 0)')
        figa.update_yaxes(title=None, )
        figa.update_xaxes(title=None, showgrid=False)
        figa.update_yaxes(tickfont=dict(size=8)),
        figa.update_layout(transition_duration=500)
        fig=figa
        figb = px.treemap(df_u, path=['USO'], values='PROMEDIO', color_discrete_sequence=px.colors.qualitative.G10, )
        figb.update_layout(margin = dict(t=0, l=0, r=0, b=0),paper_bgcolor='rgba(0, 0, 0, 0)', height=220 )
        figb.data[0].textinfo = 'label+text+value' 
        figb.layout.hovermode = False
        figb.update_layout(transition_duration=500)
        fig2=figb
        fig4 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = len(df_2.index),
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Instaladas",  },
        gauge = {'axis': {'range': [None, total]}, 'bar': {'color': "#13c6e9"},}))
        fig4.update_layout(transition_duration=500)
        fig4['layout'].update(margin=dict(l=0,r=0,b=0,t=0),  paper_bgcolor='rgba(0, 0, 0, 0)', height=200, font={'color':'#aaa'} )
        figg=fig4
    elif len(zonas)>0:
        
        df_filt=df.loc[df['ZONAS VIBRA'].isin(zonas)]
        lats=df_filt["Latitud"] 
        lons=df_filt["Longitud"]
        h_name=df_filt['ZONAS VIBRA']
        y=(df_filt['Latitud'].max()+df_filt['Latitud'].min())/2
        x=(df_filt['Longitud'].max()+df_filt['Longitud'].min())/2
        fig3=go.Figure(go.Scattermapbox(
            lat=lats, 
            lon=lons, 
            marker=go.scattermapbox.Marker(
                size=9,
                color='#13c6e9',
                opacity=1),
            text=h_name,
            hoverinfo='text',
            name="Zonas Vibra")
                          )
        fig3.update_layout(
            mapbox={
                    'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                    'zoom': 9.8,
                    'center' : {"lat": y, "lon":x}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
        fig3.update_layout(
            transition_duration=500,
            legend=dict(x=0,y=1,font=dict(size=15,color="white"),
            bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
        fig3['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500)
        container_2=[
                html.H4('Localización', id='map_title' ),
                dcc.Graph(figure=fig3, id='var_censo'),
            ]

        df_last=df_filt.iloc[: , -12:]
        df_last['Total']=df_last.iloc[: , -12:].sum(1)
        df_mes=df_last.sum(axis = 0, skipna = True).reset_index()
        df_mes = df_mes.rename(columns={'index': 'Mes', 0: 'Conexiones'})
        df_mes=df_mes[0:12]
        meses=df_mes['Mes']
        figa = px.line(df_mes, x="Mes", y="Conexiones", )
        figa.update_traces(line=dict(width=6, color='#13c6e9'))
        figa.add_scatter(x=df_mes['Mes'], y=df_mes['Conexiones'],marker_color='#13c6e9', marker_size=12)
        figa['layout'].update(margin=dict(l=0,r=0,b=0,t=0), showlegend=False, paper_bgcolor='rgba(0, 0, 0, 0)', height=220, font={'color':'#aaa'}, plot_bgcolor='rgba(0, 0, 0, 0)')
        figa.update_yaxes(title=None, )
        figa.update_xaxes(title=None, showgrid=False)
        figa.update_yaxes(tickfont=dict(size=8)),
        figa.update_layout(transition_duration=500)
        fig=figa
        figb = px.treemap(df_u, path=['USO'], values='PROMEDIO', color_discrete_sequence=px.colors.qualitative.G10, )
        figb.update_layout(margin = dict(t=0, l=0, r=0, b=0),paper_bgcolor='rgba(0, 0, 0, 0)', height=220 )
        figb.data[0].textinfo = 'label+text+value' 
        figb.layout.hovermode = False
        figb.update_layout(transition_duration=3000)
        fig2=figb
        fig4 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = len(df.index),
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Instaladas",  },
        gauge = {'axis': {'range': [None, total]}, 'bar': {'color': "#13c6e9"},}))
        fig4.update_layout(transition_duration=500)
        fig4['layout'].update(margin=dict(l=0,r=0,b=0,t=0),  paper_bgcolor='rgba(0, 0, 0, 0)', height=200, font={'color':'#aaa'} )
        figg=fig4

    return container_2, fig, fig2, figg
    
#update options zonas
@app.callback(
    [
        Output('drop-zona', 'options'),
        Output('drop-zona', 'value'),
        Output('drop-zona', 'clearable'),
        Output('drop-zona', 'multi'),
    ],
    Input('drop-comunas', 'value'),
)
def update_zonas(comuna):
    if comuna!='total':
        df_id=df[df['COMUNA']==comuna]['ZONAS VIBRA'].sort_values()
        options=[{'label': i, 'value':i} for i in df_id]
        value=''
        clearable=False
        multi=True
    else:
        df_id=df.iloc[:, 1]
        df_id=df_id.sort_values()
        options=[{'label': i, 'value':i} for i in df_id]
        value=''
        clearable=False
        multi=True
    return options, value, clearable, multi

#update demographic heatmap
@app.callback(
    [
        Output('main-map2', 'children'),
    ],
    [
        Input('type-variable', 'value'),
              
    ]
)
def update_mainmap_variable(variable):
    lats=df["Latitud"] 
    lons=df["Longitud"]
    h_name=df['ZONAS VIBRA']
    y=(df['Latitud'].max()+df['Latitud'].min())/2
    x=(df['Longitud'].max()+df['Longitud'].min())/2
    if variable=='NINGUNA':
        
        
        fig=go.Figure(go.Scattermapbox(
            lat=lats, 
            lon=lons, 
            marker=go.scattermapbox.Marker(
                size=6,
                color='#13c6e9',
                opacity=1),
            text=h_name,
            hoverinfo='text',
            name="Zonas Vibra")
                      )
        fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 9.8,
                'center' : {"lat": y, "lon":x}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
        ) 
        fig.update_layout(
            transition_duration=500,
            legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
            bgcolor='rgba(255, 255, 255, 0)',
                       )
        )
        fig['layout'].update(
            margin=dict(l=0,r=0,b=0,t=0), 
            showlegend=True, 
            height=500)
        container_2=[
            
            dcc.Graph(figure=fig, id='var_censo'),
        ]
        
    elif variable=='PORCENTAJE DE UNIDADES CON USO VIVIENDA':
 
            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_VIVIENDA",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_VIVIENDA': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0)'
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE UNIDADES CON USO DIFERENTE A VIVIENDA':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_OTROSUSOS",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_OTROSUSOS': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE VIVIENDAS CON ENERGÍA ELÉCTRICA':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_ENERGIA",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_ENERGIA': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)', 
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE VIVIENDAS EN ESTRATO 1':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_E1",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_E1': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE VIVIENDAS EN ESTRATO 2':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_E2",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_E2': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE VIVIENDAS EN ESTRATO 3':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_E3",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_E3': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE VIVIENDAS EN ESTRATO 4':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_E4",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_E4': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE VIVIENDAS EN ESTRATO 5':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_E5",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_E5': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE VIVIENDAS EN ESTRATO 6':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_E6",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_E6': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)', 
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE VIVIENDAS CON SERVICIO DE ACUEDUCTO':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_ACUE",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_ACUE': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE VIVIENDAS CON SERVICIO DE ALCANTARILLADO':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_ALC",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_ALC': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE VIVIENDAS CON SERVICIO DE GAS NATURAL':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_GAS",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_GAS': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE VIVIENDAS CON SERVICIO DE RECOLECCIÓN DE BASURAS':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_BAS",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_BAS': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE VIVIENDAS CON SERVICIO DE INTERNET':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_INTE",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_INTE': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='NÚMERO DE PERSONAS':
 
            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="TP27_PERSO",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'TP27_PERSO': 'Personas'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE HOMBRES':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_H",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_H': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE MUJERES':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_M",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_M': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE PERSONAS ENTRE 0 - 9 AÑOS':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_0_9",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_0_9': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE PERSONAS ENTRE 10 - 19 AÑOS':
 
            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_10_19",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_10_19': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE PERSONAS ENTRE 20 - 29 AÑOS':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_20_29",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_20_29': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE PERSONAS ENTRE 30 - 39 AÑOS':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_30_39",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_30_39': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE PERSONAS ENTRE 40 - 49 AÑOS':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_40_49",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_40_49': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE PERSONAS ENTRE 50 - 59 AÑOS':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_50_59",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_50_59': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE PERSONAS ENTRE 60 - 69 AÑOS':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_60_69",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_60_69': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE PERSONAS ENTRE 70 - 79 AÑOS':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_70_79",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_70_79': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORCENTAJE DE PERSONAS ENTRE 80 Y MÁS AÑOS':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_80",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_80': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORC. DE PERSONAS NIVEL EDUCATIVO PREESCOLAR Y BÁSICA PRIMARIA':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_PREE",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_PREE': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORC. DE PERSONAS NIVEL EDUCATIVO BÁSICA SECUNDARIA':
 
            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_SEC",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_SEC': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORC. DE PERSONAS NIVEL EDUCATIVO TÉCNICO A PROFESIONAL':
 
            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_0_TP",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_0_TP': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORC. DE PERSONAS NIVEL EDUCATIVO POSTGRADO':
 
            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_POST",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_POST': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="#FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]
    elif variable=='PORC. DE PERSONAS NIVEL EDUCATIVO NINGUNO':

            fig = px.choropleth_mapbox(ibague_mzn, geojson=ibague_mzn.geometry, 
                    locations=ibague_mzn.index, color="PORC_NIN",
                    height=600,
                   color_continuous_scale="RdYlGn",
                    labels={'PORC_NIN': '%'},
                     
                   )
            fig.add_scattermapbox( lat=lats, 
                                       lon=lons, 
                                       mode = 'markers', 
                                       hovertext=h_name, marker_size=6,
                                       marker_color='#13c6e9', hoverlabel={ }, name="Zonas Vibra")
            fig.update_layout(
            mapbox={
                'accesstoken':'pk.eyJ1IjoiY2FybG9zcnVpeiIsImEiOiJja3JrdzMwODkyNG9rMm5vMjMwamt0MTdoIn0.9aeH5Caw5g8GDmEEePpjow',
                'zoom': 11.5,
                'center' : {"lat": 4.435800, "lon": -75.199009}, 'style':'mapbox://styles/carlosruiz/ckry7q3tk08pi17pdhos24xsf'}
            ) 
            fig.update_layout(
                transition_duration=500,
                legend=dict(x=0,y=1,font=dict(size=15,color="FFFFFF"),
                bgcolor='rgba(255, 255, 255, 0.5)',
                           )
            )
            fig['layout'].update(
                margin=dict(l=0,r=0,b=0,t=0), 
                showlegend=True, 
                height=500),
            fig.update_layout( 
                  height=460,
                  mapbox_center = {"lat": 4.435800, "lon": -75.199009},
                  paper_bgcolor='rgb(233,233,233,0)', font={'color':'#aaa'})
            container_2=[

                dcc.Graph(figure=fig, id='var_censo'),
            ]

    return container_2
        
        
        
        
    


#Help principal
@app.callback(
    Output("modal", "is_open"),
    [Input("show-estad-modal", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, is_open):
    if n1 :
        return not is_open
    return is_open

#Help model1
@app.callback(
    Output("modal2", "is_open"),
    [Input("show-model1-modal", "n_clicks")],
    [State("modal2", "is_open")],
)
def toggle_modal(n1, is_open):
    if n1 :
        return not is_open
    return is_open

#Help model2
@app.callback(
    Output("modal3", "is_open"),
    [Input("show-model2-modal", "n_clicks")],
    [State("modal3", "is_open")],
)
def toggle_modal(n1, is_open):
    if n1 :
        return not is_open
    return is_open

#Help demographics
@app.callback(
    Output("modal4", "is_open"),
    [Input("show-demog-modal", "n_clicks")],
    [State("modal4", "is_open")],
)
def toggle_modal(n1, is_open):
    if n1 :
        return not is_open
    return is_open


@app.callback(
    Output("modal5", "is_open"),
    [Input('tabs_id', 'active_tab')],
    [State("modal5", "is_open")],
)
def toggle_modal(tab, is_open):
    if (tab=='modelo'):
        return not is_open
    return is_open

@app.callback(
    Output("modal6", "is_open"),
    [Input("show-demograf-modal", "n_clicks")],
    [State("modal6", "is_open")],
)
def toggle_modal(n1, is_open):
    if n1 :
        return not is_open
    return is_open

app.config.suppress_callback_exceptions = True

# Main
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8050")

import sys
import psycopg2
import pandas as pd
# Connection parameters, yours will be different
param_dic = {
    "host"      : "ibague.c0ccqdznpnus.us-east-2.rds.amazonaws.com",
    "database"  : "postgres",
    "user"      : "postgres",
    "password"  : "EUSjbUWLStCT"
}
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**param_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1) 
    print("Connection successful")
    return conn

db_con = connect()

def postgresql_to_dataframe(conn, select_query, column_names):
    """
    Tranform a SELECT query into a pandas dataframe
    """
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    
    # Naturally we get a list of tupples
    tupples = cursor.fetchall()
    cursor.close()
    
    # We just need to turn it into a pandas dataframe
    df = pd.DataFrame(tupples, columns = column_names)
    return df

def mapear_mes(x):
    if x == 1:
        return 'Ene '
    if x == 2:
        return 'Feb '
    if x == 3:
        return 'Mar '
    if x == 4:
        return 'Abr '
    if x == 5:
        return 'May '
    if x == 6:
        return 'Jun '
    if x == 7:
        return 'Jul '
    if x == 8:
        return 'Ago '
    if x == 9:
        return 'Sep ' 
    if x == 10:
        return 'Oct '
    if x == 11:
        return 'Nov '
    if x == 12:
        return 'Dic '


def get_conexiones():
    query = 'SELECT * FROM "Conexiones_Zonas"'
    columns = ['ID_CONEXION', 'ID', 'ZONAS VIBRA', 'CONEXIONES', 'FECHA']
    df = postgresql_to_dataframe(db_con, query, columns).drop('ID_CONEXION', axis = 1)
    pivot = df.pivot(index=['ID', 'ZONAS VIBRA'], columns=["FECHA"],values="CONEXIONES")
    
    temp = pd.DataFrame(index = range(len(pivot.columns)))
    temp['FECHA'] = pivot.columns
    temp['MES'] = pd.DatetimeIndex(temp['FECHA']).month
    temp['year'] = pd.DatetimeIndex(temp['FECHA']).year
    pivot.columns = temp['MES'].apply(mapear_mes) + temp['year'].astype(str)
    pivot['PROMEDIO'] = pivot.mean(axis = 1)
    return  pivot.reset_index()

def get_Usabilidad():
    query = 'SELECT * FROM "Usabilidad_Zonas"'
    columns = ['ID_USO', 'USO', 'PORCENTAJE', 'FECHA']
    df = postgresql_to_dataframe(db_con, query, columns).drop('ID_USO', axis = 1)
    pivot = df.pivot(index=['USO'], columns=["FECHA"],values="PORCENTAJE")
    
    temp = pd.DataFrame(index = range(len(pivot.columns)))
    temp['FECHA'] = pivot.columns
    temp['MES'] = pd.DatetimeIndex(temp['FECHA']).month
    temp['year'] = pd.DatetimeIndex(temp['FECHA']).year
    pivot.columns = temp['MES'].apply(mapear_mes) + temp['year'].astype(str)
    pivot['PROMEDIO'] = pivot.mean(axis = 1)
    return  pivot.reset_index()

def get_Variables_Censo():
    query = 'SELECT * FROM "Variables_Censo"'
    columns = ['VARIABLE', 'DESCRIPCIÓN', 'INCLUIR']
    return postgresql_to_dataframe(db_con, query, columns)

def get_Data_Zonas():
    query = 'SELECT * FROM "Data_Zonas"'
    columns = ['ID', 'ZONAS VIBRA', 'COMUNA', 'Latitud', 'Longitud', 'distmin', 'distmax', 'dist_zona1',
                'dist_zona2', 'dist_zona3', 'dist_zona4', 'dist_zona5', 'dist_zona6', 'dist_zona7', 'dist_zona8',
                'dist_zona9', 'dist_zona10', 'dist_zona11', 'dist_zona12', 'dist_zona13', 'dist_zona14', 'dist_zona15',
                'dist_zona16', 'dist_zona17', 'dist_zona18', 'dist_zona19', 'dist_zona20', 'dist_zona21', 'dist_zona22',
                'dist_zona23', 'dist_zona24', 'dist_zona25', 'dist_zona26', 'dist_zona27', 'dist_zona28', 'dist_zona29',
                'dist_zona30', 'dist_zona31', 'dist_zona32', 'dist_zona33', 'dist_zona34', 'dist_zona35', 'dist_zona36',
                'dist_zona37', 'dist_zona38', 'dist_zona39', 'dist_zona40', 'dist_zona41', 'dist_zona42', 'dist_zona43',
                'dist_zona44', 'dist_zona45', 'dist_zona46', 'dist_zona47', 'dist_zona48', 'dist_zona49', 'dist_zona50',
                'dist_zona51', 'dist_zona52', 'dist_zona53', 'dist_zona54', 'dist_zona55', 'dist_zona56', 'dist_zona57',
                'dist_zona58', 'dist_zona59', 'dist_zona60', 'dist_zona61', 'dist_zona62', 'dist_zona63', 'dist_zona64',
                'dist_zona65', 'dist_zona66', 'dist_zona67', 'dist_zona68', 'dist_zona69', 'dist_zona70', 'dist_zona71',
                'dist_zona72', 'dist_zona73', 'dist_zona74', 'dist_zona75', 'dist_zona76', 'dist_zona77', 'dist_zona78',
                'dist_zona79', 'dist_zona80', 'dist_zona81', 'dist_zona82', 'dist_zona83', 'dist_zona84', 'dist_zona85',
                'dist_zona86', 'dist_zona87', 'dist_zona88', 'dist_zona89', 'dist_zona90', 'dist_zona91', 'dist_zona92',
                'dist_zona93', 'dist_zona94', 'dist_zona95', 'dist_zona96', 'dist_zona97', 'dist_zona98', 'dist_zona99',
                'dist_zona100', 'dist_zona101', 'dist_zona102', 'dist_zona103', 'dist_zona104', 'dist_zona105',
                'dist_zona106', 'dist_zona107', 'dist_zona108', 'dist_zona109', 'dist_zona110', 'dist_zona111',
                'dist_zona112', 'dist_zona113', 'dist_zona114', 'dist_zona115', 'dist_zona116', 'dist_zona117',
                'dist_zona118', 'dist_zona119', 'dist_zona120', 'dist_zona121', 'dist_zona122', 'dist_zona123',
                'dist_zona124', 'dist_zona125', 'dist_zona126', 'dist_zona127', 'dist_zona128', 'dist_zona129',
                'dist_zona130', 'dist_zona131', 'dist_zona132', 'dist_zona133', 'dist_zona134', 'dist_zona135',
                'dist_zona136', 'dist_zona137', 'dist_zona138', 'dist_zona139', 'dist_zona140', 'dist_zona141',
                'dist_zona142', 'dist_zona143', 'dist_zona144', 'dist_zona145', 'dist_zona146', 'dist_zona147',
                'dist_zona148', 'dist_zona149', 'dist_zona150', 'CLAS_CCDGO', 'TP9_1_USO', 'TP9_2_USO', 'TP9_3_USO',
                'TP9_4_USO', 'TP9_2_1_MI', 'TP9_2_2_MI', 'TP9_2_3_MI', 'TP9_2_4_MI', 'TP9_2_9_MI', 'TP9_3_1_NO',
                'TP9_3_2_NO', 'TP9_3_3_NO', 'TP9_3_4_NO', 'TP9_3_5_NO', 'TP9_3_6_NO', 'TP9_3_7_NO', 'TP9_3_8_NO',
                'TP9_3_9_NO', 'TP9_3_10_N', 'TP9_3_99_N', 'PORC_VIVIENDA', 'PORC_OTROSUSOS', 'TUNIDADES', 'TVIVIENDA',
                'TP14_1_TIP', 'TP14_2_TIP', 'TP14_3_TIP', 'TP14_4_TIP', 'TP14_5_TIP', 'TP14_6_TIP', 'TP16_HOG', 'TP19_EE_1',
                'PORC_ENERGIA','TP19_EE_E1', 'TP19_EE_E2', 'TP19_EE_E3', 'TP19_EE_E4', 'TP19_EE_E5', 'TP19_EE_E6',
                'PORC_E1', 'PORC_E2', 'PORC_E3', 'PORC_E4', 'PORC_E5', 'PORC_E6', 'TP19_ACU_1', 'PORC_ACUE', 'PORC_ALC',
                'PORC_GAS', 'PORC_INTE', 'PORC_BAS', 'TP19_ALC_1', 'TP19_GAS_1', 'TP19_RECB1', 'TP19_INTE1', 'TP19_INTE2',
                'TP27_PERSO', 'TP32_1_SEX', 'TP32_2_SEX', 'PORC_H', 'PORC_M', 'TP34_1_EDA', 'TP34_2_EDA', 'TP34_3_EDA',
                'TP34_4_EDA', 'TP34_5_EDA', 'TP34_6_EDA', 'TP34_7_EDA', 'TP34_8_EDA', 'TP34_9_EDA', 'TP51PRIMAR', 
                'TP51SECUND', 'TP51SUPERI', 'TP51POSTGR', 'TP51_13_ED', 'TP51_99_ED', 'PORC_0_9', 'PORC_10_19',
                'PORC_20_29', 'PORC_30_39', 'PORC_40_49', 'PORC_50_59', 'PORC_60_69', 'PORC_70_79', 'PORC_80',
                'PORC_PREE', 'PORC_SEC', 'PORC_0_TP', 'PORC_POST', 'PORC_NIN', 'ene.-19', 'feb.-19', 'mar.-19',
                'abr.-19', 'may.-19', 'jun.-19', 'jul.-19', 'ago.-19', 'sep.-19', 'oct.-19', 'nov.-19', 'dic.-19',
                'dic.-20', 'feb.-21', 'mar.-21', 'abr.-21']
    return postgresql_to_dataframe(db_con, query, columns)

def get_Data_Manzanas():
    query = 'SELECT * FROM "Data_Manzanas"'
    columns = ['X', 'Y', 'COD_DANE_A', 'DPTO_CCDGO', 'MPIO_CCDGO', 'MPIO_CDPMP', 'CLAS_CCDGO', 'SETR_CCDGO', 'SETR_CCNCT',
               'SECR_CCDGO', 'SECR_CCNCT', 'ZU_CCDGO', 'ZU_CDIVI', 'SETU_CCDGO', 'SETU_CCNCT', 'SECU_CCDGO', 'SECU_CCNCT',
               'MANZ_CCDGO', 'AG_CCDGO', 'DATO_ANM', 'VERSION','AREA', 'LATITUD','LONGITUD', 'DENSIDAD', 'CTNENCUEST', 
               'TP3_1_SI', 'TP3_2_NO', 'TP3A_RI', 'TP3B_TCN','TP4_1_SI', 'TP4_2_NO', 'TP9_1_USO', 'TP9_2_USO', 'TP9_3_USO',
               'TP9_4_USO', 'TP9_2_1_MI','TP9_2_2_MI', 'TP9_2_3_MI', 'TP9_2_4_MI', 'TP9_2_9_MI', 'TP9_3_1_NO', 'TP9_3_2_NO',
               'TP9_3_3_NO', 'TP9_3_4_NO','TP9_3_5_NO', 'TP9_3_6_NO', 'TP9_3_7_NO', 'TP9_3_8_NO','TP9_3_9_NO', 'TP9_3_10_N',
               'TP9_3_99_N', 'TVIVIENDA', 'TP14_1_TIP', 'TP14_2_TIP','TP14_3_TIP', 'TP14_4_TIP', 'TP14_5_TIP', 'TP14_6_TIP',
               'TP15_1_OCU', 'TP15_2_OCU', 'TP15_3_OCU','TP15_4_OCU', 'TP16_HOG', 'TP19_EE_1', 'TP19_EE_2','TP19_EE_E1',
               'TP19_EE_E2', 'TP19_EE_E3', 'TP19_EE_E4','TP19_EE_E5', 'TP19_EE_E6', 'TP19_EE_E9','TP19_ACU_1', 'TP19_ACU_2',
               'TP19_ALC_1', 'TP19_ALC_2', 'TP19_GAS_1', 'TP19_GAS_2', 'TP19_GAS_9','TP19_RECB1', 'TP19_RECB2', 'TP19_INTE1',
               'TP19_INTE2', 'TP19_INTE9','TP27_PERSO', 'PERSONAS_L', 'PERSONAS_S', 'TP32_1_SEX','TP32_2_SEX', 'TP34_1_EDA',
               'TP34_2_EDA', 'TP34_3_EDA', 'TP34_4_EDA', 'TP34_5_EDA', 'TP34_6_EDA','TP34_7_EDA', 'TP34_8_EDA', 'TP34_9_EDA',
               'TP51PRIMAR', 'TP51SECUND', 'TP51SUPERI','TP51POSTGR', 'TP51_13_ED', 'TP51_99_ED', 'CD_LC_CM', 'NMB_LC_CM',
               'TP_LC_CM', 'Shape_Leng', 'Shape_Area', 'COD_RDTM','PORC_VIVIENDA', 'PORC_OTROSUSOS', 'PORC_ENERGIA', 'PORC_E1',
               'PORC_E2', 'PORC_E3', 'PORC_E4', 'PORC_E5', 'PORC_E6', 'PORC_ACUE','PORC_ALC', 'PORC_GAS', 'PORC_INTE',
               'PORC_BAS', 'PORC_H', 'PORC_M', 'PORC_0_9', 'PORC_10_19', 'PORC_20_29', 'PORC_30_39', 'PORC_40_49',
               'PORC_50_59', 'PORC_60_69', 'PORC_70_79', 'PORC_80', 'PORC_PREE', 'PORC_SEC', 'PORC_0_TP', 'PORC_POST','PORC_NIN']
    return postgresql_to_dataframe(db_con, query, columns)


def get_Ubicacion_Zonas():
    query = 'SELECT * FROM "Ubicacion_Zonas"'
    columns = ['ID', 'ZONAS VIBRA', 'DIRECCION', 'Latitud', 'Longitud', 'dist_zona1', 'dist_zona2', 'dist_zona3', 'dist_zona4',
               'dist_zona5', 'dist_zona6', 'dist_zona7', 'dist_zona8', 'dist_zona9', 'dist_zona10', 'dist_zona11', 
               'dist_zona12', 'dist_zona13', 'dist_zona14', 'dist_zona15', 'dist_zona16', 'dist_zona17', 'dist_zona18',
               'dist_zona19', 'dist_zona20', 'dist_zona21', 'dist_zona22', 'dist_zona23', 'dist_zona24', 'dist_zona25',
               'dist_zona26', 'dist_zona27', 'dist_zona28', 'dist_zona29', 'dist_zona30', 'dist_zona31', 'dist_zona32',
               'dist_zona33', 'dist_zona34', 'dist_zona35', 'dist_zona36', 'dist_zona37', 'dist_zona38', 'dist_zona39',
               'dist_zona40', 'dist_zona41', 'dist_zona42', 'dist_zona43', 'dist_zona44', 'dist_zona45', 'dist_zona46',
               'dist_zona47', 'dist_zona48', 'dist_zona49', 'dist_zona50', 'dist_zona51', 'dist_zona52', 'dist_zona53',
               'dist_zona54', 'dist_zona55', 'dist_zona56', 'dist_zona57', 'dist_zona58', 'dist_zona59', 'dist_zona60',
               'dist_zona61', 'dist_zona62', 'dist_zona63', 'dist_zona64', 'dist_zona65', 'dist_zona66', 'dist_zona67',
               'dist_zona68', 'dist_zona69', 'dist_zona70', 'dist_zona71', 'dist_zona72', 'dist_zona73', 'dist_zona74',
               'dist_zona75', 'dist_zona76', 'dist_zona77', 'dist_zona78', 'dist_zona79', 'dist_zona80', 'dist_zona81',
               'dist_zona82', 'dist_zona83', 'dist_zona84', 'dist_zona85', 'dist_zona86', 'dist_zona87', 'dist_zona88',
               'dist_zona89', 'dist_zona90', 'dist_zona91', 'dist_zona92', 'dist_zona93', 'dist_zona94', 'dist_zona95',
               'dist_zona96', 'dist_zona97', 'dist_zona98', 'dist_zona99', 'dist_zona100', 'dist_zona101', 'dist_zona102',
               'dist_zona103', 'dist_zona104', 'dist_zona105', 'dist_zona106', 'dist_zona107', 'dist_zona108', 'dist_zona109',
               'dist_zona110', 'dist_zona111', 'dist_zona112', 'dist_zona113', 'dist_zona114', 'dist_zona115', 'dist_zona116',
               'dist_zona117', 'dist_zona118', 'dist_zona119', 'dist_zona120', 'dist_zona121', 'dist_zona122', 'dist_zona123',
               'dist_zona124', 'dist_zona125', 'dist_zona126', 'dist_zona127', 'dist_zona128', 'dist_zona129', 'dist_zona130',
               'dist_zona131', 'dist_zona132', 'dist_zona133', 'dist_zona134', 'dist_zona135', 'dist_zona136', 'dist_zona137',
               'dist_zona138', 'dist_zona139', 'dist_zona140', 'dist_zona141', 'dist_zona142', 'dist_zona143', 'dist_zona144',
               'dist_zona145', 'dist_zona146', 'dist_zona147', 'dist_zona148', 'dist_zona149', 'dist_zona150']
    return postgresql_to_dataframe(db_con, query, columns)

def get_df_model():
    query = 'SELECT * FROM "Model"'
    columns = ['Unnamed: 0', 'far_dist', 'DENSIDAD', 'febrero', 'marzo','abril', 'TP19_EE_E2_pct', 'TP19_EE_E3_pct',
               'TP19_EE_E4_pct', 'TP19_EE_E5_pct', 'TP19_EE_E6_pct', 'TP34_2_EDA_pct', 'TP34_3_EDA_pct', 'TP34_4_EDA_pct',
               'TP34_5_EDA_pct', 'TP34_6_EDA_pct', 'TP34_7_EDA_pct', 'TP34_8_EDA_pct', 'TP34_9_EDA_pct', 'TP19_ALC_1_pct',
               'TP19_EE_1_pct', 'TP19_GAS_1_pct', 'TP19_INTE2_pct', 'geometry', 'LATITUD', 'LONGITUD', 'Intercept',
               'prob_logit', 'COD_DANE_A']
    return postgresql_to_dataframe(db_con, query, columns)

import pyodbc # CONECTOR PARA Sql Server
import pandas as pd
from datetime import datetime 
from Funciones.secundarias import fecha_actual, configuracion
import time
from tkinter import messagebox





# FUNCIÓN PARA VACIAR ARCHIVO
def eliminar_lineas(contador):
    ### OBTENER Y FORMATEAR HORA ACUTAL
    fecha_hora = fecha_actual()
    parametros = configuracion()
    try:
        with open(parametros["path"], 'r') as archivo:
            lineas = archivo.readlines()

        lineas = [lineas[0]] + lineas[contador :-1]

        with open(parametros["path"], 'w') as archivo:
            archivo.writelines(lineas)

        print(f"{fecha_hora}: Se han eliminado {contador} registros")
    except Exception as ex:
        print(f"{fecha_hora}: Error al eliminar líneas del archivo: {ex}")



# FUNCIÓN PARA CONECTAR CON BDD
def conectar_bdd():
    parametros = configuracion()
    # DATOS DE CONEXIÓN
    server = parametros["server"]
    db = parametros["bdd"]
    user = parametros["user"]
    password = parametros["password"]
    # CONECTAR A BASE DE DATOS
    vi_contador = 0
    v_conectado = "n"
    while vi_contador < 3:
        try:
            global cnn
            cnn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER='+server+';DATABASE='+db+';UID='+user+';PWD='+password
            )
            vi_contador = 10
            v_conectado = "s"
        except:
            vi_contador += 1
            v_conectado = "n"
    return v_conectado






# FUNCIÓN PRINCIPAL
def main(timer_runs, ruta_archivo):
    parametros = configuracion()
    fecha_hora = fecha_actual()
    print(f"{fecha_hora}: Ingresando datos..." )
    # INGRESAR DATOS
    while timer_runs.is_set():
        tiempo = parametros["tiempo"]
        v_conectado = conectar_bdd()
        if v_conectado == "s":
            ingresar_datos(ruta_archivo)

        time.sleep(int(tiempo))  # Segundos


#FUNCIÓN PARA INGRESAR DATOS
def ingresar_datos(ruta_archivo):
    fecha_hora = fecha_actual()

    try: 
        df = pd.read_csv(ruta_archivo, sep=";", parse_dates=["dd-MM-yyyy H:mm:ss"], dayfirst=True, encoding='unicode_escape').fillna('0')
    except Exception as ex:
        messagebox.showerror(message="Archivo erroneo o no vinculado, intente otra vez", title='ERROR')
        return
    
    try:
        # VALORES DECIMALES
        df['TEMP. SONDA'] = df['TEMP. SONDA'].str.replace(',', '.').astype(float)
        df['TEMP. SOBRE FIJA'] = df['TEMP. SOBRE FIJA'].str.replace(',', '.').astype(float)
        df['TEMP. BAJO TELA 1'] = df['TEMP. BAJO TELA 1'].str.replace(',', '.').astype(float)
        df['TEMP. BAJO TELA 2'] = df['TEMP. BAJO TELA 2'].str.replace(',', '.').astype(float)
        df['HUMEDAD SOBRE TELA EN HORNO'] = df['HUMEDAD SOBRE TELA EN HORNO'].str.replace(',', '.').astype(float)
        df['PRESION DIFERENCIAL HORNO'] = df['PRESION DIFERENCIAL HORNO'].str.replace(',', '.').astype(float)
        #### Contador de GAS
        df['CONTADOR DE GAS'] = df['CONTADOR DE GAS'].str.replace(',', '.').astype(float)
        df['CONTADOR DE GAS ETAPA 1'] = df['CONTADOR DE GAS ETAPA 1'].str.replace(',', '.').astype(float)
        df['CONTADOR DE GAS ETAPA 2'] = df['CONTADOR DE GAS ETAPA 2'].str.replace(',', '.').astype(float)
        df['CONTADOR DE GAS ETAPA 3'] = df['CONTADOR DE GAS ETAPA 3'].str.replace(',', '.').astype(float)
        df['CONTADOR DE GAS ETAPA 4'] = df['CONTADOR DE GAS ETAPA 4'].str.replace(',', '.').astype(float)
        df['CONTADOR DE GAS ETAPA 5'] = df['CONTADOR DE GAS ETAPA 5'].str.replace(',', '.').astype(float)
        df['CONTADOR DE GAS ETAPA 6'] = df['CONTADOR DE GAS ETAPA 6'].str.replace(',', '.').astype(float)
        ### Tiempo
        df['TIEMPO DE SECADO EN MIN'] = df['TIEMPO DE SECADO EN MIN'].str.replace(',', '.').astype(float)
        df['TIEMPO TRANSCURRIDO EN ETAPA 1'] = df['TIEMPO TRANSCURRIDO EN ETAPA 1'].str.replace(',', '.').astype(float)
        df['TIEMPO TRANSCURRIDO EN ETAPA 2'] = df['TIEMPO TRANSCURRIDO EN ETAPA 2'].str.replace(',', '.').astype(float)
        df['TIEMPO TRANSCURRIDO EN ETAPA 3'] = df['TIEMPO TRANSCURRIDO EN ETAPA 3'].str.replace(',', '.').astype(float)
        df['TIEMPO TRANSCURRIDO EN ETAPA 4'] = df['TIEMPO TRANSCURRIDO EN ETAPA 4'].str.replace(',', '.').astype(float)
        df['TIEMPO TRANSCURRIDO EN ETAPA 5'] = df['TIEMPO TRANSCURRIDO EN ETAPA 5'].str.replace(',', '.').astype(float)
        df['TIEMPO TRANSCURRIDO EN ETAPA 6'] = df['TIEMPO TRANSCURRIDO EN ETAPA 6'].str.replace(',', '.').astype(float)

        # VALORES INT/Numeric
        df['ETAPA DEL PROCESO DE HORNEADO'] = df['ETAPA DEL PROCESO DE HORNEADO'].str.replace(',', '.').astype(float) / 1
        df['POSICION MANUAL CELOCIAS'] = df['POSICION MANUAL CELOCIAS'].str.replace(',', '.').astype(float) / 1
        df['VALOR SALIDA 0-100% - CELOSIA'] = df['VALOR SALIDA 0-100% - CELOSIA'].str.replace(',', '.').astype(float) / 1
        df['SP TEMP ETAPA 1 EN HORNO'] = df['SP TEMP ETAPA 1 EN HORNO'].str.replace(',', '.').astype(float) / 1
        df['SP TEMP ETAPA 2 EN HORNO'] = df['SP TEMP ETAPA 2 EN HORNO'].str.replace(',', '.').astype(float) / 1
        df['SP TEMP ETAPA 3 EN HORNO'] = df['SP TEMP ETAPA 3 EN HORNO'].str.replace(',', '.').astype(float) / 1
        df['SP TEMP ETAPA 4 EN HORNO'] = df['SP TEMP ETAPA 4 EN HORNO'].str.replace(',', '.').astype(float) / 1
        df['SP TEMP ETAPA 5 EN HORNO'] = df['SP TEMP ETAPA 5 EN HORNO'].str.replace(',', '.').astype(float) / 1
        df['SP TEMP ETAPA 6 EN HORNO'] = df['SP TEMP ETAPA 6 EN HORNO'].str.replace(',', '.').astype(float) / 1
        #PASAR LOS VALORES A INT/Numeric
        df['ETAPA DEL PROCESO DE HORNEADO'] = df['ETAPA DEL PROCESO DE HORNEADO'].astype(int)
        df['POSICION MANUAL CELOCIAS'] = df['POSICION MANUAL CELOCIAS'].astype(int)
        df['VALOR SALIDA 0-100% - CELOSIA'] = df['VALOR SALIDA 0-100% - CELOSIA'].astype(int)
        df['SP TEMP ETAPA 1 EN HORNO'] = df['SP TEMP ETAPA 1 EN HORNO'].astype(int)
        df['SP TEMP ETAPA 2 EN HORNO'] = df['SP TEMP ETAPA 2 EN HORNO'].astype(int)
        df['SP TEMP ETAPA 3 EN HORNO'] = df['SP TEMP ETAPA 3 EN HORNO'].astype(int)
        df['SP TEMP ETAPA 4 EN HORNO'] = df['SP TEMP ETAPA 4 EN HORNO'].astype(int)
        df['SP TEMP ETAPA 5 EN HORNO'] = df['SP TEMP ETAPA 5 EN HORNO'].astype(int)
        df['SP TEMP ETAPA 6 EN HORNO'] = df['SP TEMP ETAPA 6 EN HORNO'].astype(int)

    except Exception as ex:
        print(f"{fecha_hora}: Ha ocurrido el siguiente error: {ex}")
        return 
    

    try:    
        # CURSOR PARA INGRESAR DATOS
        cursor_insert = cnn.cursor()
        ultimo = ultimo_registro()
    except:
        fecha_act = fecha_actual()
        print(f"{fecha_act}: Ups, algo salió mal")
        return


    # Contador de registros ingresados
    contador = 0
    try:
        ultimoRegistro = ultimo[0]
        if ultimoRegistro == None:
            ultimoRegistro = datetime.strptime("17/01/2018 10:05:00", '%d/%m/%Y %H:%M:%S')
        else:
            ultimoRegistro = datetime.strftime(ultimoRegistro, '%d/%m/%Y %H:%M:%S')
            ultimoRegistro = datetime.strptime(ultimoRegistro, '%d/%m/%Y %H:%M:%S')
    except Exception as ex:
        print(f"{fecha_hora}: Ups, algo salió mal...")
        return     


    try:
        # For PARA INTERAR .DAT
        for i, row in df.iterrows():   
            # Formateo de fecha
            campo_fecha = row['dd-MM-yyyy H:mm:ss']
            v_fecha = datetime.strftime(campo_fecha, '%d/%m/%Y %H:%M:%S')
            fecha = datetime.strptime(v_fecha, '%d/%m/%Y %H:%M:%S')
            
            
            if fecha != ultimoRegistro and fecha > ultimoRegistro:
                try:
                    # SENTENCIA SQL
                    sql = f'''INSERT INTO HornoMiagTCO (fecha, batch, variedad, etapaProceso, tSonda, tSobreFija, tBajoTela, tBajoTela2,
                                HRSobreTela, Celosia, valorSalidaCelosia, PresionDiferencial, GasTotal, GasEtapa1,
                                GasEtapa2, GasEtapa3, GasEtapa4, GasEtapa5, GasEtapa6, TiempoTotal, TiempoBarraE1,
                                TiempoBarraE2, TiempoBarraE3, TiempoBarraE4, TiempoBarraE5, TiempoBarraE6, SPTemp1,
                                SPTemp2, SPTemp3, SPTemp4, SPTemp5, SPTemp6)
                                VALUES ('{v_fecha}', '{row['Numero de Batch']}', '{row['Variedad']}', '{row['ETAPA DEL PROCESO DE HORNEADO']}',
                                    '{row['TEMP. SONDA']}','{row['TEMP. SOBRE FIJA']}', '{row['TEMP. BAJO TELA 1']}', '{row['TEMP. BAJO TELA 2']}',
                                    '{row['HUMEDAD SOBRE TELA EN HORNO']}', '{row['POSICION MANUAL CELOCIAS']}', '{row['VALOR SALIDA 0-100% - CELOSIA']}',
                                    '{row['PRESION DIFERENCIAL HORNO']}', '{row['CONTADOR DE GAS']}', '{row['CONTADOR DE GAS ETAPA 1']}', 
                                    '{row['CONTADOR DE GAS ETAPA 2']}', '{row['CONTADOR DE GAS ETAPA 3']}', '{row['CONTADOR DE GAS ETAPA 4']}',
                                    '{row['CONTADOR DE GAS ETAPA 5']}', '{row['CONTADOR DE GAS ETAPA 6']}', '{row['TIEMPO DE SECADO EN MIN']}',
                                    '{row['TIEMPO TRANSCURRIDO EN ETAPA 1']}', '{row['TIEMPO TRANSCURRIDO EN ETAPA 2']}', '{row['TIEMPO TRANSCURRIDO EN ETAPA 3']}',
                                    '{row['TIEMPO TRANSCURRIDO EN ETAPA 4']}', '{row['TIEMPO TRANSCURRIDO EN ETAPA 5']}', '{row['TIEMPO TRANSCURRIDO EN ETAPA 6']}',
                                    '{row['SP TEMP ETAPA 1 EN HORNO']}', '{row['SP TEMP ETAPA 2 EN HORNO']}', '{row['SP TEMP ETAPA 3 EN HORNO']}',
                                    '{row['SP TEMP ETAPA 4 EN HORNO']}', '{row['SP TEMP ETAPA 5 EN HORNO']}', '{row['SP TEMP ETAPA 6 EN HORNO']}')'''
                    cursor_insert.execute(sql)
                    contador += 1
                except:
                    print(f"{fecha_hora}: Error en fila \n {v_fecha} - {row['Numero de Batch']}")
        # Confirmación del ingreso
        cnn.commit()
        cursor_insert.close()
        cnn.close()
        print(f"{fecha_hora}: Se han ingresado: {contador} registros")
    except TypeError:
        messagebox.showerror(message="Error en archivo, Favor informar a Depto. TI", title='ERROR')
        return
    except:
        return

### FUNCIÓN PARA PARAR CERRAR CONEXION BDD
def cerrar_conexion():
    fecha_hora = fecha_actual()
    try:
        cnn.close()
        print(f"{fecha_hora}: La conexión se ha cerrado")
    except:
        print(f"{fecha_hora}: Conexión cerrada...")
        
        


### RECUPERAR ÚLTIMO REGISTRO BDD
def ultimo_registro():
    cursor = cnn.cursor()
    sql = "SELECT MAX(Fecha) FROM HornoMiagTCO"
    cursor.execute(sql)

    global registro_fecha
    registro_fecha = cursor.fetchone()

    cursor.close()
    ultima_fecha = []
    for i in registro_fecha:
        ultima_fecha.append(i)
    return ultima_fecha
    


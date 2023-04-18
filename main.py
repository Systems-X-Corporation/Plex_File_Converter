import PySimpleGUI as sg
import pandas as pd
import os
from datetime import date

sg.theme("LightGreen")
layout = [[sg.T("")], [sg.Text("No. Consecutivo:  "), sg.Input(default_text="001", key='-CONC-', enable_events=True)],
          [sg.T("")],
          [sg.Text("Archivo: "), sg.Input(readonly=True),
           sg.FileBrowse(button_text=". . .", key='-IN-')], [sg.T("")], [sg.Button("Convertir")]]

###Building Window
window = sg.Window('Banorte Payments by Systems-X', layout, size=(500, 180), element_justification='center')

today = date.today()
try:
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == '-CONC-' and values['-CONC-'] and (values['-CONC-'][-1] not in ('0123456789') or len(
                values['-CONC-']) > 3):
            window['-CONC-'].update(values['-CONC-'][:-1])
        elif event == "Convertir":
            if values['-IN-'].lower().endswith(('.csv')) == True:
                if values['-CONC-']:

                    df = pd.read_csv(values['-IN-'], dtype={'Cuenta Destino': float, 'Cuenta Origen': str, 'Descripcion': str})

                    df['Operacion'] = df['Operacion'].fillna(2)

                    df['Clave ID'] = df['Clave ID'].fillna('')

                    df['Cuenta Origen'] = df['Cuenta Origen'].fillna('')

                    df['Cuenta Destino'] = df['Cuenta Destino'].fillna(0)
                    df['Cuenta Destino'] = df['Cuenta Destino'].astype(float)
                    #df['Cuenta Destino'] = df['Cuenta Destino'].astype(int) #Transform to int to remove the .00

                    df['Importe'] = df['Importe'].fillna(0)
                    df['Importe'] = df['Importe'].replace(",", "", regex=True)
                    df['Importe'] = df['Importe'].astype(float)
                    df['Importe'] = (df['Importe']*100).astype(int)

                    df['Referencia'] = df['Referencia'].fillna('')

                    df['Descripcion'] = df['Descripcion'].fillna('')

                    df['Moneda Origen'] = df['Moneda Origen'].fillna('1')

                    df['Moneda Destino'] = df['Moneda Destino'].fillna('1')

                    df['RFC Ordenante'] = df['RFC Ordenante'].fillna('')

                    df['IVA'] = df['IVA'].fillna(0)
                    df['IVA'] = df['IVA'].replace(",", "", regex=True)
                    df['IVA'] = df['IVA'].astype(float)
                    df['IVA'] = (df['IVA'] * 100).astype(int)

                    df['Email Beneficiario'] = df['Email Beneficiario'].fillna('')

                    df['Fecha Aplicacion'] = df['Fecha Aplicacion'].fillna('')

                    df['Instruccion Pago'] = df['Instruccion Pago'].fillna('')

                    export_Payments = ''

                    for index, row in df.iterrows():
                        Operacion = str(row['Operacion']).rjust(2, '0')
                        Operacion = Operacion[:2]

                        Clave_ID = str(row['Clave ID']).ljust(13, ' ')
                        Clave_ID = Clave_ID[:13]

                        Cuenta_Origen = str(row['Cuenta Origen']).rjust(20, '0')
                        Cuenta_Origen = Cuenta_Origen[:20]

                        Cuenta_Destino = float(row['Cuenta Destino'])
                        #Cuenta_Destino = int(row['Cuenta Destino']) #Transform to int to remove the .00
                        Cuenta_Destino = str(Cuenta_Destino).rjust(20, '0')
                        Cuenta_Destino = Cuenta_Destino[:20]

                        Importe = str(row['Importe']).rjust(14, '0')
                        Importe = Importe[:14]

                        Referencia = str(row['Referencia']).rjust(10, '0')
                        Referencia = Referencia[:10]

                        Descripcion = str(row['Descripcion']).ljust(30, ' ')
                        Descripcion = Descripcion[:30]

                        Moneda_Origen = str(row['Moneda Origen']).ljust(1, '1')
                        Moneda_Origen = Moneda_Origen[:1]

                        Moneda_Destino = str(row['Moneda Destino']).ljust(1, '1')
                        Moneda_Destino = Moneda_Destino[:1]

                        RFC_Ordenante = str(row['RFC Ordenante']).ljust(13, ' ')
                        RFC_Ordenante = RFC_Ordenante[:13]

                        IVA = str(row['IVA']).rjust(14, '0')
                        IVA = IVA[:14]

                        Email_Beneficiario = str(row['Email Beneficiario']).ljust(39, ' ')
                        Email_Beneficiario = Email_Beneficiario[:39]

                        Fecha_Aplicacion = str(row['Fecha Aplicacion']).replace('/', '').ljust(8)
                        Fecha_Aplicacion = Fecha_Aplicacion[:8]

                        Instruccion_Pago = str(row['Instruccion Pago']).ljust(70, ' ')
                        Instruccion_Pago = Instruccion_Pago[:70]

                        export_Payments += Operacion + \
                                                Clave_ID + \
                                                Cuenta_Origen + \
                                                Cuenta_Destino + \
                                                Importe + \
                                                Referencia + \
                                                Descripcion + \
                                                Moneda_Origen + \
                                                Moneda_Destino + \
                                                RFC_Ordenante + \
                                                IVA + \
                                                Email_Beneficiario + \
                                                Fecha_Aplicacion + \
                                                Instruccion_Pago + '\n'
                        #print(Cuenta_Destino)

                    with open(os.path.join(os.path.expanduser('~'), 'Documents',
                                              'PP012345' + today.strftime("%Y%m%d") + values["-CONC-"] + '.txt'),
                             "w") as export_Txt:
                        export_Txt.write(export_Payments)

                    sg.Popup('Archivo creado con éxito', keep_on_top=True, modal=True)

                    path = os.path.expanduser('~/Documents')
                    path = os.path.realpath(path)
                    os.startfile(path)
                else:
                    sg.Popup('No se ingresó un No. Consecutivo', keep_on_top=True, modal=True)

            elif values["-IN-"] == "":
                sg.Popup('No se seleccionó un archivo', keep_on_top=True, modal=True)

            else:
                sg.Popup('Archivo inválido', keep_on_top=True, modal=True)
except BaseException as  e:
    sg.Popup('Ocurrió un error. Intente de nuevo. \n %s' %e, keep_on_top=True, modal=True)

window.close()

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
            if values["-IN-"].lower().endswith(('.csv')) == True:
                if values['-CONC-']:

                    df = pd.read_csv(values["-IN-"])

                    df['Operacion'] = df['Operacion'].fillna('')
                    df['Clave ID'] = df['Clave ID'].fillna('')
                    df['Cuenta Origen'] = df['Cuenta Origen'].fillna('')
                    df['Cuenta Destino'] = df['Cuenta Destino'].fillna('')
                    df['Importe'] = df['Importe'].fillna(0)
                    df['Importe'] = df['Importe'].replace(",", "", regex=True)
                    df['Importe'] = df['Importe'].astype(float)
                    df['Importe'] = (df['Importe'] * 100).astype(int)
                    df['Referencia'] = df['Referencia'].fillna('')
                    df['Descripcion'] = df['Descripcion'].fillna('')
                    df['Moneda Origen'] = df['Moneda Origen'].fillna('1')
                    df['Moneda Destino'] = df['Moneda Destino'].fillna('1')
                    df['RFC Ordenante'] = df['RFC Ordenante'].fillna('')
                    df['IVA'] = df['IVA'].fillna(0)
                    df['Email Beneficiario'] = df['Email Beneficiario'].fillna('')
                    df['Fecha Aplicacion'] = pd.to_datetime(df['Fecha Aplicacion'])
                    df['Fecha Aplicacion'] = df['Fecha Aplicacion'].dt.strftime('%d/%m/%Y').fillna('')
                    df['Instruccion Pago'] = df['Instruccion Pago'].fillna('')

                    export_Payments = ''

                    for index, row in df.iterrows():
                        export_Payments += str(row['Operacion']).rjust(2, '0') + \
                                           str(row['Clave ID']).ljust(13) + \
                                           str(row['Cuenta Origen']).rjust(20, '0') + \
                                           str(row['Cuenta Destino']).rjust(20, '0') + \
                                           str(row['Importe']).rjust(14, '0') + \
                                           str(row['Referencia']).rjust(10, '0') + \
                                           str(row['Descripcion']).ljust(30) + \
                                           str(row['Moneda Origen']).ljust(1, '1') + \
                                           str(row['Moneda Destino']).ljust(1, '1') + \
                                           str(row['RFC Ordenante']).ljust(13) + \
                                           str(row['IVA']).rjust(14, '0') + \
                                           str(row['Email Beneficiario']).ljust(39) + \
                                           str(row['Fecha Aplicacion']).replace('/', '').ljust(8) + \
                                           str(row['Instruccion Pago']).ljust(70) + '\n'

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
except Exception as e:
    sg.Popup('Ocurrió un error. Intente de nuevo.\n', keep_on_top=True, modal=True)
    print(e)

window.close()

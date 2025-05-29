# Este archivo de Python es para crear las funciones que van a generar los graficos como PNG

import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

df= pd.read_csv("dataset\liga_2023.csv")

superclasico = df[
    ((df['local_team'] == 'Boca Juniors') & (df['visitor_team'] == 'River Plate')) |
    ((df['local_team'] == 'River Plate') & (df['visitor_team'] == 'Boca Juniors'))
]

clasicoavellaneda = df[
    ((df['local_team'] == 'Racing Club') & (df['visitor_team'] == 'Independiente')) |
    ((df['local_team'] == 'Independiente') & (df['visitor_team'] == 'Racing'))
]

clasicozonasur = df[
    ((df['local_team'] == 'Banfield') & (df['visitor_team'] == 'Lanus')) |
    ((df['local_team'] == 'Lanus') & (df['visitor_team'] == 'Banfield'))
]

clasicorosario = df[
    ((df['local_team'] == 'Newells') & (df['visitor_team'] == 'Rosario Central')) |
    ((df['local_team'] == 'Rosario Central') & (df['visitor_team'] == 'Newells'))
]

def mostplayed_clasics():
    quantity_superclasico= len(superclasico)
    quantity_clasicoavellaneda= len(clasicoavellaneda)
    quantity_clasicozonasur= len(clasicozonasur)
    quantity_clasicorosario= len(clasicorosario)
    quantity= [quantity_superclasico,quantity_clasicoavellaneda,quantity_clasicozonasur,quantity_clasicorosario]
    plt.pie(quantity,colors=["#6699CC", "#99CC66", "#DD9966"])

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    imagen_mostplayed_clasics = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return imagen_mostplayed_clasics


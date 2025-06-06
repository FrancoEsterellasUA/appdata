# Este archivo de Python es para crear las funciones que van a generar los graficos como PNG

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
from matplotlib.ticker import MultipleLocator
from matplotlib.lines import Line2D


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

clasicos = pd.concat([superclasico, clasicoavellaneda, clasicorosario, clasicozonasur], ignore_index=True)

def mostplayed_clasics():
    quantity_superclasico= len(superclasico)
    quantity_clasicoavellaneda= len(clasicoavellaneda)
    quantity_clasicozonasur= len(clasicozonasur)
    quantity_clasicorosario= len(clasicorosario)
    quantity= [quantity_superclasico,quantity_clasicoavellaneda,quantity_clasicozonasur,quantity_clasicorosario]
    plt.pie(quantity,colors=["#6699CC", "#99CC66", "#DD9966","#E7DD54"],labels=["Superclasico","Clasico Avellaneda","Clasico de Zona Sur", "Clasico de Rosario"])

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    imagen_mostplayed_clasics = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return imagen_mostplayed_clasics

def frequencywins_local_or_visit():
    clasicos['ganador'] = clasicos.apply(
    lambda row: 'Local' if row['local_result'] > row['visitor_result']
    else 'Visitante' if row['visitor_result'] > row['local_result']
    else 'Empate',
    axis=1
    )
    frecuencias = clasicos['ganador'].value_counts()

    plt.figure(figsize=(8, 6))
    plt.bar(frecuencias.index, frecuencias.values, color=['blue', 'yellow', 'red'])

    plt.xlabel('Resultado')
    plt.ylabel('')
    plt.title('¿Quien gana más a menudo: el Local o el Visitante?')
    plt.xticks(rotation=0)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_frequencywins_local_or_visit = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return image_frequencywins_local_or_visit

def victoria_aculumativa_rosario():
    clasicos['match_result'] = clasicos.apply(lambda row: (
    'Newells' if row['local_team'] == 'Newells' and row['local_result'] > row['visitor_result']
    else 'Rosario Central' if row['visitor_team'] == 'Rosario Central' and row['visitor_result'] > row['local_result']
    else 'Empate'), axis=1)

    
    clasicos['anio'] = clasicos['date_name'].str.extract(r'(\d{4})').astype(int)

    conteo = clasicos['match_result'].groupby(clasicos['anio']).value_counts().unstack(fill_value=0)

    for col in ['Newells', 'Rosario Central']:
        if col not in conteo.columns:
            conteo[col] = 0

    conteo = conteo.sort_index()
    acumulado = conteo[['Newells', 'Rosario Central']].cumsum()

    def create_decade_colored_line(ax, x, y, colors, linewidth):
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        decade_starts = x[0] + (x - x[0]) // 10 * 10
        color_cycle = []
        color_map = {}

        for i, year in enumerate(x[:-1]):
            decade = (year - x[0]) // 5
            color_map[decade] = colors[decade % len(colors)]
            color_cycle.append(color_map[decade])

        lc = LineCollection(segments, colors=color_cycle, linewidth=linewidth)
        ax.add_collection(lc)

    x = acumulado.index.values
    y_rc = acumulado['Rosario Central'].values
    y_new = acumulado['Newells'].values

    plt.figure(figsize=(8, 5))
    plt.style.use("default")
    ax = plt.gca()

    create_decade_colored_line(ax, x, y_rc, colors=['blue', 'yellow'], linewidth=3.5)

    create_decade_colored_line(ax, x, y_new, colors=['black', 'red'], linewidth=3.0)

    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(0, max(y_rc.max(), y_new.max()) + 1)
    plt.title('Evolución Acumulada de Victorias: Rosario Central vs Newells')
    plt.xlabel('Año')
    plt.ylabel('Victorias Acumuladas')
    plt.gca().xaxis.set_major_locator(MultipleLocator(10))
    plt.grid(False)

    custom_lines = [
        Line2D([0], [0], color='blue', lw=3.5, label='Rosario Central (Azul/Amarillo)'),
        Line2D([0], [0], color='yellow', lw=3.5),
        Line2D([0], [0], color='red', lw=3.0, label='Newells (Rojo/Negro)'),
        Line2D([0], [0], color='black', lw=3.0),
    ]
    plt.legend(handles=custom_lines, loc="upper left")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_victoria_acumulada_rosario = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return image_victoria_acumulada_rosario 

def victoria_acumulada_super():
    clasicos['match_result'] = clasicos.apply(lambda row: (
    'River Plate' if row['local_team'] == 'River Plate' and row['local_result'] > row['visitor_result']
    else 'Boca Juniors' if row['visitor_team'] == 'Boca Juniors' and row['visitor_result'] > row['local_result']
    else 'Empate'), axis=1)

    clasicos['anio'] = clasicos['date_name'].str.extract(r'(\d{4})').astype(int)


    conteo = clasicos['match_result'].groupby(clasicos['anio']).value_counts().unstack(fill_value=0)


    for col in ['Boca Juniors', "River Plate"]:
        if col not in conteo.columns:
            conteo[col] = 0

    conteo = conteo.sort_index()
    acumulado = conteo[['Boca Juniors', 'River Plate']].cumsum()

    def create_decade_colored_line(ax, x, y, colors, linewidth):
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)


        decade_starts = x[0] + (x - x[0]) // 10 * 10
        color_cycle = []
        color_map = {}

        for i, year in enumerate(x[:-1]):
            decade = (year - x[0]) // 5
            color_map[decade] = colors[decade % len(colors)]
            color_cycle.append(color_map[decade])

        lc = LineCollection(segments, colors=color_cycle, linewidth=linewidth)
        ax.add_collection(lc)

    x = acumulado.index.values
    y_rc = acumulado['Boca Juniors'].values
    y_new = acumulado['River Plate'].values

    plt.figure(figsize=(8, 5))
    plt.style.use("default")
    ax = plt.gca()

    create_decade_colored_line(ax, x, y_rc, colors=['blue', 'yellow'], linewidth=3.5)


    create_decade_colored_line(ax, x, y_new, colors=["#fae1de", 'red'], linewidth=3.0)

    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(0, max(y_rc.max(), y_new.max()) + 1)
    plt.title('Evolución Acumulada de Victorias: Boca Juniors vs River Plate')
    plt.xlabel('Año')
    plt.ylabel('Victorias Acumuladas')
    plt.gca().xaxis.set_major_locator(MultipleLocator(10))
    plt.grid(False)

    
    custom_lines = [
        Line2D([0], [0], color='blue', lw=3.5, label='Boca Juniors '),
        Line2D([0], [0], color='yellow', lw=3.5),
        Line2D([0], [0], color='#fae1de', lw=3.0, label='River Plate '),
        Line2D([0], [0], color='red', lw=3.0),
    ]
    plt.legend(handles=custom_lines, loc="upper left")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_victoria_acumulada_super = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return image_victoria_acumulada_super

def victoria_acumulado_zonasur():
    clasicos['match_result'] = clasicos.apply(lambda row: (
    'Banfield' if row['local_team'] == 'Banfield' and row['local_result'] > row['visitor_result']
    else 'Lanus' if row['visitor_team'] == 'Lanus' and row['visitor_result'] > row['local_result']
    else 'Empate'), axis=1)
    
    clasicos['anio'] = clasicos['date_name'].str.extract(r'(\d{4})').astype(int)


    conteo = clasicos['match_result'].groupby(clasicos['anio']).value_counts().unstack(fill_value=0)


    for col in ['Lanus', 'Banfield']:
        if col not in conteo.columns:
            conteo[col] = 0

    conteo = conteo.sort_index()
    acumulado = conteo[['Lanus', 'Banfield']].cumsum()

    def create_decade_colored_line(ax, x, y, colors, linewidth):
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)


        decade_starts = x[0] + (x - x[0]) // 10 * 10
        color_cycle = []
        color_map = {}

        for i, year in enumerate(x[:-1]):
            decade = (year - x[0]) // 5
            color_map[decade] = colors[decade % len(colors)]
            color_cycle.append(color_map[decade])

        lc = LineCollection(segments, colors=color_cycle, linewidth=linewidth)
        ax.add_collection(lc)


    x = acumulado.index.values
    y_rc = acumulado['Lanus'].values
    y_new = acumulado['Banfield'].values

    
    plt.figure(figsize=(8, 5))
    plt.style.use("default")
    ax = plt.gca()

    
    create_decade_colored_line(ax, x, y_rc, colors=['maroon', 'maroon'], linewidth=3.5)


    create_decade_colored_line(ax, x, y_new, colors=['green', '#8cffb1'], linewidth=3.0)

    
    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(0, max(y_rc.max(), y_new.max()) + 1)
    plt.title('Evolución Acumulada de Victorias: Lanus vs Banfield')
    plt.xlabel('Año')
    plt.ylabel('Victorias Acumuladas')
    plt.gca().xaxis.set_major_locator(MultipleLocator(10))
    plt.grid(False)

    
    custom_lines = [
        Line2D([0], [0], color='maroon', lw=3.5, label='Lanus'),

        Line2D([0], [0], color='green', lw=3.0, label='Banfield'),
        Line2D([0], [0], color='#8cffb1', lw=3.0),
    ]
    plt.legend(handles=custom_lines, loc="upper left")
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_victoria_acumulada_zonasur = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return image_victoria_acumulada_zonasur

def victoria_acumulada_avellaneda():
    clasicos['match_result'] = clasicos.apply(lambda row: (
    'Racing Club' if row['local_team'] == 'Racing Club' and row['local_result'] > row['visitor_result']
    else 'Independiente' if row['visitor_team'] == 'Independiente' and row['visitor_result'] > row['local_result']
    else 'Empate'), axis=1)

    clasicos['anio'] = clasicos['date_name'].str.extract(r'(\d{4})').astype(int)


    conteo = clasicos['match_result'].groupby(clasicos['anio']).value_counts().unstack(fill_value=0)


    for col in ['Independiente', "Racing Club"]:
        if col not in conteo.columns:
            conteo[col] = 0

    conteo = conteo.sort_index()
    acumulado = conteo[['Independiente', 'Racing Club']].cumsum()

    def create_decade_colored_line(ax, x, y, colors, linewidth):
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)


        decade_starts = x[0] + (x - x[0]) // 10 * 10
        color_cycle = []
        color_map = {}

        for i, year in enumerate(x[:-1]):
            decade = (year - x[0]) // 5
            color_map[decade] = colors[decade % len(colors)]
            color_cycle.append(color_map[decade])

        lc = LineCollection(segments, colors=color_cycle, linewidth=linewidth)
        ax.add_collection(lc)


    x = acumulado.index.values
    y_rc = acumulado['Independiente'].values
    y_new = acumulado['Racing Club'].values

    
    plt.figure(figsize=(8, 5))
    plt.style.use("default")
    ax = plt.gca()

    
    create_decade_colored_line(ax, x, y_rc, colors=['red', 'red'], linewidth=3.5)


    create_decade_colored_line(ax, x, y_new, colors=["#20bcfa", 'lightblue'], linewidth=3.0)

    
    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(0, max(y_rc.max(), y_new.max()) + 1)
    plt.title('Evolución Acumulada de Victorias: Independiente vs Racing Club')
    plt.xlabel('Año')
    plt.ylabel('Victorias Acumuladas')
    plt.gca().xaxis.set_major_locator(MultipleLocator(10))
    plt.grid(False)

    
    custom_lines = [
        Line2D([0], [0], color='red', lw=3.5, label='Independiente'),

        Line2D([0], [0], color='#20bcfa', lw=3.0, label='Racing Club'),
        Line2D([0], [0], color='lightblue', lw=3.0),
    ]
    plt.legend(handles=custom_lines, loc="upper left")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_victoria_acumulada_avellaneda = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return image_victoria_acumulada_avellaneda
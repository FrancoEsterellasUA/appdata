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
from sklearn.linear_model import LinearRegression



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

def victoria_acumulativa_rosario():
    clasicorosario['match_result'] = clasicorosario.apply(
    lambda row: row['local_team'] if row['local_result'] > row['visitor_result']
    else row['visitor_team'] if row['visitor_result'] > row['local_result']
    else 'Empate',
    axis=1
    )

    
    clasicorosario['anio'] = clasicorosario['date_name'].str.extract(r'(\d{4})').astype(int)
    conteo = clasicorosario.groupby(['anio', 'match_result']).size().unstack(fill_value=0)


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
    superclasico['match_result'] = superclasico.apply(
    lambda row: (
        row['local_team'] if row['local_result'] > row['visitor_result']
        else row['visitor_team'] if row['visitor_result'] > row['local_result']
        else 'Empate'
    ),
    axis=1
    )

    superclasico['anio'] = superclasico['date_name'].str.extract(r'(\d{4})').astype(int)
    conteo = superclasico.groupby(['anio', 'match_result']).size().unstack(fill_value=0)


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
    clasicozonasur['match_result'] = clasicozonasur.apply(
    lambda row: row['local_team'] if row['local_result'] > row['visitor_result']
    else row['visitor_team'] if row['visitor_result'] > row['local_result']
    else 'Empate',
    axis=1
    )
    
    clasicozonasur['anio'] = clasicozonasur['date_name'].str.extract(r'(\d{4})').astype(int)
    conteo = clasicozonasur.groupby(['anio', 'match_result']).size().unstack(fill_value=0)




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
    clasicoavellaneda['match_result'] = clasicoavellaneda.apply(
    lambda row: row['local_team'] if row['local_result'] > row['visitor_result']
    else row['visitor_team'] if row['visitor_result'] > row['local_result']
    else 'Empate',
    axis=1
    )

    clasicoavellaneda['anio'] = clasicoavellaneda['date_name'].str.extract(r'(\d{4})').astype(int)
    conteo = clasicoavellaneda.groupby(['anio', 'match_result']).size().unstack(fill_value=0)



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

# _____________________________

def entrenar_modelo(df, nombre_equipo):
    X = df['year'].values.reshape(-1, 1)
    y = df['wins'].values

    modelo = LinearRegression()
    modelo.fit(X, y)

    print(f"\n--- {nombre_equipo} ---")
    print("Pendiente:", modelo.coef_[0])
    print("Intercepción:", modelo.intercept_)

    return modelo

def regresion_linear_superclasico():
    superclasico['year'] = superclasico['date_name'].str.extract('(\d{4})').astype(int)

    superclasico['winner'] = superclasico.apply(lambda row: (
        row['local_team'] if row['local_result'] > row['visitor_result']
        else row['visitor_team'] if row['visitor_result'] > row['local_result']
        else 'Empate'), axis=1)

    equipos = ['Boca Juniors', 'River Plate']
    df_cumuls = {}

    for equipo in equipos:
        df_eq = superclasico[superclasico['winner'] == equipo]
        victorias_anuales = df_eq.groupby('year').size().reindex(range(2000, 2025), fill_value=0).reset_index()
        victorias_anuales.columns = ['year', 'wins']
        victorias_anuales['wins_cum'] = victorias_anuales['wins'].cumsum()

        modelo = LinearRegression()
        X = victorias_anuales['year'].values.reshape(-1, 1)
        y = victorias_anuales['wins_cum'].values
        modelo.fit(X, y)

        anios_futuros = np.arange(2025, 2041).reshape(-1, 1)
        pred_futuro = modelo.predict(anios_futuros)

        x_total = np.concatenate([victorias_anuales['year'], anios_futuros.flatten()])
        y_total = np.concatenate([victorias_anuales['wins_cum'], pred_futuro])

        df_cumuls[equipo] = (x_total, y_total)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(*df_cumuls['Boca Juniors'], label='Boca Juniors', color='blue')
    plt.plot(*df_cumuls['River Plate'], label='River Plate', color='red')
    plt.axvline(x=2024, color='gray', linestyle='--', label='Fin datos reales')
    plt.title('Victorias Boca vs River : prediccion con Regresion Lineal')
    plt.xlabel('Año')
    plt.ylabel('Victorias Acumuladas')
    plt.legend()
    plt.grid(False)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_regresion_lineal_super = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return image_regresion_lineal_super


def regresion_linear_avellaneda():
    clasicos['match_result'] = clasicos.apply(lambda row: (
    'Racing Club' if row['local_team'] == 'Racing Club' and row['local_result'] > row['visitor_result']
    else 'Independiente' if row['visitor_team'] == 'Independiente' and row['visitor_result'] > row['local_result']
    else 'Empate'), axis=1)
    
    clasicoavellaneda['year'] = clasicoavellaneda['date_name'].str.extract('(\d{4})').astype(int)
    clasicoavellaneda['winner'] = clasicoavellaneda.apply(lambda row: (
    'Racing Club' if row['local_team'] == 'Racing Club' and row['local_result'] > row['visitor_result']
    else 'Independiente' if row['visitor_team'] == 'Independiente' and row['visitor_result'] > row['local_result']
    else 'Empate'
    ), axis=1)
    victorias = clasicoavellaneda[clasicoavellaneda['winner'].isin(['Independiente', 'Racing Club'])]
    ganados_por_anio = victorias.groupby(['year', 'winner']).size().reset_index(name='wins')

    independiente_df = ganados_por_anio[ganados_por_anio['winner'] == 'Independiente'][['year', 'wins']]
    racing_df = ganados_por_anio[ganados_por_anio['winner'] == 'Racing Club'][['year', 'wins']]

    modelo_independiente = entrenar_modelo(independiente_df,"Independiente")
    modelo_racing = entrenar_modelo(racing_df, "Racing Club")

    anios_futuros = np.array([2025, 2026, 2027, 2030, 2035, 2040,2050,2055,2060]).reshape(-1, 1)

    pred_independiente = modelo_independiente.predict(anios_futuros)
    pred_racing = modelo_racing.predict(anios_futuros)

    def obtener_victorias_acumuladas(df, equipo, anio_final=2060):
        df_eq = df[df['winner'] == equipo].sort_values('year')
        X = df_eq['year'].values.reshape(-1, 1)
        y = df_eq['wins'].values

        modelo = LinearRegression()
        modelo.fit(X, y)

        anios_futuros = np.arange(df_eq['year'].max() + 1, anio_final + 1).reshape(-1, 1)
        pred = np.clip(modelo.predict(anios_futuros), 0, None)

        df_eq['wins_cumul'] = df_eq['wins'].cumsum()
        ultimo_total_real = df_eq['wins_cumul'].iloc[-1]
        pred_cumul = np.cumsum(pred) + ultimo_total_real

        anios_totales = np.concatenate([df_eq['year'].values, anios_futuros.flatten()])
        victorias_totales = np.concatenate([df_eq['wins_cumul'].values, pred_cumul])
        return anios_totales, victorias_totales, df_eq['year'].max()
    independiente_x, independiente_y, anio_corte_independiente = obtener_victorias_acumuladas(ganados_por_anio, 'Independiente')
    racing_x, racing_y, anio_corte_racing = obtener_victorias_acumuladas(ganados_por_anio, 'Racing Club')


    plt.plot(independiente_x, independiente_y,  color='red', label='Independiente')
    plt.plot(racing_x, racing_y,  color='lightblue', label='Racing Club')


    plt.axvline(x=anio_corte_independiente, color='gray', linestyle='--', label='Fin datos reales')


    plt.xticks(np.arange(min(independiente_x.min(), racing_x.min()), 2060,5))
    plt.xlim(2000, 2060)
    plt.ylim(20, 85)
    plt.title('Victorias Independiente vs Racing : prediccion con Regresion Lineal')
    plt.xlabel('Año')
    plt.ylabel('Victorias acumuladas')
    plt.legend()
    plt.grid(False)
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_regresion_lineal_avellaneda = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return image_regresion_lineal_avellaneda

def regresion_linear_zonasur():
    clasicos['match_result'] = clasicos.apply(lambda row: (
        'Banfield' if row['local_team'] == 'Banfield' and row['local_result'] > row['visitor_result']
        else 'Lanus' if row['visitor_team'] == 'Lanus' and row['visitor_result'] > row['local_result']
        else 'Empate'), axis=1)

    clasicozonasur['year'] = clasicozonasur['date_name'].str.extract('(\d{4})').astype(int)
    clasicozonasur['winner'] = clasicozonasur.apply(lambda row: (
        'Banfield' if row['local_team'] == 'Banfield' and row['local_result'] > row['visitor_result']
        else 'Lanus' if row['visitor_team'] == 'Lanus' and row['visitor_result'] > row['local_result']
        else 'Empate'), axis=1)

    victorias = clasicozonasur[clasicozonasur['winner'].isin(['Lanus', 'Banfield'])]
    ganados_por_anio = victorias.groupby(['year', 'winner']).size().reset_index(name='wins')

    lanus_df = ganados_por_anio[ganados_por_anio['winner'] == 'Lanus'][['year', 'wins']].sort_values('year')
    banfield_df = ganados_por_anio[ganados_por_anio['winner'] == 'Banfield'][['year', 'wins']].sort_values('year')

    modelo_lanus = entrenar_modelo(lanus_df, "Lanus")
    modelo_banfield = entrenar_modelo(banfield_df, "Banfield")

    anios_futuros = np.array([2025, 2026, 2027, 2030, 2035, 2040, 2050, 2055, 2060]).reshape(-1, 1)

    pred_lanus = modelo_lanus.predict(anios_futuros)
    pred_banfield = modelo_banfield.predict(anios_futuros)

    def obtener_victorias_acumuladas(df, equipo, anio_final=2060):
        df_eq = df[df['winner'] == equipo].sort_values('year')
        X = df_eq['year'].values.reshape(-1, 1)
        y = df_eq['wins'].values

        modelo = LinearRegression()
        modelo.fit(X, y)

        anios_futuros = np.arange(df_eq['year'].max() + 1, anio_final + 1).reshape(-1, 1)
        pred = np.clip(modelo.predict(anios_futuros), 0, None)

        df_eq['wins_cumul'] = df_eq['wins'].cumsum()
        ultimo_total_real = df_eq['wins_cumul'].iloc[-1]
        pred_cumul = np.cumsum(pred) + ultimo_total_real

        anios_totales = np.concatenate([df_eq['year'].values, anios_futuros.flatten()])
        victorias_totales = np.concatenate([df_eq['wins_cumul'].values, pred_cumul])
        return anios_totales, victorias_totales, df_eq['year'].max()

    lanus_x, lanus_y, anio_corte_lanus = obtener_victorias_acumuladas(ganados_por_anio, 'Lanus')
    banfield_x, banfield_y, anio_corte_banfield = obtener_victorias_acumuladas(ganados_por_anio, 'Banfield')

    plt.plot(lanus_x, lanus_y, color='maroon', label='Lanus')
    plt.plot(banfield_x, banfield_y, color='lightgreen', label='Banfield')

    plt.axvline(x=anio_corte_lanus, color='gray', linestyle='--', label='Fin datos reales')

    plt.xticks(np.arange(min(lanus_x.min(), banfield_x.min()), 2060, 5))
    plt.xlim(2000, 2060)
    plt.ylim(5, 80)
    plt.title('Victorias Lanus vs Banfield : prediccion con Regresion Lineal')
    plt.xlabel('Año')
    plt.ylabel('Victorias acumuladas')
    plt.legend()
    plt.grid(False)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_regresion_lineal_zonasur = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return image_regresion_lineal_zonasur

    
def regresion_linear_rosario():
    clasicorosario['year'] = clasicorosario['date_name'].str.extract('(\d{4})').astype(int)
    clasicorosario['winner'] = clasicorosario.apply(lambda row: (
        row['local_team'] if row['local_result'] > row['visitor_result']
        else row['visitor_team'] if row['visitor_result'] > row['local_result']
        else 'Empate'), axis=1)

    equipos = ['Newells', 'Rosario Central']
    df_cumuls = {}

    for equipo in equipos:
        df_eq = clasicorosario[clasicorosario['winner'] == equipo]
        victorias_anuales = df_eq.groupby('year').size().reindex(range(1960, 2025), fill_value=0).reset_index()
        victorias_anuales.columns = ['year', 'wins']
        victorias_anuales['wins_cum'] = victorias_anuales['wins'].cumsum()

        modelo = LinearRegression()
        X = victorias_anuales['year'].values.reshape(-1, 1)
        y = victorias_anuales['wins_cum'].values
        modelo.fit(X, y)

        anios_futuros = np.arange(2025, 2061).reshape(-1, 1)
        pred_futuro = modelo.predict(anios_futuros)

        x_total = np.concatenate([victorias_anuales['year'], anios_futuros.flatten()])
        y_total = np.concatenate([victorias_anuales['wins_cum'], pred_futuro])

        df_cumuls[equipo] = (x_total, y_total)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(*df_cumuls['Newells'], label='Newells', color='black')
    plt.plot(*df_cumuls['Rosario Central'], label='Rosario Central', color='gold')
    plt.axvline(x=2024, color='gray', linestyle='--', label='Fin datos reales')
    plt.title('Regresión Lineal sobre Victorias Acumuladas')
    plt.xlabel('Año')
    plt.ylabel('Victorias Acumuladas')
    plt.legend()
    plt.grid(False)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_regresion_lineal_rosario = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return image_regresion_lineal_rosario

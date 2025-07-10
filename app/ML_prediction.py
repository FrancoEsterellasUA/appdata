from plots import df
import pandas as pd
from sklearn.linear_model import LogisticRegression

superclasico = df[
    ((df['local_team'] == 'Boca Juniors') & (df['visitor_team'] == 'River Plate')) |
    ((df['local_team'] == 'River Plate') & (df['visitor_team'] == 'Boca Juniors'))
]
clasicoavellaneda = df[
    ((df['local_team'] == 'Racing Club') & (df['visitor_team'] == 'Independiente')) |
    ((df['local_team'] == 'Independiente') & (df['visitor_team'] == 'Racing Club'))
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

clasicos['year'] = clasicos['date_name'].str.extract('(\d+)', expand=False)
clasicos['year'] = clasicos['year'].apply(
    lambda x: x[:-1] + '0' if x else ''
)
clasicos['year'].value_counts()
ml_clasicos= clasicos
if 'visitor_team_id' in clasicos.columns or 'local_team_id' in clasicos.columns:
    ml_clasicos = clasicos.drop(columns=['local_team_id', 'visitor_team_id'])
ml_clasicos['gana_local'] = ml_clasicos['local_result'] > ml_clasicos['visitor_result']
ml_clasicos['gana_local'] = ml_clasicos['gana_local'].astype(int)
# ml_clasicos.sample()




dummies = pd.get_dummies(ml_clasicos['local_team'])
X = ml_clasicos[['local_team', 'local_result', 'year']]
X = pd.concat([dummies, ml_clasicos[['local_result', 'year']]], axis=1)
y= ml_clasicos['gana_local']


modelo = LogisticRegression()
modelo.fit(X, y)

#nuevo_sample = pd.DataFrame([{'Boca Juniors': False,'River Plate': True, 'local_result': 1, 'year':1990}])


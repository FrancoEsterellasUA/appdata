from plots import df
import pandas as pd
from sklearn.linear_model import LogisticRegression

superclasico = df[
    ((df['local_team'] == 'Boca Juniors') & (df['visitor_team'] == 'River Plate')) |
    ((df['local_team'] == 'River Plate') & (df['visitor_team'] == 'Boca Juniors'))
]

superclasico['year'] = superclasico['date_name'].str.extract('(\d+)', expand=False)
superclasico['year'] = superclasico['year'].apply(
    lambda x: x[:-1] + '0' if x else ''
)
superclasico['year'].value_counts()
ml_superclasico= superclasico
if 'visitor_team_id' in superclasico.columns or 'local_team_id' in superclasico.columns:
    ml_superclasico = superclasico.drop(columns=['local_team_id', 'visitor_team_id'])
ml_superclasico['gana_local'] = ml_superclasico['local_result'] > ml_superclasico['visitor_result']
ml_superclasico['gana_local'] = ml_superclasico['gana_local'].astype(int)
# ml_superclasico.sample()




dummies = pd.get_dummies(ml_superclasico['local_team'])
X = ml_superclasico[['local_team', 'local_result', 'year']]
X = pd.concat([dummies, ml_superclasico[['local_result', 'year']]], axis=1)
y= ml_superclasico['gana_local']


modelo = LogisticRegression()
modelo.fit(X, y)

#nuevo_sample = pd.DataFrame([{'Boca Juniors': False,'River Plate': True, 'local_result': 1, 'year':1990}])


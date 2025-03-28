import pathlib as pl

import numpy as np
import pandas as pd

data = pl.Path(__file__).parent.absolute() / 'data'
associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')

id = 2

evenements = evenements_df[evenements_df['association_id'] == id]

print(evenements.to_json())

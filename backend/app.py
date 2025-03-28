import pathlib as pl

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / 'data'

# Charger les données CSV
associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')

## Vous devez ajouter les routes ici : 
@app.route('/api/alive', methods=['GET'])
def api_alise():
    return jsonify({"message": "Alive"}), 200

@app.route('/api/associations', methods=['GET'])
def api_associations():
    liste = associations_df['nom'].values.tolist()
    return jsonify(liste), 200

@app.route('/api/association/<int:id>', methods=['GET'])
def api_detail_association():
    if id in associations_df['id'].values :
        detail = associations_df.set_index('id').loc[id,'description']
        return jsonify(detail), 200
    else :
        return jsonify({ "error": "Association not found" }), 404


if __name__ == '__main__':
    app.run(debug=False)




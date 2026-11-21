"""
Builds the course dataset `force_wells.csv.gz` from the FORCE 2020 lithology competition data.

Source: Bormann P., Aursand P., Dilib F., Manral S., Dischington P. (2020).
FORCE 2020 Well well log and lithofacies dataset for machine learning competition.
Zenodo. https://doi.org/10.5281/zenodo.4351156
Well logs: NLOD 2.0 (Norwegian Licence for Open Government Data).
Lithology interpretations: CC BY 4.0.

Run once from this folder:  python make_force_wells.py
"""
import pandas as pd

TRAIN_URL = ("https://raw.githubusercontent.com/bolgebrygg/Force-2020-Machine-Learning-competition/"
             "master/lithology_competition/data/train.zip")

TRAIN_WELLS = ['16/10-2', '16/10-5', '16/5-3', '16/2-6', '16/2-16', '25/11-19 S',
               '31/2-9', '31/2-19 S', '32/2-1', '33/9-17', '34/12-1', '34/3-1 A',
               '35/9-10 S', '35/9-5']
BLIND_WELLS = ['35/11-11']

COLUMNS = ['WELL', 'DEPTH_MD', 'X_LOC', 'Y_LOC', 'Z_LOC', 'GROUP', 'FORMATION',
           'CALI', 'BS', 'GR', 'SGR', 'SP', 'RSHA', 'RMED', 'RDEP', 'RXO',
           'RHOB', 'DRHO', 'NPHI', 'PEF', 'DTC',
           'FORCE_2020_LITHOFACIES_LITHOLOGY', 'FORCE_2020_LITHOFACIES_CONFIDENCE']

print('Downloading FORCE 2020 training data (~90 MB)...')
data = pd.read_csv(TRAIN_URL, sep=';', compression='zip', usecols=COLUMNS)

data = data[data['WELL'].isin(TRAIN_WELLS + BLIND_WELLS)].copy()
data['SET'] = data['WELL'].map(lambda w: 'blind' if w in BLIND_WELLS else 'train')

data.to_csv('force_wells.csv.gz', index=False, float_format='%.4f')
print(f"Saved force_wells.csv.gz: {len(data)} rows, {data['WELL'].nunique()} wells")
print(data.groupby('SET')['WELL'].nunique())
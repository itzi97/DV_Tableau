import requests
import pandas as pd
import numpy as np
from io import BytesIO

# ── Data sources ──────────────────────────────────────────────────────────────
LAW_URL = "https://raw.githubusercontent.com/itzi97/DV_Tableau/main/data/database-statefirearmlaws.xlsx"
RATE_URL = "https://raw.githubusercontent.com/itzi97/DV_Tableau/main/data/Firearm_suicide_homicide_dataset_v2.csv"

laws = pd.read_excel(BytesIO(requests.get(LAW_URL).content))
rates = pd.read_csv(RATE_URL)

# ── Law group scores (row-level, non-aggregate) ────────────────────────────
df = laws.merge(rates[['year','state','firearm_homicide_rate']], on=['year','state'], how='inner')
df['public_score']   = df['universal'] + df['gvro']    + df['assault']
df['evidence_score'] = df['permit']    + df['waiting'] + df['mcdv']

# ── Find first adoption year per state per group ───────────────────────────
def get_adoption_year(df, score_col, threshold=1):
    results = []
    for state, grp in df.groupby('state'):
        grp = grp.sort_values('year')
        crossed = grp[grp[score_col] >= threshold]
        if len(crossed) > 0:
            results.append({'state': state, 'adopt_year': crossed['year'].iloc[0]})
    return pd.DataFrame(results)

public_adopt   = get_adoption_year(df, 'public_score')
evidence_adopt = get_adoption_year(df, 'evidence_score')

# ── Build event-time dataset ───────────────────────────────────────────────
def build_event_study(df, adopt_df, label, window=(-15, 15)):
    records = []
    for _, row in adopt_df.iterrows():
        state, adopt_year = row['state'], row['adopt_year']
        state_data = df[df['state'] == state][['year','firearm_homicide_rate']].copy()
        state_data['event_year'] = state_data['year'] - adopt_year
        state_data = state_data[
            (state_data['event_year'] >= window[0]) &
            (state_data['event_year'] <= window[1])
        ]
        state_data['law_group'] = label
        records.append(state_data)
    return pd.concat(records, ignore_index=True)

public_es   = build_event_study(df, public_adopt,   'Popular Laws')
evidence_es = build_event_study(df, evidence_adopt, 'Evidence Laws')
combined    = pd.concat([public_es, evidence_es], ignore_index=True)

# ── Aggregate: mean ± 95% CI per event_year x law_group ───────────────────
avg = combined.groupby(['law_group','event_year'])['firearm_homicide_rate'] \
              .agg(['mean','sem','count']).reset_index()
avg.columns = ['law_group','event_year','mean_rate','sem','n_states']
avg['ci_upper'] = avg['mean_rate'] + 1.96 * avg['sem']
avg['ci_lower'] = avg['mean_rate'] - 1.96 * avg['sem']

# ── Export ─────────────────────────────────────────────────────────────────
avg.to_csv('data/event_study_results.csv', index=False)
combined.to_csv('data/event_study_raw.csv', index=False)
print('Saved: data/event_study_results.csv and data/event_study_raw.csv')

import requests
import pandas as pd
import numpy as np
from io import BytesIO

# ── Data sources
LAW_URL  = "https://raw.githubusercontent.com/itzi97/DV_Tableau/main/data/database-statefirearmlaws.xlsx"
RATE_URL = "https://raw.githubusercontent.com/itzi97/DV_Tableau/main/data/Firearm_suicide_homicide_dataset_v2.csv"

laws  = pd.read_excel(BytesIO(requests.get(LAW_URL).content))
rates = pd.read_csv(RATE_URL)

# ── Merge
df = laws.merge(rates[['year','state','firearm_homicide_rate']], on=['year','state'], how='inner')

# ── Law group scores (row-level)
# Popular : red flag (gvro) + assault weapons ban  [removed universal/background checks]
# Evidence: permit-to-purchase + waiting + DV restriction + universal background checks
df['public_score']   = df['gvro']   + df['assault']
df['evidence_score'] = df['permit'] + df['waiting'] + df['mcdv'] + df['universal']

# ── Find first year each state adopts at least 1 law from each group
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

# ── Build event-time dataset (±15 years around adoption)
def build_event_study(df, adopt_df, label, window=(-15, 15)):
    records = []
    for _, row in adopt_df.iterrows():
        state, adopt_year = row['state'], row['adopt_year']
        s = df[df['state'] == state][['year','firearm_homicide_rate']].copy()
        s['event_year'] = s['year'] - adopt_year
        s = s[(s['event_year'] >= window[0]) & (s['event_year'] <= window[1])]
        s['law_group'] = label
        s['state'] = state
        records.append(s)
    return pd.concat(records, ignore_index=True)

public_es   = build_event_study(df, public_adopt,   'Popular Laws')
evidence_es = build_event_study(df, evidence_adopt, 'Evidence Laws')
combined    = pd.concat([public_es, evidence_es], ignore_index=True)

# ── Normalize: subtract year-0 rate so Y = change from adoption baseline
def normalize_to_year0(df_es):
    records = []
    for (state, law_group), grp in df_es.groupby(['state', 'law_group']):
        baseline = grp[grp['event_year'] == 0]['firearm_homicide_rate'].values
        if len(baseline) == 0:
            continue
        grp = grp.copy()
        grp['rate_change'] = grp['firearm_homicide_rate'] - baseline[0]
        records.append(grp)
    return pd.concat(records, ignore_index=True)

combined_norm = normalize_to_year0(combined)

# ── Aggregate: mean ± 95% CI
avg = combined_norm.groupby(['law_group','event_year'])['rate_change'] \
                   .agg(['mean','sem','count']).reset_index()
avg.columns = ['law_group','event_year','mean_change','sem','n_states']
avg['ci_upper'] = avg['mean_change'] + 1.96 * avg['sem']
avg['ci_lower'] = avg['mean_change'] - 1.96 * avg['sem']

# ── Export
avg.to_csv('data/event_study_results.csv', index=False)
combined_norm.to_csv('data/event_study_raw.csv', index=False)
print('Saved: data/event_study_results.csv')

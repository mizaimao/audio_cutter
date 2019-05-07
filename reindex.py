#!/usr/bin/env python

import pandas as pd
df = pd.read_csv('data/export.csv',sep='\t')
df['Index'] = range(1,df.shape[0]+1)
df['Edits'] = [0] * df.shape[0]
df.to_csv('data/export.csv', sep='\t', index=False)

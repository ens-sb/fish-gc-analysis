#!/usr/bin/env python

import re
import os
import pandas as pd
import matplotlib.pyplot as plt

def parse_iqtree_matrix(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Find the Rate matrix Q block
    matrix_match = re.search(r'Rate matrix Q:\n\n\s+A\s+(.*?)\n\s+C\s+(.*?)\n\s+G\s+(.*?)\n\s+T\s+(.*)', content)
    if not matrix_match:
        return None

    # Parse rows into a numerical grid
    rows = [list(map(float, matrix_match.group(i).split())) for i in range(1, 5)]
    
    # Mapping: A=0, C=1, G=2, T=3
    # WEAK (A, T) indexes: 0, 3
    # STRONG (G, C) indexes: 1, 2
    
    # Flux W -> S: A->C (0,1), A->G (0,2), T->C (3,1), T->G (3,2)
    ws_rates = [rows[0][1], rows[0][2], rows[3][1], rows[3][2]]
    
    # Flux S -> W: C->A (1,0), C->T (1,3), G->A (2,0), G->T (2,3)
    sw_rates = [rows[1][0], rows[1][3], rows[2][0], rows[2][3]]
    
    flux_ws = sum(ws_rates)
    flux_sw = sum(sw_rates)
    bias = flux_ws / flux_sw
    
    return {
        'file': os.path.basename(file_path).rsplit('.', 1)[0],
        'W_to_S': flux_ws,
        'S_to_W': flux_sw,
        'Bias_B': bias
    }

# Run on your files
results = []
for file in [f for f in os.listdir('.') if f.endswith('.iqtree')]:
    data = parse_iqtree_matrix(file)
    if data: results.append(data)

df = pd.DataFrame(results)
print(df)

# Plotting
plt.figure(figsize=(8, 6))
for i, row in df.iterrows():
    plt.scatter(row['S_to_W'], row['W_to_S'], label=row['file'], s=100)
    
plt.plot([0, max(df['W_to_S'])], [0, max(df['W_to_S'])], 'k--', alpha=0.5, label='Equilibrium (B=1)')
plt.xlabel('Strong → Weak Rate (Pull toward AT)')
plt.ylabel('Weak → Strong Rate (Push toward GC)')
plt.title('Mutational Pressure: gBGC vs Selection')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('ws_rates.pdf', bbox_inches='tight')

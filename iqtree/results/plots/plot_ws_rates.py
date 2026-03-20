#!/usr/bin/env python

import re
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

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
    
    # Parse filename: e.g. aKRAB_NEG_1_s12
    basename = os.path.basename(file_path).rsplit('.', 1)[0]
    match = re.match(r'(.+?)_(NEG|POS|UNK)_(\d+)_(s12|s3)', basename)
    status = match.group(2) if match else 'unknown'
    site = match.group(4) if match else 'unknown'
    group_id = match.group(3) if match else ''
    
    return {
        'file': basename,
        'status': status,
        'site': site,
        'group_id': group_id,
        'W_to_S': flux_ws,
        'S_to_W': flux_sw,
        'Bias_B': bias
    }

# Run on your files
results = []
for file in [f for f in os.listdir('../') if f.endswith('.iqtree')]:
    data = parse_iqtree_matrix(f"../{file}")
    if data: results.append(data)

df = pd.DataFrame(results)
print(df.to_string())

# Define colors for status and markers for site
status_colors = {
    'NEG': 'tab:blue',
    'POS': 'tab:red',
    'UNK': 'tab:gray'
}

site_markers = {
    's12': 'o',   # circle for sites 1&2
    's3':  's'    # square for site 3
}

# Plotting
fig, ax = plt.subplots(figsize=(8, 6))

# Plot each group
for (status, site), grp in df.groupby(['status', 'site']):
    ax.scatter(
        grp['S_to_W'], grp['W_to_S'],
        color=status_colors.get(status, 'black'),
        marker=site_markers.get(site, 'x'),
        s=100, edgecolors='black', linewidths=0.5,
    )

# Label each point with the group_id (clade)
for _, row in df.iterrows():
    ax.annotate(
        row['group_id'],
        (row['S_to_W'], row['W_to_S']),
        textcoords='offset points',
        xytext=(6, 6),
        fontsize=8,
        alpha=0.8
    )

# Diagonal equilibrium line
max_val = max(df['W_to_S'].max(), df['S_to_W'].max())
ax.plot([0, max_val], [0, max_val], 'k--', alpha=0.5)

ax.set_xlabel('Strong → Weak Rate (Pull toward AT)')
ax.set_ylabel('Weak → Strong Rate (Push toward GC)')
ax.set_title('Mutational Pressure: gBGC vs Selection')

# Build a manual legend: one entry per status (color) + one per site (marker)
legend_elements = []
for status, color in status_colors.items():
    legend_elements.append(Line2D([0], [0], marker='o', color='w',
                                   markerfacecolor=color, markeredgecolor='black',
                                   markersize=10, label=status))
for site, marker in site_markers.items():
    legend_elements.append(Line2D([0], [0], marker=marker, color='w',
                                   markerfacecolor='tab:gray', markeredgecolor='black',
                                   markersize=10, label=site))
legend_elements.append(Line2D([0], [0], linestyle='--', color='black',
                               alpha=0.5, label='Equilibrium (B=1)'))

ax.legend(handles=legend_elements, title='Status / Site')

ax.grid(True, alpha=0.3)
fig.savefig('ws_rates.pdf', bbox_inches='tight')
plt.show()

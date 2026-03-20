#!/usr/bin/env python

import re
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def extract_rates(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Locate the Rate matrix Q
    # We look for the 4x4 block following "Rate matrix Q:"
    regex = r"Rate matrix Q:\n\n\s+A\s+(.*?)\n\s+C\s+(.*?)\n\s+G\s+(.*?)\n\s+T\s+(.*)"
    match = re.search(regex, content)
    if not match:
        return None

    # Parse rows into floats
    rows = [list(map(float, match.group(i).split())) for i in range(1, 5)]
    
    # Map the 12 individual non-diagonal rates
    # Matrix order: A, C, G, T
    rates = {
        'A->C': rows[0][1], 'A->G': rows[0][2], 'A->T': rows[0][3],
        'C->A': rows[1][0], 'C->G': rows[1][2], 'C->T': rows[1][3],
        'G->A': rows[2][0], 'G->C': rows[2][1], 'G->T': rows[2][3],
        'T->A': rows[3][0], 'T->C': rows[3][1], 'T->G': rows[3][2]
    }
    return rates

# 1. Gather data from all .iqtree files
results = []
for file in sorted([f for f in os.listdir('../') if f.endswith('.iqtree')]):
    data = extract_rates(f"../{file}")
    if data:
        data['filename'] = file.split('.')[0]
        results.append(data)

df = pd.DataFrame(results)

# 2. Visualise and Save to PDF
with PdfPages('IQTree_Rate_Analysis.pdf') as pdf:
    for i, row in df.iterrows():
        plt.figure(figsize=(10, 6))
        
        # Sort rates into categories for the plot
        # WS = Push toward Strong (gBGC), SW = Pull toward Weak (Methylation/Neutral)
        ws_labels = ['A->C', 'A->G', 'T->C', 'T->G']
        sw_labels = ['C->A', 'C->T', 'G->A', 'G->T']
        other_labels = ['A->T', 'T->A', 'C->G', 'G->C']
        
        all_labels = ws_labels + sw_labels + other_labels
        all_values = [row[l] for l in all_labels]
        colors = ['red']*4 + ['blue']*4 + ['gray']*4
        
        plt.bar(all_labels, all_values, color=colors)
        plt.axhline(0, color='black', linewidth=0.8)
        
        # Add a "Net Bias" calculation to the title
        ws_sum = sum(row[l] for l in ws_labels)
        sw_sum = sum(row[l] for l in sw_labels)
        bias = ws_sum / sw_sum
        
        plt.title(f"Analysis: {row['filename']}\nNet WS-Bias Ratio: {bias:.2f} (Red=Push, Blue=Leak)")
        plt.ylabel("Substitution Rate")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        pdf.savefig()
        plt.close()

print("Success: IQTree_Rate_Analysis.pdf has been generated.")

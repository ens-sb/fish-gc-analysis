fish-gc-analysis
================

Alignment data
---------------

The codon alignment data and starting tree topology used in available under `data/`. They were produced by a run of the `corefu` pipeline on the 178 fish genomes dataset and then agressively filtered to keep only the least gappy sites.

Filtering log:

```
-------------
| Arguments |
-------------
Input file: merged_codon_alns.fas (format: fasta)
Output file: fish178_struct_trimmed_codon_aln.fas (format: fasta)
Sequence type: Nucleotides
Gaps threshold: 0.01
Gap characters: ['-', '?', '*', 'X', 'x', 'N', 'n']
Trimming mode: gappy
Create complementary output: False
Process as codons: True
Trim ends only: False
Create log file: False


------------------------
| Writing output files |
------------------------
Trimmed alignment: fish178_struct_trimmed_codon_aln.fas
Complement file: False
Log file: False


---------------------
| Output Statistics |
---------------------
Original length: 16917759
Number of sites kept: 49737
Number of sites trimmed: 16868022
Percentage of alignment trimmed: 99.706%

Execution time: 442.525s
```

nhPhyml analyses
----------------

## Preprocessing

For the nhPhyml analyses, the identifiers from the trimmed alignment and the starting tree topology were modified to be compatible with the requirements of nhPhyml (available under `nhphyml/data`).

## Running nhPhyml

Two separate nhPhyml analyses were run — one on codon sites 1+2 and one on codon site 3 — to assess GC-content heterogeneity across the phylogeny at different codon positions.

Both analyses use the same preprocessed alignment and rooted tree from `nhphyml/data/` and share the following nhPhyml settings:

| Parameter | Value | Description |
|-----------|-------|-------------|
| `-format` | `s` | Sequential Phylip format |
| `-tstv` | `e` | Estimate the transition/transversion ratio |
| `-rates` | `4` | 4 discrete gamma rate categories |
| `-alpha` | `e` | Estimate the gamma shape parameter |
| `-topology` | `e` | Estimate (optimise) the tree topology |
| `-eqfreq` | `lim` | Use limited equilibrium frequency model |
| `-numeqfreq` | `10` | 10 equilibrium frequency categories |
| `-eqfreqlow` | `0.4` | Lower bound for equilibrium GC frequency |
| `-eqfrequpp` | `0.9` | Upper bound for equilibrium GC frequency |

### Sites 1+2

Run script: `nhphyml/sites12/run_nhphyml_sites12.sh`

```bash
nhPhyml -format=s -sequences=fish178_struct_trimmed_codon_aln_safe.phy \
    -tree=../data/rooted_corefu_iqtree_nuc_sites3_safe.nwk -positions=12 -tstv=e -rates=4 -alpha=e \
    -topology=e -eqfreq=lim -numeqfreq=10 -eqfreqlow=0.4 -eqfrequpp=0.9
```

Output files (under `nhphyml/sites12/`):

- `*_nhPhymlGC.tree` — Tree with GC-content estimates at each node
- `*_nhPhymlEq.tree` — Tree under the equilibrium (homogeneous) model
- `*_nhPhyml.lk` — Log-likelihood of the fitted model
- `*_nhPhyml.lnf` — Per-site log-likelihoods
- `*_nhPhyml.compout` — Composition (GC-content) estimates per branch

### Site 3

Run script: `nhphyml/sites3/run_nhphyml_sites3.sh`

```bash
nhPhyml -format=s -sequences=fish178_struct_trimmed_codon_aln_safe.phy \
    -tree=../data/rooted_corefu_iqtree_nuc_sites3_safe.nwk -positions=3 -tstv=e -rates=4 -alpha=e \
    -topology=e -eqfreq=lim -numeqfreq=10 -eqfreqlow=0.4 -eqfrequpp=0.9
```

Output files will be written to `nhphyml/sites3/` with the same suffixes as above.

## Post-processing

The script `nhphyml/scripts/remap_ids.py` restores the original species identifiers in the nhPhyml output trees by reversing the safe-ID mapping:

```bash
nhphyml/scripts/remap_ids.py -t <nhphyml_output.tree> -m nhphyml/data/id_mapping.tsv -o <restored.nwk>
```

Use the `-k`/`--keep-gc` flag to retain the per-leaf GC-content values annotated by nhPhyml alongside the restored names.

## Results

### G+C content visualization via Newick trees

Since nhPhyML uses a non-stationary and non-homogeneous model, the G+C content is not constant across the tree. These two files help you visualize the two different ways the model describes G+C composition:

`fish178_nhphyml_sites*_eq*.nwk`

- **What it displays:** The **equilibrium G+C content** for each branch.
- **Meaning:** This represents the G+C content towards which the sequence would eventually evolve if the evolutionary process on that specific branch continued indefinitely. In a non-homogeneous model, each branch can have its own "target" equilibrium frequency.
- **Location:** The values are usually displayed in the position where bootstrap supports are typically found.

`fish178_nhphyml_sites*_gc*.nwk`

- **What it displays:** The **actual estimated G+C content** at each internal node.
- **Meaning:** This is the inferred G+C composition of the ancestral sequence at that specific point in time (at that node). It is the result of the evolutionary process moving from the root toward the tips.
- **Note:** This file typically does not include the G+C content of the root node. To find the estimated G+C content of the very first ancestor (the root), you should check the second line of the `.lk` (likelihood) output file.

The Newick files are generated for both the sites 1+2 and site 3 analyses, allowing you to compare how G+C content varies across the tree for different codon positions.

### Comparing topologies using tanglegrams

We use tanglegrams to visually compare tree topologies:

- `nhphyml/sites3/tanglegrams/corefu_prot_vs_nhphyml_sites3.pdf` - a comparison of the tree inferred by nhPhyml on codon site 3 (right) with the tree inferred by IQ-TREE on the corresponding protein alignment (left). It is apparent from the plot that the toplogies are very similar.

- `nhphyml/sites3/tanglegrams/nhphyml_sites3_vs_nhphyml_sites12.pdf` - a comparison of the tree inferred by nhPhyml on codon site 3 (left) with the tree inferred by nhPhyml on codon sites 1+2 (right).

- `nhphyml/sites12/tanglegrams/corefu_prot_vs_nhphyml_sites12.pdf` - a comparison of the tree inferred by nhPhyml on codon sites 1+2 (right) with the tree inferred by IQ-TREE on the corresponding protein alignment (left).
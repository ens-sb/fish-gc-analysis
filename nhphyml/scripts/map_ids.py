#!/usr/bin/env python

import sys
import argparse
from Bio import AlignIO
from Bio import Phylo


def prepare_nhphyml_files(fasta_file, tree_file, phylip_out, tree_out, map_out):
    """
    Reads a FASTA alignment and a Newick tree, replaces long IDs with
    safe 10-character-compliant IDs, and exports to Phylip and Newick formats.
    """
    print(f"Reading alignment from {fasta_file}...")
    try:
        alignment = AlignIO.read(fasta_file, "fasta")
    except Exception as e:
        print(f"Error reading FASTA file: {e}")
        sys.exit(1)

    mapping = {}

    # 1. Generate safe IDs and rename sequences
    for i, record in enumerate(alignment):
        original_id = record.id
        # Generate a safe, sequential ID (e.g., S0001)
        safe_id = f"S{i+1:04d}"

        mapping[original_id] = safe_id

        # Overwrite the record with the safe ID and clear the description
        # so Biopython doesn't accidentally write it into the Phylip file
        record.id = safe_id
        record.description = ""

    # 2. Write the Phylip alignment
    print(f"Writing Phylip alignment to {phylip_out}...")
    AlignIO.write(alignment, phylip_out, "phylip-sequential")

    # 3. Process the tree file
    print(f"Reading tree from {tree_file}...")
    try:
        tree = Phylo.read(tree_file, "newick")
    except Exception as e:
        print(f"Error reading Tree file: {e}")
        sys.exit(1)

    # 4. Replace terminal node (leaf) names in the tree
    for clade in tree.find_clades(terminal=True):
        if clade.name:
            # Strip quotes if they were added to the newick tips
            clean_name = clade.name.strip("'").strip('"')
            if clean_name in mapping:
                clade.name = mapping[clean_name]
            else:
                print(f"Warning: Tree tip '{clean_name}' was not found in the FASTA alignment!")

    print(f"Writing updated tree to {tree_out}...")
    Phylo.write(tree, tree_out, "newick")

    # 5. Save the mapping to a TSV file for later restoration
    print(f"Saving ID mapping to {map_out}...")
    with open(map_out, "w") as f:
        f.write("Safe_ID\tOriginal_ID\n")
        for orig, safe in mapping.items():
            f.write(f"{safe}\t{orig}\n")

    print("\nSuccess! All files generated.")


if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="Format FASTA alignments and Newick trees for nhPhyml by generating safe IDs."
    )

    # Required arguments
    parser.add_argument("-f", "--fasta", required=True, help="Path to the input FASTA alignment")
    parser.add_argument("-t", "--tree", required=True, help="Path to the input Newick tree file")

    # Optional arguments with defaults
    parser.add_argument(
        "-p",
        "--phylip",
        default="alignment_safe.phy",
        help="Output path for the safe Phylip alignment (default: alignment_safe.phy)",
    )
    parser.add_argument(
        "-o",
        "--outtree",
        default="tree_safe.nwk",
        help="Output path for the safe Newick tree (default: tree_safe.nwk)",
    )
    parser.add_argument(
        "-m",
        "--mapping",
        default="id_mapping.tsv",
        help="Output path for the ID mapping TSV file (default: id_mapping.tsv)",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Run the main function using the parsed arguments
    prepare_nhphyml_files(args.fasta, args.tree, args.phylip, args.outtree, args.mapping)

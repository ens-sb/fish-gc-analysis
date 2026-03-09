#!/usr/bin/env python

# See the NOTICE file distributed with this work for additional information
# regarding copyright ownership.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Remove every third site from a codon alignment by keeping the first two. The input sequences
must have a length divisible by 3.

Example:
    $ python remove_third_sites.py -i input.fas -o output.fas
"""

import sys
import argparse

from Bio import SeqIO
from Bio.Seq import Seq

# Parse command line arguments:
parser = argparse.ArgumentParser(description="Remove the third sites from a codon alignment.")
parser.add_argument("-i", metavar="input", type=str, help="Input fasta.", required=True)
parser.add_argument("-o", metavar="output", type=str, help="Output fasta.", required=True)


if __name__ == "__main__":
    args = parser.parse_args()

    with open(args.o, "w", encoding="utf-8") as out_fh:
        for record in SeqIO.parse(args.i, "fasta"):
            # Check if sequence length is divisible by 3:
            if len(record.seq) % 3 != 0:
                sys.stderr.write(f"The length of sequence {record.id} is not divisible by 3!\n")
                sys.exit(1)
            # Keep first and second sites, removing the third:
            seq_str = str(record.seq)
            record.seq = Seq("".join(seq_str[i : i + 2] for i in range(0, len(seq_str), 3)))
            # Write out record:
            SeqIO.write(record, out_fh, "fasta")

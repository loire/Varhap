# Varhap
A small pipeline designed to call variants on haploids genome.
Configuration file is for the cc2 cluster in cirad. 

## Dependencies
* python 3 and 2 
* script fastqCombinedPairedEnd.py (provided in the repo): used to synchronize read pairs if you cleaned them independantly.
* snakemake
* bwa
* freebayes
* vcffilter (comes with freebayes)
* samtools
* picard tools 

## usage (on cc2):
file VARHAP.snake needs to be edited in order to:
* specify data directory (several reads pair can be analyzed jointly
* Reference sequences on which mapping should be done (fasta format)
* extension of file name (reads R1) should be specified
* module load should work as such
Then you can try:

```
module load system/python/3.4.3
snakemake -s VARHAP.snake  --jobs 12 --cluster "qsub -q normal.q -cwd -V -pe parallel_smp {threads}" -r
```

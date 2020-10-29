#!/usr/bin/env bash
snakemake --forcerun --resources mem_mb=5632000 --jobs 128\
          --cluster "sbatch --partition fat03 -n {cluster.n} --time {cluster.time} --mail-type=FAIL"\
          --cluster-config cluster.json\
          --jobname "{jobid}.{rulename}"\
          --keep-going\
          --rerun-incomplete\
          --use-conda

	  

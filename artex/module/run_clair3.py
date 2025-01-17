import os
import sys
import logging
import subprocess


def run_clair3(bam: str, ref: str, threads: int, model: str, builtin_model_path: str, config: str, work: str, chunk_size: int, min_coverage: int, verbose: bool) -> None:
    if model:
        clair3_model = model
    else:
        predownload = {"R9G2": "ont_guppy2", "R9G4": "r941_prom_hac_g360+g422", "R9G6": "r941_prom_sup_g5014"}
        clair3_model = os.path.join(builtin_model_path, predownload[config])


    # change to working directory and run Clair3
    os.chdir(work)
    clair3_command = f'run_clair3.sh --bam_fn={bam} --ref_fn={ref} --threads={threads} --platform="ont" --model_path={clair3_model} --output="clair3" --include_all_ctgs --no_phasing_for_fa --chunk_size={chunk_size} --haploid_sensitive --min_coverage={min_coverage}'
    
    clair3_result = subprocess.run(clair3_command, shell = True, capture_output = True, text = True)
    

    if clair3_result.returncode != 0:
        logging.error("Fail to run Clair3 variant calling")
        logging.error(clair3_result.stdout)
        sys.exit(1)

    if verbose:
        logging.info(clair3_result.stdout)



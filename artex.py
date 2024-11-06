import click
import os
import sys
from src.test_env import test_env
import subprocess

CURRENT = os.path.dirname(os.path.realpath(__file__))

@click.command()
@click.option("-i", "--input", type = str, help = "Path to the Artic pipeline output directory")
@click.option("-o", "--output", type = str, help = "Output directory")
@click.option("-p", "--prefix", type = str, default = "clair3", help = "Output prefix")
@click.option("-c", "--config", type = str, help = "Basecalling configuration, predicted by LongBow, options: [R9G2, R9G4, R9G6]")
@click.option("-w", "--work", type = str, default = "SAME AS OUTPUT PATH", help = "Working directory, for storing intermediate results")
@click.option("-r", "--ref", type = str, default = f"{CURRENT}/ref/nCoV-2019/V3/nCoV-2019.reference.fasta", help = "Reference file")
@click.option("-m", "--model", type = str, default = f"{CURRENT}/clair3_model", help = "Path to clair3 model")
@click.option("-t", "--threads", type = int, default = 12, help = "Parallel threads for Clair3")
@click.option("--chunk_size", type = int, default = 2000, help = "Chuck size for Clair3")
@click.option("--min_coverage", type = int, default = 10, help = "Minimum coverage required to call a variant in Clair3")
@click.option("--test", is_flag = True, help = "Run test for the current environment")
@click.option("--verbose", is_flag = True, help = "Verbose mode, print progress to Stdout")
@click.version_option(version="0.1.1", prog_name = r"Artex, Artic pipeline extension for calling low coverage variants, based on Python 3.7+")
def main(input, output, prefix, config, work, ref, model, threads, chunk_size, min_coverage, test, verbose):
    # check environment or check parameters
    if test:
        test_env()
        sys.exit(0)
    else:
        if (not input) or (not output):
            if (not input):
                raise click.UsageError(r"Error: -i / --input parameter is required")
            if (not output):
                raise click.UsageError(r"Error: -o / --output parameter is required")
    if verbose:
        print("Check paramters")	

    # clean parameters
    input = os.path.abspath(input)
    output = os.path.abspath(output)
    if not os.path.exists(output):
        os.makedirs(output)

    if work == "SAME AS OUTPUT PATH":
        work = output
    else:
        work = os.path.abspath(work)

    if config not in {"R9G2", "R9G4", "R9G6"}:
        raise click.UsageError(r"Error: -c / --config paramter must be in [R9G2, R9G4, R9G6, R10D0]")
	
    if verbose:
        print("Pasring file from Artic pipeline")

    # run clair3 for re-variant calling
    # find sorted bam from artic pipepline
    bam = None
    pass_vcf = None
    fail_vcf = None
    file_prefix = None
    for file in os.listdir(input):
        if os.path.isfile(os.path.join(input, file)):
            if file.endswith(".sorted.bam"):
                if "trimmed" not in file:
                    bam = os.path.join(input, file)
            if file.endswith(".pass.vcf.gz"):
                pass_vcf = os.path.join(input, file)
                file_prefix = file.split(".pass.vcf.gz")[0]
            if file.endswith(".fail.vcf"):
                fail_vcf = os.path.join(input, file)
	
    # bgzip and index fail.vcf
    if f"{fail_vcf}.gz" not in os.listdir(input):
        bgzip_command = f"bgzip -k {fail_vcf}"
        bgzip_result = subprocess.run(bgzip_command, shell = True, capture_output = True, text = True)
        if bgzip_result.returncode != 0:
            print(bgzip_result.stdout)
            sys.exit(1)
    
    if f"{fail_vcf}.gz.tbi" not in os.listdir(input):
        tabix_command = f"tabix {fail_vcf}.gz"
        tabix_result = subprocess.run(tabix_command, shell = True, capture_output = True, text = True)
        if tabix_result.returncode != 0:
            print(tabix_result.stdout)
            sys.exit(1)
	
		
    if not(bam):
        raise FileNotFoundError(r"sorted.bam file not in input directory")
    if not(pass_vcf):
        raise FileNotFoundError(r"pass vcf file not in input directory")
    if not(fail_vcf):
        raise FileNotFoundError(r"fail vcf file not in input directory")
	
    if verbose:
        print(f"BAM file is: {bam}")
        print(f"PASS vcf file is: {pass_vcf}")
        print(f"FAIL vcf file is: {fail_vcf}")

    # choose clair3 model according to config
    clair3_model = {"R9G2": "ont_guppy2", "R9G4": "r941_prom_hac_g360+g422", "R9G6": "r941_prom_sup_g5014"}
    chosen = clair3_model[config]

    if verbose:
        print("Start running Clair3")

    # change to working directory
    os.chdir(work)
    clair3_command = f'run_clair3.sh --bam_fn={bam} --ref_fn={ref} --threads={threads} --platform="ont" --model_path={os.path.join(model, chosen)} --output={prefix} --include_all_ctgs --no_phasing_for_fa --chunk_size={chunk_size} --haploid_sensitive --min_coverage={min_coverage}'
    clair3_result = subprocess.run(clair3_command, shell = True, capture_output = True, text = True)
    if clair3_result.returncode != 0:
        print(clair3_result.stdout)
        sys.exit(1)	

    # run bcftools
    os.makedirs(os.path.join(work, "for_merge"), exist_ok = True)
    if verbose:
        print("Intersecting vcf")
    
    # intersect vcfs
    clair3_output = os.path.join(prefix, "merge_output.vcf.gz")
    intersect_command = f"bcftools isec -p ./for_merge -n=2 {fail_vcf}.gz {clair3_output}"
    intersect_result = subprocess.run(intersect_command, shell = True, capture_output = True, text = True)
    if intersect_result.returncode != 0:
        print(intersect_result.stdout)
        sys.exit(1)	
		
    if verbose:
        print("Merging vcf")
	
    bgzip_intersect = "bgzip -k ./for_merge/0000.vcf"
    bgzip_intersect_result = subprocess.run(bgzip_intersect, shell = True, capture_output = True, text = True)
    tabix_intersect = "tabix ./for_merge/0000.vcf.gz"
    tabix_intersect_result = subprocess.run(tabix_intersect, shell = True, capture_output = True, text = True)
	
    # merge vcfs
    merge_command = f"bcftools merge -o {file_prefix}.artex.vcf.gz -O z {pass_vcf} ./for_merge/0000.vcf.gz --force-samples"
    merge_result = subprocess.run(merge_command, shell = True, capture_output = True, text = True)
    if merge_result.returncode != 0:
        print(merge_result.stdout)
        sys.exit(1)
		

if __name__ == "__main__":
    main()

import click
import os
import sys
from module.check_parameter import check_parameter
from module.parse_artic_files import parse_artic_files
from module.run_clair3 import run_clair3
from module.bcftools_postprocess import bcftools_postprocess
import subprocess
import logging

CURRENT = os.path.dirname(os.path.realpath(__file__))

@click.command()
@click.option("-i", "--input", type = str, help = "Path to the Artic pipeline output directory")
@click.option("-o", "--output", type = str, help = "Output directory")
@click.option("-p", "--prefix", type = str, default = "sample", help = "Output prefix")
@click.option("-c", "--config", type = str, default = None, help = "Basecalling configuration, config which have predownloaded Clair3 model included: [R9G2, R9G4, R9G6]")
@click.option("-w", "--work", type = str, default = "SAME AS OUTPUT PATH", help = "Working directory, for storing intermediate results")
@click.option("-r", "--ref", type = str, default = f"{CURRENT}/ref/nCoV-2019/V3/nCoV-2019.reference.fasta", help = "Reference file")
@click.option("-m", "--model", type = str, default = None, help = "Path to clair3 model")
@click.option("-t", "--threads", type = int, default = 12, help = "Parallel threads for Clair3")
@click.option("--chunk_size", type = int, default = 2000, help = "Chuck size for Clair3")
@click.option("--min_coverage", type = int, default = 10, help = "Minimum coverage required to call a variant in Clair3")
@click.option("--test", is_flag = True, help = "Run test for the current environment")
@click.option("--verbose", is_flag = True, help = "Verbose mode")
@click.version_option(version="0.2.0", prog_name = r"Artex, Artic pipeline extension for calling low coverage variants, based on Python 3.7+")
def main(input, output, prefix, config, work, ref, model, threads, chunk_size, min_coverage, test, verbose):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])
    
    # setting verbose mode
    # print all info if --verbose is set, otherwise only print warning and errors
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    # check environment or check parameters
    logging.info("Checking input paramter")
    input, output, prefix, config, work, ref, model, threads, chunk_size, min_coverage = check_parameter(input, output, prefix, config, work, ref, model, threads, chunk_size, min_coverage, test)

    # find files from Artic pipepline
    logging.info("Parsing file from Artic pipeline input")
    bam, pass_vcf, fail_vcf = parse_artic_files(input)


    # run Clair3 for re-variant-calling
    logging.info("Start running Clair3")
    run_clair3(bam, ref, threads, model, f"{CURRENT}/clair3_model", config, work, chunk_size, min_coverage, verbose)

    # run bcftools intersect Clair3 result with Artic fail variant
    # merge the intersect with pass variant and output
    logging.info("Start bcftools post-processing")
    bcftools_postprocess(input, pass_vcf, fail_vcf, work, prefix)

    logging.info("Artex pipeline success")

    
		


if __name__ == "__main__":
    main()

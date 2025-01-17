import os
import sys
import logging


def parse_artic_files(input: str) -> tuple:

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

    if not(bam):
        logging.error(r"Artic result sorted.bam file not in input directory")
        raise FileNotFoundError(r"Artic result sorted.bam file not in input directory")
    if not(pass_vcf):
        logging.error("Artic result pass vcf file not in input directory")
        raise FileNotFoundError("Artic result pass vcf file not in input directory")
    if not(fail_vcf):
        logging.error("Artic result fail vcf file not in input directory")
        raise FileNotFoundError("Artic result fail vcf file not in input directory")


    logging.info(f"BAM file is: {bam}")
    logging.info(f"PASS vcf file is: {pass_vcf}")
    logging.info(f"FAIL vcf file is: {fail_vcf}")


    return (bam, pass_vcf, fail_vcf)

import os
import sys
import logging
import subprocess
from module.cal_extra_count import extra_variant_count


def bcftools_postprocess(input: str, pass_vcf: str, fail_vcf: str, work: str, prefix: str) -> None:
    # bgzip and index fail.vcf
    os.chdir(work)
    bgzip_command = f"bgzip -kf -c {os.path.join(input, fail_vcf)} > artic.fail.vcf.gz"
    bgzip_result = subprocess.run(bgzip_command, shell = True, capture_output = True, text = True)
    if bgzip_result.returncode != 0:
        logging.error("Fail to bgzip fail vcf from Artic output")
        logging.error(bgzip_result.stdout)
        sys.exit(1)

    tabix_command = f"tabix -f artic.fail.vcf.gz"
    tabix_result = subprocess.run(tabix_command, shell = True, capture_output = True, text = True)
    if tabix_result.returncode != 0:
        logging.error("Fail to tabix fail vcf.gz")
        logging.error(tabix_result.stdout)
        sys.exit(1)


    # Intersect Clair3 output vcf with Artic vcf
    logging.info("Intersecting Clair3 output vcf with Artic vcf")
    os.makedirs(os.path.join(work, "for_merge"), exist_ok = True)

    # intersect vcfs
    clair3_output = os.path.join("./clair3", "merge_output.vcf.gz")
    intersect_command = f"bcftools isec -p ./for_merge -n=2 artic.fail.vcf.gz {clair3_output}"
    intersect_result = subprocess.run(intersect_command, shell = True, capture_output = True, text = True)
    if intersect_result.returncode != 0:
        logging.error("Fail to intersect Clair3 output vcf with Artic vcf")
        logging.info(intersect_result.stdout)
        sys.exit(1)

    logging.info("Merging intersected vcf with Artic pass vcf")
    
    extra_count = extra_variant_count(os.path.abspath("./for_merge/0000.vcf"))
    logging.critical(f"Extra {extra_count} variants found by Artex pipeline")

    bgzip_intersect = "bgzip -kf ./for_merge/0000.vcf"
    bgzip_intersect_result = subprocess.run(bgzip_intersect, shell = True, capture_output = True, text = True)
    tabix_intersect = "tabix -f ./for_merge/0000.vcf.gz"
    tabix_intersect_result = subprocess.run(tabix_intersect, shell = True, capture_output = True, text = True)

    # merge vcfs
    merge_command = f"bcftools merge -o {prefix}.artex.vcf.gz -O z {pass_vcf} ./for_merge/0000.vcf.gz --force-samples"
    merge_result = subprocess.run(merge_command, shell = True, capture_output = True, text = True)
    if merge_result.returncode != 0:
        logging.info("Fail to merge extrac variant of artex to the final output")
        logging.error(merge_result.stdout)
        sys.exit(1)


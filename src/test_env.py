import subprocess


def test_env() -> None:
# test clair3
    clair3_command = "run_clair3.sh --version"
    clair3_result = subprocess.run(clair3_command, shell = True, capture_output = True, text = True)
    if clair3_result.returncode == 0:
        print(f"PASS Clair3 check: {clair3_command}")
        print(f"{clair3_result.stdout}")
    else:
        print(f"FAIL Clair3 installation")

    bcftools_command = "bcftools --version"
    bcftools_result = subprocess.run(clair3_command, shell = True, capture_output = True, text = True)
    if bcftools_result.returncode == 0:
        print(f"PASS bcftools check: {bcftools_command}")
        print(f"{bcftools_result.stdout}")
    else:
        print(f"FAIL bcftools installation check")

    bgzip_command = "bgzip --version"
    bgzip_result = subprocess.run(bgzip_command, shell = True, capture_output = True, text = True)
    if bgzip_result.returncode == 0:
        print(f"PASS bgzip check: {bgzip_command}")
        print(f"{bgzip_result.stdout}")
    else:
        print(f"FAIL bgzip installation check")

    tabix_command = "tabix --version"
    tabix_result = subprocess.run(tabix_command, shell = True, capture_output = True, text = True)
    if tabix_result.returncode == 0:
        print(f"PASS tabix check: {tabix_command}")
        print(f"{tabix_result.stdout}")
    else:
        print(f"FAIL tabix installation check")	

## test_env()

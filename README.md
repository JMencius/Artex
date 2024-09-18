# Artex - Artic pipeline extension

## Introduction
Artex is a software tool designed for re-calling variants at low-coverage or low-quality sites which are often not considered or filtered out in the original `ARTIC pipeline`. It utilizes the amplicon mode of `Clair3` for re-variant calling. Variants are recovered by intersecting the FAIL.vcf results from the ARTIC pipeline with the Clair3 output. Those variant can be of great importance, which can exist in the `S-gene`, such as the example provide in `test_data/ERR5398250`


## Installation 
Artex can operate in most modern operation system with Python environment. 

### Option 1.  Build an conda virtural environment
The `artex.yaml` file is also included in the release, which you can recreate the author's python environment using the following command.
```bash
conda env create -f artex.yaml;
```

### Option 2. Build the environment manually
```bash
conda create -n artex python=3.9.0;
conda activate artex;
conda config --add channels defaults;
conda config --add channels bioconda;
conda config --add channels conda-forge;
conda install -c bioconda clair3;
conda install -c bioconda bcftools;
pip install click;
```

After installation, you can test the installation with:
```bash
./artic --test;
```
Or run the example test data with:
```bash
bash test.sh;
```
The result will be in `test_data/artex_output_ERR5398250`.

## Usage:
There parameters are mandatory:
| Parameters | Explaination |
|:---:|:---:|
|`-i` / `--input`  | Path to the Artic pipeline output directory |
|`-o` / `--output` | Output directory |
|`-c` / `--config` | Basecalling configuration, predcited by LongBow, options: [R9G2, R9G4, R9G6] |


Full parameters
```
Usage: ./artex [OPTIONS]
Usage: python artex.py [OPTIONS]

Options:
  -i, --input TEXT        Path to the Artic pipeline output directory  [REQUIRED]
  -o, --output TEXT       Output directory [REQUIRED]
  -p, --prefix TEXT       Output prefix for Clair3 [DEFAULT: clair3]
  -c, --config TEXT       Basecalling configuration, predcited by LongBow, options: [R9G2, R9G4, R9G6]  [REQUIRED]
  -w, --work TEXT         Workding directory, for storing intermediate results [DEFAULT: SAME AS OUTPUT]
  -r, --ref TEXT          Reference file [DEFAULT: ./ref/nCoV-2019/V3/nCoV-2019.reference.fasta]
  -m, --model TEXT        Path to Clair3 model [DEFAULT: ./clair3_model]
  -t, --threads INTEGER   Parallel threads for Clair3 [DEFAULT: 12]
  --chunk_size INTEGER    Chuck size for Clair3 [DEFAULT: 2000]
  --min_coverage INTEGER  Minimum coverage required to call a variant in Clair3 [DEFAULT: 10]
  --test                  Run test for the current environment
  --verbose               Verbose mode, print progress to Stdout
  --version               Show the version and exit.
  --help                  Show this message and exit.
```

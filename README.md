# Artex - <u>Art</u>ic <u>ex</u>tension

## Introduction
Artex is a software tool designed for re-calling variants at low-coverage or low-quality sites which are often not considered or filtered out in the original `ARTIC pipeline`. It utilizes the amplicon mode of `Clair3` for re-variant calling. Variants are recovered by intersecting the `FAIL.vcf` results from the `ARTIC pipeline` with the Clair3 output. Those variants can be of great importance, which can exist in the `S-gene`, such as the example provided in `test_data/ERR5398250`.


## Installation 
Artex is compatible with most modern operating system that support a Python environment. However, only the _Linux_ operating system has been tested, and its use is recommended.

### Option 1.  Build an conda virtural environment
The `artex.yaml` file is included in the release.
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
<mark>You may have to change the artex file permission to execute it with chmod +x artex .</mark>


## Installation test
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
Three parameters are mandatory:
| Parameters | Explaination |
|:---:|:---:|
|`-i` / `--input`  | Path to the Artic pipeline output directory |
|`-o` / `--output` | Output directory |
|`-c` / `--config` | Basecalling configuration, predcited by LongBow, options: [R9G2, R9G4, R9G6] |


Artex full parameters
```
Usage: ./artex [OPTIONS]
Usage: python artex.py [OPTIONS]

Options:
  -i, --input TEXT        Path to the Artic pipeline output directory  [REQUIRED]
  -o, --output TEXT       Output directory [REQUIRED]
  -p, --prefix TEXT       Output prefix for Clair3 [DEFAULT: clair3]
  -c, --config TEXT       Basecalling configuration, predicted by LongBow, options: [R9G2, R9G4, R9G6]  [REQUIRED]
  -w, --work TEXT         Working directory, for storing intermediate results [DEFAULT: SAME AS OUTPUT]
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
## Performance
For each sample, Artex is expected to finish analysis of extra variant from the results of Artic pipeline with minutes using 12 threads.



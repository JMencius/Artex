# Artex - Artic pipeline extension

## Introduction
Artex is an addition software built to re-variant calling of low coverage sites or low qulaity sites, which is often filtered from the original Aritic pipeline. Briefly, amplicon mode of `Clair3` is delopyed to re-variant calling. Variants were recover from the intersect between `FAIL.vcf` results from the Artic pipeline and Clair3 output.


## Installation 
Artex can operate in most modern operation system with Python 3.7+ environment. 

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
conda install -c bioconda artex;
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
```
Usage: ./artex [OPTIONS]
Usage: python artex.py [OPTIONS]

Options:
  -i, --input TEXT        Path to the Artic pipeline output directory
  -o, --output TEXT       Output directory
  -p, --prefix TEXT       Output prefix
  -c, --config TEXT       Basecalling configuration, predcited by LongBow,
                          options: [R9G2, R9G4, R9G6]
  -w, --work TEXT         Workding directory, for storing intermediate results
  -r, --ref TEXT          Reference file
  -m, --model TEXT        Path to clair3 model
  -t, --threads INTEGER   Parallel threads for Clair3
  --chunk_size INTEGER    Chuck size for Clair3
  --min_coverage INTEGER  Minimum coverage required to call a variant in
                          Clair3
  --test                  Run test for the current environment
  --verbose               Verbose mode, print progress to Stdout
  --version               Show the version and exit.
  --help                  Show this message and exit.
```

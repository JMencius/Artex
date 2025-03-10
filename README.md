# Artex - **Art**ic **ex**tension

## Introduction
Artex is a software tool designed for re-calling variants at low-coverage or low-quality sites typically missed or discarded by the `ARTIC pipeline`. In priciple, Artex utilizes the amplicon mode of `Clair3` for re-variant calling. Variants are recovered by intersecting the `FAIL.vcf` results from the `Artic pipeline` with the `Clair3` output. 

Extra variants found by Artex can be of great importance, which can exist in the `S-gene`, such as the example provided in `./tests/ERR5398250`.


## Installation 
### Option1. Install through Bioconda
Artex is compatible with most modern operating system with Python environment. However, only the _Linux_ operating system has been tested, and its use is recommended. To install:
```bash
conda create -n artex python=3.9.0;
conda install -c bioconda artex;
```

### Option2. Install through pre-built docker image
A pre-built docker image is available at <https://hub.docker.com/repository/docker/jmencius/artex/general>
```bash
docker pull jmencius/artex:0.2.0;
```


### Installation test
After installation, you can test the environment with:
```bash
artex --test;
```


## Usage
Three parameters are mandatory:
| Parameters | Explanation |
|:---:|:---:|
|`-i` / `--input`  | Path to the Artic pipeline output directory |
|`-o` / `--output` | Output directory |
|`-c` / `--config` | Basecalling configuration, predcited by LongBow, options: [R9G2, R9G4, R9G6] |

If you want to call extra variants in data with R10 config, please manually specify the Clair3 model file with `-m` or `--model`.


Artex full parameters:
```
Usage: artex [OPTIONS]

Options:
  -i, --input TEXT        Path to the Artic pipeline output directory
  -o, --output TEXT       Output directory
  -p, --prefix TEXT       Output prefix
  -c, --config TEXT       Basecalling configuration, config which have
                          predownloaded Clair3 model included: [R9G2, R9G4, R9G6]
  -w, --work TEXT         Working directory, for storing intermediate results
  -r, --ref TEXT          Reference file
  -m, --model TEXT        Path to clair3 model
  -t, --threads INTEGER   Parallel threads for Clair3
  --chunk_size INTEGER    Chuck size for Clair3
  --min_coverage INTEGER  Minimum coverage required to call a variant in Clair3
  --test                  Run test for the installation environment
  --verbose               Verbose mode, output the process of Artex
  --version               Show the version and exit.
  --help                  Show this message and exit.
```

## Example and test
### end-to-end test
We provide an `end_to_end_test.sh` test file in [./tests](./tests). After successfully installing the software, you can download and run the test to verify `Artex` functionality.
```
# artex --verbose -i ${artic output folder} -o ${artex output folder} -c ${config};
artex --verbose -i ./ERR5398250 -o ./ERR5398250_artex -c R9G4;
```
After running the end-to-end test, the output directory contains the following files and folders:
| file/folder name | Description | Category |
|:---:|:---:|:---:|
| `artic.fail.vcf.gz` | compressed FAIL variant reported by artic | Intermediate result |
| `artic.fail.vcf.gz.tbi` | Indedx file for compressed FAIL variant reported by artic | Intermediate result |
| `clair3` | Clair3 output for re-variant calling | Intermediate result |
| `for_merge` | Contains `0000.vcf`, which includes extra variants called by Artex | Intermediate result |
| `sample.artex.vcf.gz` | Final Artex results, combining extra variants called by Artex with PASS variants reported by Artic | Final result |




## Performance
As a reference, the end-to-end test mentioned above completes in 21 seconds on an AMD EPYC 7K62 processor (using 12 threads).




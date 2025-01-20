# Artex - **Art**ic **ex**tension

## Introduction
Artex is a software tool designed for re-calling variants at low-coverage or low-quality sites which are often not considered or filtered out in the original `ARTIC pipeline`. It utilizes the amplicon mode of `Clair3` for re-variant calling. Variants are recovered by intersecting the `FAIL.vcf` results from the `Artic pipeline` with the Clair3 output. Those variants can be of great importance, which can exist in the `S-gene`, such as the example provided in `tests/ERR5398250`.


## Installation 
Artex is compatible with most modern operating system that support a Python environment. However, only the _Linux_ operating system has been tested, and its use is recommended. To install:
```bash
conda create -n artex python=3.9;
conda install artex;
```


## Installation test
After installation, you can test the environment with:
```bash
artic --test;
```


## Usage
Three parameters are mandatory:
| Parameters | Explanation |
|:---:|:---:|
|`-i` / `--input`  | Path to the Artic pipeline output directory |
|`-o` / `--output` | Output directory |
|`-c` / `--config` | Basecalling configuration, predcited by LongBow, options: [R9G2, R9G4, R9G6] |

If you want to call extra variant in data with R10 config, please manually specify the Clair3 model file with `-m` or `--model`.


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
We provide an example and `end-to-end` test file in `./test`. You can try it after successful installation.

```bash
cd ./tests;
bash end_to_end_test.sh;
```


## Performance
For each sample, Artex is expected to finish analysis of extra variant from the results of Artic pipeline within minutes using the default 12 threads.

As a reference, for the `end-to-end` test above, the runtime on an AMD EPYC-7K62 is 21 seconds.




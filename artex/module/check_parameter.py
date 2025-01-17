import os
import sys
import logging
from module.test_env import test_env
import math

def check_parameter(input, output, prefix, config, work, ref, model, threads, chunk_size, min_coverage, test):
    
    # test environment
    if test:
        logging.info("Checking environment")
        test_env()
        sys.exit(0)
    
    
    # check paramters
    if (not input) or (not output):
        if (not input):
            logging.error("-i / --input parameter is not set")
            raise click.UsageError(r"Error: -i / --input parameter is required")
        if (not output):
            logging.error("-o / --output parameter is not set")
            raise click.UsageError(r"Error: -o / --output parameter is required")

    if chunk_size < 0:
        logging.error("--chunk_size must larger than 0")
        sys.exit(1)
    else:
        chunk_size = math.ceil(chunk_size)

    if threads < 0:
        logging.error("-t or --threads must larger than 0")
        sys.exit(1)
    else:
        threads = math.ceil(threads)

    if min_coverage < 0:
        logging.error("--min-coverage must larger than 0")
        sys.exit(1)
    else:
        min_coverage = math.ceil(min_coverage)

    if not(model) and not(config):
        logging.error("Either --config or --model must be specified")
        sys.exit(1)

    if model and config:
        logging.error("--config and --model cannot be used together")
        sys.exit(1)

    # clean parameters
    input = os.path.abspath(input)
    output = os.path.abspath(output)
    if not os.path.exists(output):
        logging.warning("Output directory does not existing, creating output directory")
        os.makedirs(output)

    if work == "SAME AS OUTPUT PATH":
        work = output
    else:
        work = os.path.abspath(work)
    

    if model:
        model = os.path.abspath(model)
    
    if config:
        if config not in {"R9G2", "R9G4", "R9G6"}:
            raise click.UsageError(r"Error: -c / --config paramter must be in [R9G2, R9G4, R9G6], for other Clair3 model please manual specify the Clair3 model by --model")

    
    return (input, output, prefix, config, work, ref, model, threads, chunk_size, min_coverage)







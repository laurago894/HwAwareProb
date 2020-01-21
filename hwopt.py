import sys
import argparse
from PSDD_functions import PSDD_to_AC
from functions import scaling_search
import pruning_functions
import csv


def run(args):

    bench_name=args.inputBenchmark
    model_nums=args.models.split(',')

    #Seach through trade-off space
    scaling_search.search_tradeoff(bench_name, model_nums)



def main(argv=None):
    parser = argparse.ArgumentParser(description='Run the hardware-aware model optimization')
    parser.add_argument('inputBenchmark', help='Provide the name of the benchmark')
    parser.add_argument('-models', '--models', type=str, default=None,
                        help='Pre-trained PSDD models to use for the trade-off space search')
    parser.add_argument('-csi', '--csi', action='store_true', help='Consider sensor and feature costs')
    parser.add_argument('-ms', '--ms', action='store_true', help='Scale model complexity')
    parser.add_argument('-fs', '--fs', action='store_true', help='Scale sensor interfaces and prune model')
    parser.add_argument('-ps', '--ps', action='store_true', help='Scale floating point precision')



    args = parser.parse_args(argv)

    run(args)


if __name__ == "__main__":
    sys.exit(main())
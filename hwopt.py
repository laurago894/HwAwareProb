import sys
import argparse
from PSDD_functions import PSDD_to_AC
from functions import tradeoff_functions
import pruning_functions
import csv


def run(args):

    bench_name=args.inputBenchmark
    model_nums=args.models.split(',')


    for model_num in model_nums:

        print '\n\nNow in model  ', model_num, '...'

        ac_model=PSDD_to_AC.convert_psdd('models/' + bench_name + '/psdd/0-' + model_num + '.psdd', model_num, bench_name)

        tradeoff_functions.metric_est(bench_name, ac_model)



def main(argv=None):
    parser = argparse.ArgumentParser(description='Run the hardware-aware model optimization')
    parser.add_argument('inputBenchmark', help='Provide the name of the benchmark')
    parser.add_argument('-models', '--models', type=str, default=None,
                        help='Pre-trained PSDD models to use for the trade-off space search')


    args = parser.parse_args(argv)

    run(args)


if __name__ == "__main__":
    sys.exit(main())
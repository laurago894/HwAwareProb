from functions import tradeoff_functions, functions_util
from PSDD_functions import PSDD_to_AC

def search_tradeoff(bench_name,model_nums):

    #tradeoff_dict: collect accuracy, cost, features, bits (and sensors)
    tradeoff_dict={}
    cost_list=[]
    id_list=[]

    id_counter=0

    #load the dataset

    #Use training data to get Paretos because validation sets are often too small
    validation_set=functions_util.read_file('datasets/' + bench_name + '/' + bench_name +'.train.data')
    test_set=functions_util.read_file('datasets/' + bench_name + '/' + bench_name +'.test.data')


    feature_set=range(1,len(validation_set[0].split(',')))

    for model_num in model_nums:
        print '\n\nNow in model  ', model_num, '...'

        ac_model = PSDD_to_AC.convert_psdd('models/' + bench_name + '/psdd/0-' + model_num + '.psdd', model_num, bench_name)

        (acc, cost) = tradeoff_functions.metric_est(bench_name, ac_model,validation_set,feature_set,64, 0, 0)

        print acc
        print cost

        #(cost,accuracy,mod,feats,nb)
        tradeoff_dict[id_counter]=(cost,acc,model_num,feature_set,64)

        cost_list.append((cost,id_counter))

        id_counter+=1

        #Feature pruning routine

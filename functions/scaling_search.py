from functions import tradeoff_functions, functions_util
from PSDD_functions import PSDD_to_AC
from pruning_functions import feature_pruning

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
    class_num = len(validation_set[0].split(','))
    #What is the cost of the largest available AC?
    max_model=max(model_nums)

    ac_model = PSDD_to_AC.convert_psdd('models/' + bench_name + '/psdd/0-' + max_model + '.psdd', max_model, bench_name)

    (acc_baseline, cost_baseline) = tradeoff_functions.metric_est(bench_name, ac_model, validation_set, feature_set, 64, 0)

    for model_num in model_nums:
        print '\n\nNow in model  ', model_num, '...'

        ac_model = PSDD_to_AC.convert_psdd('models/' + bench_name + '/psdd/0-' + model_num + '.psdd', model_num, bench_name)

        (acc, cost) = tradeoff_functions.metric_est(bench_name, ac_model,validation_set,feature_set,64, 0)


        print 'Accuracy of full feeature set ', acc
        print 'Cost of full feature set ', cost

        #(cost,accuracy,mod,feats,nb)
        tradeoff_dict[id_counter]=(cost,acc,model_num,feature_set,64)

        cost_list.append((cost,id_counter))

        id_counter+=1



        #Feature pruning routine
        #Loop through features, check accuracy and cost after pruning each feature

        print 'Full feature set ', feature_set

        prunable_feature_set=[f for f in feature_set]

        selected_fs=[]


        while len(prunable_feature_set) > 1:

            cfs=[]
            for feat_prune in prunable_feature_set:
                candidate_feats=[f for f in prunable_feature_set if f!=feat_prune]
                (acc_ca, cost_ca) = tradeoff_functions.metric_est(bench_name, ac_model, validation_set, candidate_feats, 64, 0,featp=feat_prune)

                ncost = cost_ca / float(cost_baseline)

                #Options of cost function for feature selection
                # cf=acc_ca/ncost
                alpha = 0.001
                # cf=acc_ca/float(((1-alpha)*ncost) +alpha)
                cf = acc_ca - (alpha * ncost)

                cfs.append((cf,acc_ca,cost_ca,candidate_feats,feat_prune))

            winner=max(cfs)

            print 'Winner set ', winner
            #prune AC and reestimate cost
            #To add

            # (nodes, lmap_indeces, lmap_weights, lmap_type, lmap_belong, indicator_dict, literal_assign)
            content_ac = ac_model[0]
            lmap_id = ac_model[1]
            lmap_w = ac_model[2]
            lmap_t = ac_model[3]
            lmap_b = ac_model[4]
            indicator_dict = ac_model[5]
            variable_list = ac_model[6]

            (content_ac_pr, lmap_weights_pr, lmap_indeces_pr, lmap_pr, lmap_type_pr,
             indicator_dict_pr)= feature_pruning.ac_pruning(lmap_id, lmap_w, lmap_t, variable_list, lmap_b, indicator_dict, content_ac,
                                       winner[3]+[class_num], model_num)

            pruned_model=(content_ac_pr,lmap_indeces_pr,lmap_weights_pr,lmap_type_pr,indicator_dict_pr,variable_list)

            cost_ori=tradeoff_functions.cost_est((content_ac,[0]), 64)

            cost_pruned_model=tradeoff_functions.cost_est((content_ac_pr,[0]), 64)

            print 'The cost of the pruned model ', cost_pruned_model, 'original was ', cost_ori

            # metric_est(bench_name, model, dataset, observed_features, bits, sensor_cost, **kwargs):
            #
            #
            # # (nodes, lmap_indeces, lmap_weights, lmap_type, lmap_belong, indicator_dict, literal_assign)

            selected_fs.append(winner)

            tradeoff_dict[id_counter] = (winner[2],winner[1],model_num,winner[3],64)
            # cost_list.append((winner[2], id_counter))
            cost_list.append((cost_pruned_model, id_counter))

            id_counter+=1

            prunable_feature_set=[f for f in prunable_feature_set if f!=winner[4]]


        print selected_fs
        print tradeoff_dict

        print sorted(cost_list)







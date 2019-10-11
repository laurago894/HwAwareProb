from functions import functions_util, inference_fcns

def metric_est(bench_name,model):


    #(nodes, lmap_indeces, lmap_weights, lmap_type, lmap_belong, indicator_dict, literal_assign)
    content_ac=model[0]
    lmap_id=model[1]
    lmap_w=model[2]
    variable_list=model[6]


    validation_set=functions_util.read_file('datasets/' + bench_name + '/' + bench_name +'.train.data')
    test_set=functions_util.read_file('datasets/' + bench_name + '/' + bench_name +'.test.data')

    class_num = len(validation_set[0].split(','))
    thres=0.5

    NodesEv = [var for var in variable_list]
    obs_var_num = NodesEv
    obs_var_den = [ne for ne in NodesEv if ne != class_num]

    classes = [0, 1]

    # print 'Init weight...'
    init_weight = inference_fcns.init_weight(content_ac, lmap_id, lmap_w)

    operations_index, operation = inference_fcns.extract_operations(content_ac)

    #For verification purposes: w should be 1
    #wmc, w = inference_fcns.performWMC(operations_index, operation, init_weight, content_ac)
    #print w
from functions import functions_util, inference_fcns
import math, sys

def cost_est(model,bits,**kwargs):

    content_ac = model[0]

    cost_add_flt={64:32,32:16,16:8,8:4}
    cost_mult_flt={64:120,32:25,16:5,8:1}

    cost_reg={64:40,32:20,16:10,8:5}
    cost_sram={64:200,32:100,16:50,8:25}

    par_num = sum([1 for ac in content_ac if 'L' in ac]) #Number of parameters
    add_num = sum([1*len(ac.split(' '))-2-1+1 for ac in content_ac  if 'O' in ac]) #Number of multiplications
    mult_num = sum([1*len(ac.split(' '))-3-1+1 for ac in content_ac if 'A' in ac]) #Number of additions

    #Feature and cost sensor are 0 by default
    cost_sensors=0
    cost_features=0

    #Estimate savings from feature-pruning induced model reduction
    print '\n'
    if kwargs:
        if 'pruned_feature' in kwargs:

            #How much would we save if we pruned features in kwargs
            indicator_dict = model[5]
            variable_list = model[6]

            n_mult = len(indicator_dict[variable_list[kwargs['pruned_feature']] + '_0']) + len(
                indicator_dict[variable_list[kwargs['pruned_feature']] + '_1'])
            n_add = n_mult / 2
            n_params = len(indicator_dict[variable_list[kwargs['pruned_feature']] + '_0']) + len(
                indicator_dict[variable_list[kwargs['pruned_feature']] + '_1'])

            saved_mul=n_mult
            saved_add=n_add
            saved_params=n_params

            par_num-=saved_params
            add_num-=saved_add
            mult_num-=saved_mul

            print 'Cost savings', saved_params, saved_mul, saved_add


        if 'sensor_dict' in kwargs:
            print 'Sensor costs!'
            sens_dict=kwargs['sensor_dict']
            sensor_c = kwargs['max_cost']*0.1   #Sensor cost is 10% of most expensive AC comp. cost
            feature_set=kwargs['feature_set']

            sensor_occurrence = [sens_dict[f] for f in feature_set if f in feature_set] #Which sensors are active?

            nsensors = len(set(sensor_occurrence))
            print set(sensor_occurrence)
            print 'Sensors number ', nsensors

            cost_sensors=sensor_c*nsensors

            cost_features=len(feature_set)*((30*cost_add_flt[32])+(30*cost_mult_flt[32])) #Each feature requires 30 MAC, features are extracted at 32 bits


    out_cost=(add_num * cost_add_flt[bits]) + (mult_num * cost_mult_flt[bits]) + ((add_num + mult_num) * cost_reg[bits] ) + (par_num * cost_sram[bits])+cost_sensors+cost_features

    #Return list with [total cost with sensors and features, total cost without sensors or features, sensor cost, feature cost]
    return out_cost



def accuracy_estimation(validation_set,indicator_dict,variable_list,obs_var_den,init_weight,
                        operations_index,operation,content_ac,classes,obs_var_num,thres,**kwargs):

    correct_count=0
    all_ratios=[]

    for test in validation_set:

        if test:
            observation = [int(t) for t in test.split(',')]

            gt = observation[-1]

            #Set indicator values according to observation
            position_neg_den = [indicator_dict[variable_list[var] + '_' + str(value)] for value, var in
                                zip(observation, variable_list) if var in obs_var_den ]

            psn_den = [pos for position in position_neg_den for pos in position]

            init_weight_den = [w for w in init_weight]

            for psden in psn_den:
                init_weight_den[psden] = 0

            wmc_den, w_den= inference_fcns.performWMC(operations_index, operation, init_weight_den,content_ac)

            w_den+= sys.float_info.min  #Avoid division by 0

            #Collect num/den ratio
            ratios = []
            nn=[]

            for classv in classes:

                # chnage observation value of class variable
                observation[-1] = classv
                position_neg_num = [indicator_dict[variable_list[var] + '_' + str(value)] for value, var in zip(observation, variable_list) if var in obs_var_num]

                psn_num = [pos for position in position_neg_num for pos in position]


                init_weight_num = [w for w in init_weight]

                for psnum in psn_num:
                    init_weight_num[psnum] = 0


                wmc_num, w_num= inference_fcns.performWMC(operations_index, operation, init_weight_num,content_ac)

                nn.append(w_num)
                rati = w_num / w_den

                ratios.append(rati)
            all_ratios.append(ratios)

            conditions = [loc for loc, num in enumerate(ratios) if num >= thres]

            if len(conditions) == 1:
                if int(conditions[0]) == gt:
                    correct_count += 1
            elif len(conditions) > 1:
                if int(conditions.index(max(conditions))) == gt:
                    correct_count += 1

    accuracy=float(correct_count) / (len(validation_set))

    return accuracy

def metric_est(bench_name,model,dataset,observed_features,bits,sensor_cost,**kwargs):


    content_ac=model[0]

    ce=cost_est(content_ac,64)
    lmap_id=model[1]
    lmap_w=model[2]
    indicator_dict = model[5]
    variable_list=model[6]


    class_num = len(dataset[0].split(','))
    thres=0.5

    NodesEv = observed_features+[class_num]

    obs_var_num = NodesEv
    obs_var_den = observed_features


    classes = [0, 1]

    # Initialize weight vector
    init_weight = inference_fcns.init_weight(content_ac, lmap_id, lmap_w)

    operations_index, operation = inference_fcns.extract_operations(content_ac)

    #To verify WMC: w should be 1
    # wmc, w = inference_fcns.performWMC(operations_index, operation, init_weight, content_ac)
    # print 'w is ', w

    acc=accuracy_estimation(dataset, indicator_dict, variable_list, obs_var_den, init_weight,
                        operations_index, operation, content_ac, classes, obs_var_num, thres)

    if kwargs:
        if 'featp' in kwargs:
            cost=cost_est(model,bits,pruned_feature=kwargs['featp'])
    elif not kwargs:
        cost = cost_est(model, bits)


    # print 'acc is ', acc
    # print 'cost is ', cost

    return(acc,cost)
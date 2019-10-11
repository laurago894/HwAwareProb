import csv
import math
import os
from functions import functions_util


#transform a parameter node into an ac with two mults. and one add.
def T_node(node,max_node,offset,operation_dict,variable_list,indicator_dict,test,nodes,lmap_indeces,lmap_weights,lmap_type,lmap_belong):
    #What variable does it correpond to?
    var_literal=variable_list[int(node[3])]

    #Generate a list with 7 spaces for the sub-circuit
    sub_ac=[None]*7
    #Generate list with the 4 lmap leaves involved
    sub_lmap_ind=[None]*4
    sub_lmap_w=[None]*4
    sub_lmap_t = [None] * 4
    sub_lmap_b = [None] * 4

    test.append('x')

    ######## First add all involved parameters to sub ac

    #Node 1: the input parameter, name it with its id
    sub_ac[0]='L ' + node[1]
    sub_lmap_ind[0]= int(node[1]) #index is the one already provided
    sub_lmap_w[0]=math.exp(float(node[-1])) # param value provided in psdd
    sub_lmap_t[0]='param'
    sub_lmap_b[0]=var_literal

    #Node 2: the indicator for the input parameter
    max_node+=1
    sub_ac[1]='L ' + str(max_node) #use max node number
    sub_lmap_ind[1]= max_node
    sub_lmap_w[1]=1.0 # weigt is 1 for now
    sub_lmap_t[1]='ind'
    sub_lmap_b[1]=var_literal
    indicator_dict[var_literal+'_0'].append(offset+1)
    # print 'Adding ', offset+1, ' to indicator dict'

    #Node 3: the 1-parameter value
    max_node+=1
    sub_ac[2]='L ' + str(max_node) #use max node number
    sub_lmap_ind[2]= max_node
    sub_lmap_w[2]=1.0-math.exp(float(node[-1])) # 1-parameter
    sub_lmap_t[2] = 'param'
    sub_lmap_b[2] = var_literal

    #Node 4: the indicator for the negated input parameter
    max_node+=1
    sub_ac[3]='L ' + str(max_node) #use max node number
    sub_lmap_ind[3]= max_node
    sub_lmap_w[3]=1.0 # weigt is 1 for now
    sub_lmap_t[3] = 'ind'
    sub_lmap_b[3] = var_literal
    indicator_dict[var_literal + '_1'].append(offset + 3)
    # print 'Adding ', offset+3, ' to indicator dict'


######## Add operations

    #Node 5: The multiplication of parameter and its indicator
    sub_ac[4]='A 2 ' + str(0+offset) + ' ' + str(1+offset)

    #Node 6: The multiplication of not parameter and its indicator
    sub_ac[5]='A 2 ' + str(2+offset) + ' ' + str(3+offset)

    #Node 7: Addition of multipliers
    sub_ac[6]='O 2 2 ' + str(4+offset) + ' ' + str(5+offset)
    out_sum_location=6+offset

    #indicate that instead of looking for the leaf param you should look for the output addition
    operation_dict.update({node[1]:out_sum_location})

    offset+=7

    # print 'Indicator dict is ', indicator_dict

    [nodes.append(no) for no in sub_ac]
    [lmap_indeces.append(li) for li in sub_lmap_ind]
    [lmap_weights.append(lw) for lw in sub_lmap_w]
    [lmap_type.append(lw) for lw in sub_lmap_t]
    [lmap_belong.append(lw) for lw in sub_lmap_b]

    # print 'Checking for indicators in AC,',sub_ac[1], ' is ', [nodes[id] for id in indicator_dict[var_literal + '_0']]
    # print 'Checking for indicators in AC,', sub_ac[3], ' is ', [nodes[id] for id in indicator_dict[var_literal + '_1']]

    return sub_ac,sub_lmap_ind,sub_lmap_w,max_node,offset,operation_dict


def L_node(node, offset, operation_dict,variable_list,indicator_dict,nodes,lmap_indeces,lmap_weights,lmap_type,lmap_belong):
    var_literal = variable_list[abs(int(node[3]))]



    # Generate a list with 1 space for the sub-circuit
    sub_ac = [None] * 1
    # Generate list with the 4 lmap leaves involved
    sub_lmap_ind = [None] * 1
    sub_lmap_w = [None] * 1
    sub_lmap_t = [None] * 1
    sub_lmap_b = [None] * 1

    # Node 1: the input parameter, name it with its id
    sub_ac[0] = 'L ' + node[1]
    sub_lmap_ind[0]= int(node[1])
    sub_lmap_w[0]=1.0 # weigt is 1 for now
    sub_lmap_t[0]='ind'
    sub_lmap_b[0] = var_literal

    out_sum_location=offset

    #indicate that instead of looking for the leaf param you should look for the output addition
    operation_dict.update({node[1]:out_sum_location})

    if (int(node[3]))>0:
        indicator_dict[var_literal + '_0'].append(offset)
    elif (int(node[3]))<0:
        indicator_dict[var_literal + '_1'].append(offset)

    offset+=1

    [nodes.append(no) for no in sub_ac]
    [lmap_indeces.append(li) for li in sub_lmap_ind]
    [lmap_weights.append(lw) for lw in sub_lmap_w]
    [lmap_type.append(lw) for lw in sub_lmap_t]
    [lmap_belong.append(lw) for lw in sub_lmap_b]


    return sub_ac,sub_lmap_ind,sub_lmap_w,offset,operation_dict


def D_node(node,max_node,offset,operation_dict,nodes,lmap_indeces,lmap_weights,lmap_type,lmap_belong):


    factor_num=int(node[3])

    if factor_num==1: #if there is only one factor there is no need for an add node
        sub_ac=[None]*2
        sub_lmap_ind=[None]*1
        sub_lmap_w=[None]*1
        sub_lmap_t = [None] * 1
        sub_lmap_b = [None] *1

    else: #if there is more than one factor we have to add them at the end
        sub_ac=[None]*(factor_num+factor_num+1)
        sub_lmap_ind=[None]*(factor_num)
        sub_lmap_w=[None]*(factor_num)
        sub_lmap_t = [None] * (factor_num)
        sub_lmap_b = [None] * (factor_num)


    off=3
    and_locs=[]


    for factor in range(factor_num):
        f_index=node[4+(factor*off):6+(factor*off)]
        locations=[operation_dict[fi] for fi in f_index]
        parameter=node[6+(factor*off)]


        #Add parameter
        max_node+=1
        sub_ac[factor+(1*factor)]='L ' + str(max_node)
        sub_lmap_ind[factor] = int(max_node)  # index is the one already provided
        sub_lmap_w[factor] = math.exp(float(parameter))  # param value provided in psdd
        sub_lmap_t[factor]='param'
        sub_lmap_b[factor] = 'additional'
        # print 'New leaf is ', 'L ' + str(max_node), 'in', offset
        loc_leaf=offset
        offset+=1 #offset from inserting new leaf
        al=offset
        sub_ac[factor+1+(1*factor)]='A 2 ' + str(locations[0]) + ' ' + str(locations[1]) + ' ' + str(loc_leaf)

        offset+=1

        and_locs.append(al)

    if factor_num>1:
        st_or='O 2 2'
        for al in and_locs:
            st_or=st_or + ' ' + str(al)
        sub_ac[-1]=st_or
        out_loc=offset
        offset+=1
    else:
        out_loc=offset-1


    # out_loc=and_locs[-1]
    operation_dict.update({node[1]:out_loc})

    [nodes.append(no) for no in sub_ac]
    [lmap_indeces.append(li) for li in sub_lmap_ind]
    [lmap_weights.append(lw) for lw in sub_lmap_w]
    [lmap_type.append(lw) for lw in sub_lmap_t]
    [lmap_belong.append(lw) for lw in sub_lmap_b]

    return sub_ac, sub_lmap_ind, sub_lmap_w, max_node, offset, operation_dict



    ######## First add parameter to sub ac





def convert_psdd(inputFile,model_num,benchmark_name):


    test=[]

    content_psdd=functions_util.read_file(inputFile)

    psdd_full=[con.split() for con in content_psdd if con[0]!='c' and con[0]!='p']

    variable_nums=[int(ps[3]) if ps[0] is 'T' else int(ps[3])  for ps in psdd_full if ps[0] is not 'D']

    var_list=list(set([abs(var) for var in variable_nums]))


    letters = ['A', 'B', 'C', 'D','E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P','Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    current = letters
    new = []
    while len(new) < len(var_list):
        current = [s + 'n' for s in current]
        new = new + current

    print 'Converting PSDD in '+ inputFile +' to AC...'

    alphabet_lit=new


    literal_assign = {}


    [literal_assign.update({ii + 1: alphabet_lit[ii]}) for ii in range(len(var_list))]

    [literal_assign.update({ii + 1: 'F'+str(ii+1)}) for ii in range(len(var_list) )]

    literal_assign[len(var_list)]='CL'

    indicator_dict={}
    [indicator_dict.update({literal_assign[ii]+'_0':[]}) for ii in literal_assign]
    [indicator_dict.update({literal_assign[ii] + '_1': []}) for ii in literal_assign]

    # print 'ind dict ', indicator_dict
    offset=0
    operation_dict={}
    max_node=max([int(ps[1]) for ps in psdd_full]) #int(psdd_full[-1][1])
    # print 'max node is ', max_node
    nodes=[]
    lmap_indeces=[]
    lmap_weights=[]
    lmap_type=[]
    lmap_belong=[] #What variable is related to this param or ind


    for node in psdd_full:

        if node[0] is 'T':
            sub_ac, sub_lmap_ind, sub_lmap_w, max_node, offset, operation_dict=T_node(node,max_node,offset,operation_dict,literal_assign,indicator_dict,test
                                                                                      ,nodes,lmap_indeces,lmap_weights,lmap_type,lmap_belong)


        if node[0] is 'L':
            sub_ac, sub_lmap_ind, sub_lmap_w, offset, operation_dict=L_node(node,offset,operation_dict,literal_assign,indicator_dict,nodes,lmap_indeces,
                                                                            lmap_weights,lmap_type,lmap_belong)


        if node[0] is 'D':
            sub_ac, sub_lmap_ind, sub_lmap_w, max_node, offset, operation_dict = D_node(node, max_node, offset,
                                                                                        operation_dict, nodes,
                                                                                        lmap_indeces,
                                                                                        lmap_weights, lmap_type,
                                                                                        lmap_belong)
############################################## Save new ac and lmap files st they can be used later

    empty = []

    for var in indicator_dict:
        if not indicator_dict[var]:
            empty.append(var)

    [indicator_dict.pop(em) for em in empty]


    out_dir='models/' + benchmark_name + '/ac/'

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    fname_ac=out_dir + 'psdd_ac_'+ model_num +'.txt'

    fname_lmi = out_dir + 'lmap_ind_'+ model_num +'.txt'
    fname_lmw = out_dir + 'lmap_we_'+ model_num +'.txt'
    fname_lmt = out_dir + 'lmap_type_' + model_num + '.txt'
    fname_lmb = out_dir + 'lmap_belong_' + model_num + '.txt'

    fname_ind_dict = out_dir + 'indicator_dict_' + model_num + '.csv'
    fname_lit_assign = out_dir + 'literal_assign_' + model_num + '.csv'

    print 'Writing ac models to ', out_dir

    with open(fname_ac,'w') as fac:
        for ac in nodes:
            fac.write(ac+'\n')
    fac.close()

    with open(fname_lmi, 'w') as lm:
        for acd in lmap_indeces:
            lm.write(str(acd) + '\n')
    lm.close()

    with open(fname_lmw, 'w') as lm:
        for acd in lmap_weights:
            lm.write(str(acd) + '\n')
    lm.close()


    with open(fname_lmt, 'w') as lm:
        for acd in lmap_type:
            lm.write(str(acd) + '\n')
    lm.close()

    with open(fname_lmb, 'w') as lm:
        for acd in lmap_belong:
            lm.write(str(acd) + '\n')
    lm.close()


    wid=csv.writer(open(fname_ind_dict,'w'))
    for key,val in indicator_dict.items():
        valst = ','.join([str(v) for v in val])
        wid.writerow([key, valst])

    was=csv.writer(open(fname_lit_assign,'w'))
    for key,val in literal_assign.items():
        valst=','.join([str(v) for v in val])
        was.writerow([key,valst])


    return nodes,lmap_indeces,lmap_weights,lmap_type,lmap_belong,indicator_dict,literal_assign


########################## Generate a lmap (needed when pruning)
def generate_lmap(lmap_indeces,lmap_weights,lmap_type,variable_list,lmap_belong,indicator_dict,content_ac):

    leaf_locations = {}
    [leaf_locations.update({ac: aci}) for aci, ac in enumerate(content_ac) if 'L' in ac]

    lmap=[]

    location_ind_type={}
    [location_ind_type.update({loc:indi})  for indi in indicator_dict for loc in indicator_dict[indi]]

    for lmi,lmw,lmb,lmt in zip(lmap_indeces,lmap_weights,lmap_belong,lmap_type):

        if lmt=='ind':
            type=location_ind_type[leaf_locations['L '+str(lmi)]]
            lmap.append('cc$I$' + str(lmi) +'$1.0$+$'+ str(lmb) +'$' + type[type.index('_')+1:])
        elif lmt=='param':
            lmap.append('cc$C$'+ str(lmi) + '$'+ str(lmw) + '$+$')


    return lmap






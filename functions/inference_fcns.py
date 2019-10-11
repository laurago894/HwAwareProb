import operator

def prod(factors):
    return reduce(operator.mul, factors, 1)


def init_weight(content_ac,content_lmap_parsed_indeces,content_lmap_parsed_weights):
    weight_ac = [None] * len(content_ac)
    for i, ac in enumerate(content_ac):
        if ac[0] == 'L':
            index = int(ac[2:len(ac)])
            # index_weight = indices(content_lmap_parsed_indeces, lambda x: x == index)
            index_weight=[ii for ii,con in enumerate(content_lmap_parsed_indeces) if con==index]
            weight_ac[i] = content_lmap_parsed_weights[index_weight[0]]

        else:
            weight_ac[i] = 0
    return (weight_ac)


def extract_operation_numbers(content):
    # spaces = indices(content, lambda x: x.isspace())
    spaces=[ii for ii,con in enumerate(content) if con.isspace()]
    ex_op=[]
    if content[0] == 'A':
        for sp in range(len(spaces) - 1):
            if sp == len(spaces) - 2:
                ex_op.append(content[spaces[sp + 1] + 1:])
            else:
                ex_op.append(content[spaces[sp + 1] + 1:spaces[sp + 2]])
    else:
        for sp in range(len(spaces) - 2):
            if sp == len(spaces) - 3:
                ex_op.append(content[spaces[sp + 2] + 1:])
            else:
                ex_op.append(content[spaces[sp + 2] + 1:spaces[sp + 3]])
    return ex_op,spaces

def generate_operation_set(operations_index,content_ac):
    operation = [[] for _ in range(len(operations_index))]
    for i, op in enumerate(operations_index):
        content=content_ac[operations_index[i]]
        (extracted_op,sp)=extract_operation_numbers(content)
        operation[i]=extracted_op
    return operation

def extract_operations(args):
    k=1
    for i, ac in enumerate(args):
        if ac[0]=='L':
            k=k+1
    operations_index=[0]*(len(args)-k+1)
    operation_wmc=[0]*(len(args))
    j=0
    for i, ac in enumerate(args):
        res=[]
        if ac[0] != 'L':
            operations_index[j]=i
            j=j+1
            (op_ex, spaces) = extract_operation_numbers(ac)

            if ac[0]=='O':
                res.append(ac[0:spaces[2]])
            if ac[0]=='A':
                res.append(ac[0:spaces[1]])
            lis=list(map(int, op_ex))
            for l in lis:
                res.append(l)
            operation_wmc[i]=res
        else:
            operation_wmc[i]=ac
    operation=generate_operation_set(operations_index,args)

    return operations_index, operation



def performWMC(operations_index, operation, weight_ac_original, content_ac):

    weight_ac=[w for w in weight_ac_original]

    for i, op in enumerate(operations_index):

        temp = []
        for j in range(len(operation[i])):
            temp.append(weight_ac[int(operation[i][j])])

        if 'A' in content_ac[operations_index[i]][0]:
            weight_ac[operations_index[i]] = prod(temp)

        elif 'O' in content_ac[operations_index[i]][0]:
            weight_ac[operations_index[i]] = sum(temp)


    if content_ac[len(content_ac) - 1][0] != 'L':
        wc = weight_ac[len(content_ac) - 1]
    else:
        for w in range(len(content_ac) - 1, -1, -1):
            if content_ac[w][0] != 'L':
                wc = weight_ac[w]
                break

    return (weight_ac, wc)
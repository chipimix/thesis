import csv

from numpy import genfromtxt


#    data_cleaner(arg,'toni','musi')

# arg=numero da medicao; arg1=nome do macaco; arg2=medi/musi/puzz/movi

def data_cleaner(arg, arg1, arg2):
    my_data = genfromtxt('readings/' + arg1 + '/' + arg2 + '/' + arg1 + '_' + arg2 + '_' + arg + '.csv', delimiter=',')

    # aN_data (|N=[0,5]) is a list of length 700000 whose elements vary from 0 to 1018,
    a0_data = my_data[0::6].flatten().tolist()
    a1_data = my_data[1::6].flatten().tolist()
    a2_data = my_data[1::6].flatten().tolist()
    a3_data = my_data[1::6].flatten().tolist()
    a4_data = my_data[1::6].flatten().tolist()
    a5_data = my_data[1::6].flatten().tolist()

    # print "SIZE B4 CLEAN: ",len(a0_data)

    # a0_u_count=0 #saturated signal frequency - upper limit: >=1018
    # a0_l_count=0 #saturated signal frequency - lower limit: 0
    # a1_u_count=0
    # a1_l_count=0

    # for d in a0_data:
    #    if d==0:
    #        a0_l_count +=1
    #    elif d>= 1018:
    #        a0_u_count +=1

    count = 0
    aux = []
    indices = []

    for idx, val in enumerate(a0_data):
        if val == 0 or val >= 1018:
            count += 1
            aux.append(idx)
        else:
            if count >= 200:
                # print "single saturation's size= ", len(aux), aux
                indices += aux
            count = 0
            aux = []

    for idx, val in enumerate(a1_data):
        if val == 0 or val >= 1018:
            count += 1
            aux.append(idx)
        else:
            if count >= 200:
                # print "single saturation's size= ", len(aux), aux
                indices += aux
            count = 0
            aux = []

    a0_out = [i for j, i in enumerate(a0_data) if j not in indices]
    a1_out = [i for j, i in enumerate(a1_data) if j not in indices]

    # print "a0 SIZE AFTER CLEAN: ",len(a0_out)
    # print "a1 SIZE AFTER CLEAN: ",len(a1_out)

    with open('readings/' + arg1 + '/' + arg2 + '/' + arg1 + '_' + arg2 + '_' + arg + '_no_sat.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows([a0_out])
        writer.writerows([a1_out])
        writer.writerows([a2_data][:len(a0_out)])
        writer.writerows([a3_data][:len(a0_out)])
        writer.writerows([a4_data][:len(a0_out)])
        writer.writerows([a5_data][:len(a0_out)])

    print("readings/" + arg1 + "/" + arg2 + "/" + arg1 + "_" + arg2 + "_" + arg + "_no_sat.csv")


def data_cleaner2(arg, arg1, arg2):
    my_data = genfromtxt('readings/' + arg1 + '/' + arg1 + '/' + arg1 + '_' + arg2 + '_' + arg + '.csv', delimiter=',')

    # aN_data (|N=[0,5]) is a list of length 700000 whose elements vary from 0 to 1018,
    a0_data = my_data[0::6].flatten().tolist()
    a1_data = my_data[1::6].flatten().tolist()
    a2_data = my_data[1::6].flatten().tolist()
    a3_data = my_data[1::6].flatten().tolist()
    a4_data = my_data[1::6].flatten().tolist()
    a5_data = my_data[1::6].flatten().tolist()

    # print "SIZE B4 CLEAN: ",len(a0_data)

    # a0_u_count=0 #saturated signal frequency - upper limit: >=1018
    # a0_l_count=0 #saturated signal frequency - lower limit: 0
    # a1_u_count=0
    # a1_l_count=0

    # for d in a0_data:
    #    if d==0:
    #        a0_l_count +=1
    #    elif d>= 1018:
    #        a0_u_count +=1

    count = 0
    aux = []
    indices = []

    for idx, val in enumerate(a0_data):
        if val == 0 or val >= 1018:
            count += 1
            aux.append(idx)
        else:
            if count >= 100:
                # print "single saturation's size= ", len(aux), aux
                indices += aux
            count = 0
            aux = []

    for idx, val in enumerate(a1_data):
        if val == 0 or val >= 1018:
            count += 1
            aux.append(idx)
        else:
            if count >= 100:
                # print "single saturation's size= ", len(aux), aux
                indices += aux
            count = 0
            aux = []

    a0_out = [i for j, i in enumerate(a0_data) if j not in indices]
    a1_out = [i for j, i in enumerate(a1_data) if j not in indices]

    # print "a0 SIZE AFTER CLEAN: ",len(a0_out)
    # print "a1 SIZE AFTER CLEAN: ",len(a1_out)

    with open('readings/' + arg1 + '/' + arg2 + '/' + arg1 + '_' + arg2 + '_' + arg + '_no_sat.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows([a0_out])
        writer.writerows([a1_out])
        writer.writerows([a2_data][:len(a0_out)])
        writer.writerows([a3_data][:len(a0_out)])
        writer.writerows([a4_data][:len(a0_out)])
        writer.writerows([a5_data][:len(a0_out)])

    print("readings/" + arg1 + "/" + arg2 + "/" + arg1 + "_" + arg2 + "_" + arg + "_no_sat.csv")


file_list = ['5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22',
             '23', '24', '25']
file_list_ze = ['3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '21',
                '22', '23', '24', '25']

for arg in file_list:
    data_cleaner(arg, 'toni', 'musi')
    data_cleaner(arg, 'toni', 'movi')
    data_cleaner(arg, 'toni', 'puzz')
    print("---- TONI OK ----")
    data_cleaner(arg, 'costa', 'musi')
    data_cleaner(arg, 'costa', 'movi')
    data_cleaner(arg, 'costa', 'puzz')
    print("---- COSTA OK ----")
    # ZE MOVI,MUSI,PUZZ FALTA 20, VAI DO 3 AO 25
for arg in file_list_ze:
    data_cleaner(arg, 'ze', 'musi')
    data_cleaner(arg, 'ze', 'movi')
    data_cleaner(arg, 'ze', 'puzz')

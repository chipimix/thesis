import csv, numpy

from numpy import genfromtxt

#    data_cleaner(arg,'toni','musi')


#v1: if noise found of size at least arg ms, removes noise
#arg=numero da medicao; arg1=nome do macaco; arg2=medi/musi/puzz/movi; arg3=min noise duration to remove

def data_cleaner_v1(arg,arg1,arg2,arg3):
    my_data = genfromtxt('readings/'+arg1+'/'+arg2+'/'+arg1+'_'+arg2+'_'+arg+'.csv', delimiter=',')

    #aN_data (|N=[0,5]) is a list of length 700000 whose elements vary from 0 to 1018,
    a0_data = my_data[0::6].flatten().tolist()
    a1_data = my_data[1::6].flatten().tolist()
    a2_data = my_data[2::6].flatten().tolist()
    a3_data = my_data[3::6].flatten().tolist()
    a4_data = my_data[4::6].flatten().tolist()
    a5_data = my_data[5::6].flatten().tolist()


    #print "SIZE B4 CLEAN: ",len(a0_data)

    #a0_u_count=0 #saturated signal frequency - upper limit: >=1018
    #a0_l_count=0 #saturated signal frequency - lower limit: 0
    #a1_u_count=0
    #a1_l_count=0

    #for d in a0_data:
    #    if d==0:
    #        a0_l_count +=1
    #    elif d>= 1018:
    #        a0_u_count +=1

    count = 0
    aux = []
    indices = []

    for idx, val in enumerate(a0_data):
        if val == 0 or val >=1018:
            count+=1
            aux.append(idx)
        else:
            if count>=arg3:
                #print "single saturation's size= ", len(aux), aux
                indices+=aux
            count=0
            aux = []

    for idx, val in enumerate(a1_data):
        if val == 0 or val >=1018:
            count+=1
            aux.append(idx)
        else:
            if count>=arg3:
                #print "single saturation's size= ", len(aux), aux
                indices+=aux
            count=0
            aux = []

    a0_out = [i for j, i in enumerate(a0_data) if j not in indices]
    a1_out = [i for j, i in enumerate(a1_data) if j not in indices]

    #print "SIZE AFTER CLEANING NOISE: a0=",len(a0_out)," =a1= ",len(a1_out)

    fft_a0=numpy.square(numpy.absolute(numpy.fft.rfft(a0_out)))/1000
    fft_a1=numpy.square(numpy.absolute(numpy.fft.rfft(a1_out)))/1000



    csv_file = file('readings/'+arg1+'/'+arg2+'/'+arg1+'_'+arg2+'_'+arg+'_clean.csv', 'a')
    numpy.savetxt(csv_file, [fft_a0], delimiter=",", fmt="%.3e")
    numpy.savetxt(csv_file, [fft_a1], delimiter=",", fmt="%.3e")
    numpy.savetxt(csv_file, [a2_data], delimiter=",")
    numpy.savetxt(csv_file, [a3_data], delimiter=",")
    numpy.savetxt(csv_file, [a4_data], delimiter=",")
    numpy.savetxt(csv_file, [a5_data], delimiter=",")

    print("readings/"+arg1+"/"+arg2+"/"+arg1+"_"+arg2+"_" +arg+"_clean.csv")


#v1: if noise found of size at least arg ms, discards corresponding second
#arg=numero da medicao; arg1=nome do macaco; arg2=medi/musi/puzz/movi; arg3=min noise duration to remove
def data_cleaner_v2(arg,arg1,arg2,arg3):
    my_data = genfromtxt('readings/'+arg1+'/'+arg2+'/'+arg1+'_'+arg2+'_'+arg+'.csv', delimiter=',')

    #aN_data (|N=[0,5]) is a list of length 700000 whose elements vary from 0 to 1018,

    a0_data = my_data[0::6]
    a1_data = my_data[1::6]
    a2_data = my_data[2::6].flatten().tolist()
    a3_data = my_data[3::6].flatten().tolist()
    a4_data = my_data[4::6].flatten().tolist()
    a5_data = my_data[5::6].flatten().tolist()



    indices = []
    idx = 0

    for arr in a0_data:
        count = 0
        for num in arr:
            if num == 0 or num >= 1018:
                count += 1
            elif count >= arg3:
                indices.extend([idx])
                break
        idx += 1

    idx = 0
    for arr in a1_data:
        count = 0
        for num in arr:
            if num == 0 or num >= 1018:
                count += 1
            elif count >= arg3:
                indices.extend([idx])
                break
        idx += 1

    aux=0
    for num in list(set(indices)):
        a0_data=numpy.delete(a0_data,(num-aux),0)
        a1_data=numpy.delete(a1_data,(num-aux),0)
        aux+=1
    # print a0_data.shape
    # print a1_data.shape
    fft_a0=numpy.square(numpy.absolute(numpy.fft.rfft(a0_data.flatten())))/1000
    fft_a1=numpy.square(numpy.absolute(numpy.fft.rfft(a1_data.flatten())))/1000


    csv_file = file('readings/'+arg1+'/'+arg2+'/'+arg1+'_'+arg2+'_'+arg+'_clean.csv', 'a')
    numpy.savetxt(csv_file, [fft_a0], delimiter=",", fmt="%.3e")
    numpy.savetxt(csv_file, [fft_a1], delimiter=",", fmt="%.3e")
    numpy.savetxt(csv_file, [a2_data], delimiter=",", fmt="%d")
    numpy.savetxt(csv_file, [a3_data], delimiter=",", fmt="%d")
    numpy.savetxt(csv_file, [a4_data], delimiter=",", fmt="%d")
    numpy.savetxt(csv_file, [a5_data], delimiter=",", fmt="%d")

file_list = ['5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25']
file_list_ze_medi = ['3','4','5','6','7','8','9','10','11','12','13','15','16','17','18','19','21','22','23','24','25']
file_list_ze_else=['3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','21','22','23','24','25']

for arg in file_list:
    data_cleaner_v2(arg, 'toni', 'musi',10)
    data_cleaner_v2(arg, 'toni', 'movi',10)
    data_cleaner_v2(arg, 'toni', 'puzz',10)
    data_cleaner_v2(arg, 'costa', 'musi',10)
    data_cleaner_v2(arg, 'costa', 'movi',10)
    data_cleaner_v2(arg, 'costa', 'puzz',10)
print("---- COSTA & TONI OK ----")
    # ZE MOVI,MUSI,PUZZ FALTA 20, VAI DO 3 AO 25
for arg in file_list_ze_else:
    data_cleaner_v2(arg, 'ze', 'musi',10)
    data_cleaner_v2(arg, 'ze', 'movi',10)
    data_cleaner_v2(arg, 'ze', 'puzz',10)
print("---- COSTA & TONI OK ----")

for arg in file_list:
    data_cleaner_v2(arg, 'toni', 'medi',10)
    data_cleaner_v2(arg, 'costa', 'medi',10)
print("---- COSTA & TONI DONE ----")

for arg in file_list_ze_medi:
    data_cleaner_v2(arg, 'ze', 'medi',10)
print("---- ZE DONE ----")
import numpy as np
# # 保存1个后缀.npy
# # Save
# dict = {'num_i':-1,'filter_result_dict':{},'filter_commodity_dict':{}}
# np.save('E:\my_file.npy', dict)  # 注意带上后缀名
#
# # Load
# load_dict = np.load('E:\my_file.npy',allow_pickle=True).item()
# print(load_dict)
# load_dict['filter_result_dict'][2]=0
# np.save('E:\my_file.npy', load_dict)





# # 保存多个后缀.npz
# np_i = -1
# filter_result_dict = {}
# filter_commodity_dict = {}
# np.savez('E:\my_file.npz',np_i=np_i,filter_result_dict=filter_result_dict, filter_commodity_dict=filter_commodity_dict)
#
# dict = np.load('E:\my_file.npz', allow_pickle=True)
# np_i = dict['np_i'].tolist()
# np_i += 1
# np_filter_result_dict = dict['filter_result_dict'].tolist()
# np_filter_commodity_dict = dict['filter_commodity_dict'].tolist()
# print(str(np_i)+'\n'+str(np_filter_result_dict)+'\n'+str(np_filter_commodity_dict))
# np.savez('E:\my_file.npz',np_i=np_i)


for index in range(0, 101):
    print(index)
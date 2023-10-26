from exp_dp_command import exp_dp_command
from itertools import product

data_list = ['diabetes', 'german']
epsilon_list = [0.2, 0.5, 0.8, 1.0, 1.5, 2.0]
# epsilon_list = [.2, .5, .8]
method_list = ['fifo', 'fifoada']

for data, method, epsilon in product(data_list, method_list, epsilon_list):
    exp_dp_command(data, 'logistic', method, epsilon)
#
# for data in data_list:
#     exp_dp_command(data, 'logistic', 'non-private', 1.)

from plot_res import plot_res

def plot_command(data, loss, flag_time):
    if loss == 'hinge':
        method_list = ['auc_fifoada', 'auc_fifo']
        legend_list = [r'\texttt{AOGD}', r'$\texttt{OGD}$']
        legend_dict = dict(zip(method_list, legend_list))
        color_list = ['maroon', 'navy']
        line_list = ['--o', '-->']
        marker_list = ['>', '']        
    elif loss == 'square':
        method_list = ['auc_fifoada', 'auc_fifo']
        legend_list = [r'\texttt{AOGD}', r'$\texttt{OGD}']
        legend_dict = dict(zip(method_list, legend_list))
        color_list = ['navy', 'maroon']
        line_list = ['--o', '-->']
        marker_list = ['o', '>']
    elif loss == 'loglink':
        method_list = ['auc_fifoada','auc_fifo']
        legend_list = [r'\texttt{AOGD}', r'$\texttt{OGD}$']
        legend_dict = dict(zip(method_list, legend_list))
        color_list = ['navy','maroon']
        line_list = ['--o', '-->']
        marker_list = ['o', '>']  

    fig = plot_res(data, loss, method_list, legend_dict, color_list, marker_list, flag_time)
    if flag_time:
        fig.savefig('fig/' + data + '_' + loss + '_time' + '.png', dpi=600, bbox_inches='tight', pad_inches=0.05)
    else:
        fig.savefig('fig/' + data + '_' + loss + '.png', dpi=600, bbox_inches='tight', pad_inches=0.05)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Training setting')
    parser.add_argument('-d', '--data', default='diabetes')
    parser.add_argument('-t', '--time', action='store_true')
    args = parser.parse_args()

    plot_command(args.data, args.time)
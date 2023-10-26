import numpy as np
from sklearn import metrics
import timeit
from utils import get_idx, get_res_idx

def rs_xx_t(buf, buf_y, x, y, buf_size, t):
    '''
    Reservoir sampling xx at t = s+1
    :param buf_ids:
    :param idx:
    :param buf_size:
    :param n:
    :return:
    '''
    # run through buffer size
    for i in range(buf_size):
        rd = np.random.randint(buf_size + 1)
        if rd == buf_size:
            buf[i] = x
            buf_y[i] = y
        else:
            buf[i] = buf[rd]
            buf_y[i] = buf_y[rd]
    return buf, buf_y

def rs_xx(buf, buf_y, x, y, buf_size, n):
    '''
    Reservoir sampling xx
    :param buf_ids: the current buffer
    :param idx: sample at t
    :param buf_size: fixed buffer size
    :param n: number of received until t
    :return:
    '''
    # number of update
    k = np.random.binomial(buf_size, 1. / n)
    if k == 0:
        return buf, buf_y
    else:
        for i in range(k):
            idx_1 = np.random.randint(buf_size)
            buf[idx_1] = x
            buf_y[idx_1] = y
        return buf, buf_y

def auc_olp_square(x_tr, y_tr, x_te, y_te, options):
    n_tr = options['n_tr']
    dim = options['dim']
    n_pass = options['n_pass']
    start = timeit.default_timer()
    ids = get_idx(n_tr, n_pass)
    n_iter = len(ids)
    stop = timeit.default_timer()
    time_avg = (stop - start) / n_iter
    # ids = options['ids']
    # time_avg = options['time_avg']
    res_idx = options['res_idx']
    w_t = np.zeros(dim)
    w_sum = np.zeros(dim)
    w_sum_old = np.zeros(dim)
    eta_sum = 0.
    eta_sum_old = 0.
    eta = options['eta'] # initial eta
    etas = options['etas']
    beta = options['beta']
    buf_size = options['buffer']
    buf = np.zeros((buf_size, dim)) # initiate buffer
    buf_y = np.zeros(buf_size)

    aucs = np.zeros(len(res_idx))
    times = np.zeros(len(res_idx))
    t = 0
    i_res = 0
    time_sum = 0.
    # initiate timer
    start = timeit.default_timer()
    while t < n_iter:
        # current example
        x_t = x_tr[ids[t]]
        y_t = y_tr[ids[t]]
        eta_t = etas[t]
        if t < buf_size:
            buf[t] = x_t
            buf_y[t] = y_t
        elif t == buf_size:
            buf, buf_y = rs_xx_t(buf, buf_y, x_t, y_t, buf_size, t)
        else:
            buf, buf_y = rs_xx(buf, buf_y, x_t, y_t, buf_size, t)
        if y_t == 1:
            xx = x_t - buf[buf_y < 0]
            gd = -2 * (1 - np.inner(xx, w_t))[:, None] * xx
            # gradient step
            w_t = w_t - eta_t * np.sum(gd, axis=0) / min(t + 1, buf_size)
        else:
            xx = buf[buf_y > 0] - x_t
            gd = -2 * (1 - np.inner(xx, w_t))[:, None] * xx
            # gradient step
            w_t = w_t - eta_t * np.sum(gd, axis=0) / min(t + 1, buf_size)

        if options['proj_flag']:
            # projection
            norm = np.linalg.norm(w_t)
            if norm > beta:
                w_t = w_t * beta / norm
        # naive average
        w_sum = w_sum + w_t
        eta_sum = eta_sum + 1
        # # average eta with two step ago
        # w_sum = w_sum + eta_t * w_t_2
        # eta_sum = eta_sum + eta_t
        # # move t-2
        # w_t_2 = w_t_1 + 0.
        # # move t-1
        # w_t_1 = w_t + 0.
        # update
        t = t + 1

        # save results
        if i_res < len(res_idx) and res_idx[i_res] == t:
            # stop timer
            stop = timeit.default_timer()
            time_sum += stop - start + time_avg * (eta_sum - eta_sum_old)
            # average output
            w_avg = (w_sum - w_sum_old) / (eta_sum - eta_sum_old) # trick: only average between two i_res
            pred = (x_te.dot(w_avg.T)).ravel()
            if not np.all(np.isfinite(pred)):
                break
            fpr, tpr, thresholds = metrics.roc_curve(y_te, pred.T, pos_label=1)
            aucs[i_res] = metrics.auc(fpr, tpr)
            times[i_res] = time_sum
            i_res = i_res + 1
            w_sum_old = w_sum
            eta_sum_old = eta_sum
            # restart timer
            start = timeit.default_timer()
    return aucs, times


def rs_x_t_(buf, buf_y, x, y, buf_size, t):
    '''
    Reservoir sampling x at t = s+1
    :param buf_ids:
    :param idx:
    :param buf_size:
    :param n:
    :return:
    '''
    for i in range(buf_size):
        rd = np.random.randint(buf_size + 1)
        if rd == buf_size:
            buf[i] = x
            buf_y[i] = y
        else:
            buf[i] = buf[rd]
            buf_y[i] = buf_y[rd]
    return buf, buf_y


if __name__ == '__main__':
    from utils import data_processing

    from sklearn.model_selection import train_test_split
    options = dict()
    options['n_pass'] = 5
    options['rec_log'] = .1
    options['rec'] = 50
    options['log_res'] = False
    options['eta'] = 10.
    options['beta'] = 10.
    options['buffer'] = 200

    x, y = data_processing('diabetes')
    x_tr, x_te, y_tr, y_te = train_test_split(x, y)
    aucs, times = auc_olp_square(x_tr, y_tr, x_te, y_te, options)
    print('-------------')
    print('All Past Algorithm')
    print('-------------')
    print('AUC Score')
    print(aucs)
    print('-------------')
    print('Time Elapsed')
    print(times)
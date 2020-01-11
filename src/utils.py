import numpy as np

def median(x):
    x = np.array(x)
    med = np.median(x)

    return med


def iqr(x, c=1.5):
    x = np.array(x)

    q75, q25 = np.percentile(x, [75, 25])
    iqr = q75 - q25
    top_lim = q75 + 1.5 * iqr
    bot_lim = q25 - 1.5 * iqr

    no = x[ (x <= top_lim) & (x >= bot_lim) ]
    avg = np.mean(no)

    return avg


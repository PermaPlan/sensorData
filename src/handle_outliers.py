import numpy as np

x = np.array([47.00, 22.00, 48.00, 48.00, 48.00, 400.00, 47.00, 100.00, 48.00, 48.00])

def outlier_handle(x):
    q75, q25 = np.percentile(x, [75, 25])
    iqr = q75 - q25
    top_lim = q75 + 1.5 * iqr
    bot_lim = q25 - 1.5 * iqr 

    no = x[ (x <= top_lim) & (x >= bot_lim) ]
    avg = np.mean(no)
    med = np.median(x)

    return [avg, med]


avg, med = outlier_handle(x)
print(avg)
print(med)


def preprecess_nn(pre):
    """Convert $pre to NN input"""

    res = [0 for i in range(20)]

    # extract category id on the hundredth
    tmp = [0 for i in range(6)]
    for i in range(len(pre)):
        tmp[pre[i] // 100] = tmp[pre[i] // 100] + 1

    # find the 2 favorite categories
    maxid1, maxval = 0, 0
    for i in range(len(tmp)):
        if maxval < tmp[i]:
            maxid1 = i
            maxval = tmp[i]
    res[0] = maxid1
    tmp[maxid1] = -1
    maxid2, maxval = 0, 0
    for i in range(len(tmp)):
        if maxval < tmp[i]:
            maxid2 = i
            maxval = tmp[i]
    res[10] = maxid2

    tmp1 = 1
    tmp2 = 11
    for i in range(len(pre)):
        if pre[i] // 100 == maxid1:
            if tmp1 < 10:
                res[tmp1] = pre[i] % 100
                tmp1 += 1
        if pre[i] // 100 == maxid2:
            if tmp2 < 20:
                res[tmp2] = pre[i] % 100
                tmp2 += 1

    return res

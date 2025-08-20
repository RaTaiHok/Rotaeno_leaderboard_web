def find_interval_index(value, intervals):
    for i, interval in enumerate(intervals):
        if value < interval:
            return i
    return len(intervals)

def xp_calc(value):
    prefix_sum = [100, 220, 360, 520, 700, 900, 1120, 1360, 1660, 1870, 2090, 2320, 2560, 2810, 3070, 3340, 3620, 3910, 4210, 4460, 4720, 4990, 5270, 5560, 5860, 6170, 6490, 6820, 7160, 7510, 7870, 8240, 8620, 9010, 9410, 9820, 10240, 10670, 11110, 11560, 12020, 12490, 12970, 13460, 13960, 14470, 14990]
    intervals = [prefix_sum[i] for i in range(len(prefix_sum))]
    level = find_interval_index(value, intervals)

    if level != len(intervals):
        lower_limit = intervals[level - 1] if level > 0 else 0
        upper_limit = intervals[level]
        return level, value - lower_limit, upper_limit - lower_limit
    else:
        xp_difv = value - prefix_sum[-1]
        level = len(prefix_sum) + (xp_difv // 500) + 1
        up_xp = prefix_sum[-1] + ((xp_difv // 500) * 500)
        calc_difv = value - up_xp
        return level, calc_difv, 500
    
# if __name__ == "__main__":
#     print(xp_calc(340))
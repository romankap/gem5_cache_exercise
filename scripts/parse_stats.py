import re
from histogram_stat import HistogramStatsList

STATS_FILE_PATH = "/home/rkaplan/gem5_exercise/gem5/m5out/stats.txt"
MISS_LATENCY_STR = "missLatency"
L2_CACHE_STR = "l2cache"

#------------------------------------------

def get_histogram_stats_list(file_lines, stat_filter):
    hist_stats_list = HistogramStatsList(stat_filter, "L2 Miss Latencies")

    for line in file_lines:
        if MISS_LATENCY_STR in line:
            split_line = re.split(' +', line)
            hist_stats_list.append_line_to_histogram_list(split_line)

    return hist_stats_list

#-------------------------------------------

def plot_histogram_from_stats_file(stats_file_path, L2_CACHE_STR):
    # Using readlines()
    stats_file = open(stats_file_path, 'r')
    file_lines = stats_file.readlines()
    hist_stats_list = get_histogram_stats_list(file_lines, L2_CACHE_STR)
    hist_stats_list.plot_histogram()

    return hist_stats_list
#------------------------------------------

plot_histogram_from_stats_file(STATS_FILE_PATH, L2_CACHE_STR)
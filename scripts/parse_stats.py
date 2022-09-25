import re, os
from histogram_stat import HistogramStatsList

M5OUT_STATS_FILE_PATH = "/home/rkaplan/gem5_exercise/gem5/m5out/stats.txt"
SE_RESULTS_DIR_PATH = "/home/rkaplan/gem5_exercise/gem5/se_results/"
STATS_TXT_FILENAME = "stats.txt"
MISS_LATENCY_STR = "missLatency"
L2_CACHE_STR = "l2cache"
L3_CACHE_STR = "l3cache"
L3_STR = "l3"

INT_MM_STR = "IntMM"

#------------------------------------------

def get_histogram_stats_list(file_lines, stat_filter):
    hist_stats_list = HistogramStatsList(stat_filter, "L2 Miss Latencies")

    for line in file_lines:
        if MISS_LATENCY_STR in line:
            split_line = re.split(' +', line)
            hist_stats_list.append_line_to_histogram_list(split_line)

    return hist_stats_list

#-------------------------------------------

def plot_histogram_from_stats_file(stats_file_path, cache_level_string):
    # Using readlines()
    stats_file = open(stats_file_path, 'r')
    file_lines = stats_file.readlines()
    hist_stats_list = get_histogram_stats_list(file_lines, cache_level_string)
    hist_stats_list.plot_histogram()

    return hist_stats_list
#------------------------------------------

def plot_se_benchmark_histogram(benchmark_name, cache_level_string):
    thispath = os.path.dirname(os.path.realpath(__file__))
    bm_stats_file_full_path = os.path.join(thispath, '../',
                        SE_RESULTS_DIR_PATH, benchmark_name,
                        STATS_TXT_FILENAME)
    _ = plot_histogram_from_stats_file(bm_stats_file_full_path,
                                    cache_level_string)

#------------------------------------------

# plot_histogram_from_stats_file(M5OUT_STATS_FILE_PATH, L2_CACHE_STR)
plot_se_benchmark_histogram(INT_MM_STR, L3_STR)

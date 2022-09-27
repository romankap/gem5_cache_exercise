import re, os
from histogram_stat import HistogramStatsList
import matplotlib.pyplot as plt
import argparse

GEM5_BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../")
BUILD_SCRIPT_RELATIVE_PATH = 'build/ARM/gem5.opt'
M5OUT_STATS_FILE_PATH = os.path.join(GEM5_BASE_PATH, "m5out/stats.txt")
SE_RESULTS_BASE_DIR_PATH = os.path.join(GEM5_BASE_PATH, "se_results/")
ONLY_L2_STR = "only_L2"
WITH_L3_STR = "with_L3"
SE_BENCHMARKS_BASE_DIR_PATH = os.path.join(GEM5_BASE_PATH, "se-benchmarks/")
STARTER_SE_W_L2_CACHE_SCRIPT_PATH = "configs/example/arm/starter_se.py"
STARTER_SE_W_L3_CACHE_SCRIPT_PATH = "configs/example/arm/starter_se_with_l3_cache.py"
STATS_TXT_FILENAME = "stats.txt"
SE_RESULTS_STR = "se_results"
MISS_LATENCY_STR = "missLatency"
L2_CACHE_STR = "l2cache"
L3_CACHE_STR = "l3cache"
L2_STR = "l2"
L3_STR = "l3"
SPACE_CHAR = ' '

# Benchmarks
BUBBLE_SORT_STR = "Bubblesort"
QUICK_SORT_STR = "Quicksort"
INT_MM_STR = "IntMM"
FLOAT_MM_STR = "FloatMM"
REAL_MM_STR = "RealMM"
OSCAR_STR = "Oscar"
# BENCHMARKS_LIST = [BUBBLE_SORT_STR, QUICK_SORT_STR, INT_MM_STR]
BENCHMARKS_LIST = [INT_MM_STR, QUICK_SORT_STR, OSCAR_STR, BUBBLE_SORT_STR]
ALL_STR = "all"


#------------------------------------------

def get_histogram_stats_list(file_lines, stat_filter, benchmark_type, benchmark_name):
    plot_title_name = benchmark_name + " , " + benchmark_type
    hist_stats_list = HistogramStatsList(stat_filter, "L2 Miss Latencies", plot_title_name)

    for line in file_lines:
        if MISS_LATENCY_STR in line:
            split_line = re.split(' +', line)
            hist_stats_list.append_line_to_histogram_list(split_line)

    return hist_stats_list

#-------------------------------------------

def plot_histogram_from_stats_file(stats_file_path, cache_level_string,
                                    benchmark_type, benchmark_name):
    # Using readlines()
    stats_file = open(stats_file_path, 'r')
    file_lines = stats_file.readlines()
    hist_stats_list = get_histogram_stats_list(file_lines, cache_level_string,
                                                benchmark_type, benchmark_name)
    hist_stats_list.plot_histogram()

    return hist_stats_list
#------------------------------------------

def get_se_results_dir_path(benchmark_type, benchmark_name):
    benchmark_results_base_path = os.path.join(GEM5_BASE_PATH, SE_RESULTS_STR)
    if benchmark_type == L2_STR:
        benchmark_results_path = os.path.join(benchmark_results_base_path, ONLY_L2_STR)
    else: # benchmark_type == L3_STR
        benchmark_results_path = os.path.join(benchmark_results_base_path, WITH_L3_STR)
    benchmark_results_path = os.path.join(benchmark_results_path, benchmark_name)

    return benchmark_results_path

#------------------------------------------

def plot_se_benchmark_histogram(benchmark_name, benchmark_type, cache_level_string):    
    bm_stats_file_base_path = get_se_results_dir_path(benchmark_type, benchmark_name)
    bm_stats_file_full_path = os.path.join(bm_stats_file_base_path, STATS_TXT_FILENAME)
    histogram = plot_histogram_from_stats_file(bm_stats_file_full_path,
                                    cache_level_string, benchmark_type, benchmark_name)
    return histogram

#------------------------------------------

def execute_se_benchmark(benchmark_name, benchmark_type):
    build_path = os.path.join(GEM5_BASE_PATH, BUILD_SCRIPT_RELATIVE_PATH)
    execution_param = "-d"
    benchmark_results_path = get_se_results_dir_path(benchmark_type, benchmark_name)
    if benchmark_type == L3_STR:
        starter_se_script_path = os.path.join(GEM5_BASE_PATH, STARTER_SE_W_L3_CACHE_SCRIPT_PATH)
    else:
        starter_se_script_path = os.path.join(GEM5_BASE_PATH, STARTER_SE_W_L2_CACHE_SCRIPT_PATH)
    starter_se_script_params = '--cpu="hpi"' 
    benchmark_path = os.path.join(SE_BENCHMARKS_BASE_DIR_PATH, benchmark_name)

    execution_str = build_path + SPACE_CHAR + execution_param + \
                    benchmark_results_path + SPACE_CHAR + \
                    starter_se_script_path + SPACE_CHAR + \
                    starter_se_script_params + SPACE_CHAR + \
                    benchmark_path
    os.system(execution_str)
    print("\n ********* Done executing *********")

#------------------------------------------

def set_and_return_parsed_args():
    parser = argparse.ArgumentParser(description="Choose whether to execute a BM or only compare.")

    parser.add_argument("--bm_names", type=str, choices=BENCHMARKS_LIST,
                        default=INT_MM_STR, nargs='*', metavar='',
                        help="Choose which BM to execute or compare: " +
                        ', '.join(BENCHMARKS_LIST) + " or all.")
    parser.add_argument("--execute_bm", default=False, action='store_true',
                        help="If the argument is set, the benchmarks will be executed before their comparison.")
    args = parser.parse_args()
    return args

#------------------------------------------

def compare_benchmark_stats(benchmark_name):
    histogram_w_only_L2 = plot_se_benchmark_histogram(benchmark_name, benchmark_type=L2_STR, cache_level_string=L2_STR)
    only_L2_mean = histogram_w_only_L2.get_mean()
    only_L2_samples_num = histogram_w_only_L2.get_samples_num()

    histogram_with_L3 = plot_se_benchmark_histogram(benchmark_name, benchmark_type=L3_STR, cache_level_string=L2_STR)
    with_L3_mean = histogram_with_L3.get_mean()
    with_L3_samples_num = histogram_with_L3.get_samples_num()

    print("{}: Adding L3 changed L2 miss latencies mean from {} to {}".format(benchmark_name, only_L2_mean, with_L3_mean))
    print("{}: Adding L3 changed L2 number of misses from {} to {}".format(benchmark_name, only_L2_samples_num, with_L3_samples_num))

#------------------------------------------

def main():
    args = set_and_return_parsed_args()
    if args.execute_bm:
        if ALL_STR in args.bm_names:
            for bm_name in BENCHMARKS_LIST:
                execute_se_benchmark(bm_name, L2_STR)
                execute_se_benchmark(bm_name, L3_STR)
        else:
            for bm_name in args.bm_names:
                execute_se_benchmark(bm_name, L2_STR)
                execute_se_benchmark(bm_name, L3_STR)

    if ALL_STR in args.bm_names:
        for bm_name in BENCHMARKS_LIST:
            compare_benchmark_stats(bm_name)
    else:
        for bm_name in args.bm_names:
            compare_benchmark_stats(bm_name)
    plt.show(block=True)


#------------------------------------------

main()

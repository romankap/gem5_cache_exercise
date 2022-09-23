import re

STATS_FILE_PATH = "/home/rkaplan/gem5_exercise/gem5/m5out/stats.txt"
MISS_LATENCY_STR = "missLatency"

#------------------------------------------

def parse_stats_file(stats_file_path):
    # Using readlines()
    file1 = open(stats_file_path, 'r')
    Lines = file1.readlines()
    
    count = 0
    # Strips the newline character
    for line in Lines:
        if MISS_LATENCY_STR in line:
            split_line = re.split(' +', line)
            print("Line{}: {}".format(count, line.strip()))

#------------------------------------------

parse_stats_file(STATS_FILE_PATH)
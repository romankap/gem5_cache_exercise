from tkinter.messagebox import NO
import matplotlib.pyplot as plt

#-------------------------------------------
def is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False
#----------------------------------------------

class HistogramStat:
    def __init__(self, split_line):
        self.bucketRange = self.extract_histogram_bucket(split_line[0])
        self.bucketSamplesNum = int(split_line[1])
        self.samplesSharePercent = float(split_line[2].split("%")[0])

    #-------------------------------------------------
    
    @classmethod
    def extract_histogram_bucket(cls, stat_string):
        bucket_range = stat_string.split("::")[1]
        return bucket_range

    #-------------------------------------------------

    def get_bucket_range(self):
        return self.bucketRange

    #-------------------------------------------------

    def get_bucket_samples_num(self):
        return self.bucketSamplesNum

    #-------------------------------------------------

    def get_bucket_samples_share(self):
        return self.samplesSharePercent

    #-------------------------------------------------
    #-------------------------------------------------

    @classmethod
    def is_histogram_stat_line(cls, split_line):
        bucket_range = split_line[0].split("::")[1]
        range_start = bucket_range.split("-")[0]
        if range_start.isnumeric() or is_float(range_start):
            return True
        else:
            return False

    #-------------------------------------------------

    @classmethod
    def is_stat_line_contains_string(cls, split_line, stat_filter):
        bucket_stat_string = split_line[0].split("::")[0]
        if stat_filter in bucket_stat_string:
            return True
        else:
            return False

#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------

class HistogramStatsList:
    def __init__(self, stat_filter = None, name = None):
        self.listName = name
        self.statFilter = stat_filter
        self.histStatsList = []

    #--------------------------------------------------

    def append_line_to_histogram_list(self, split_line):
        is_hist_line = HistogramStat.is_histogram_stat_line(split_line)
        if self.statFilter != None:
            is_stat_contains_string = HistogramStat.is_stat_line_contains_string(split_line, self.statFilter)
        else:
            is_stat_contains_string = True
        
        if is_hist_line and is_stat_contains_string:
            hist_stat = HistogramStat(split_line)
            self.histStatsList.append(hist_stat)

    #--------------------------------------------------

    def plot_histogram(self):
        bucket_ranges = []
        bucket_samples = []

        for hist_stat in self.histStatsList:
            bucket_ranges.append(hist_stat.get_bucket_range())
            bucket_samples.append(hist_stat.get_bucket_samples_num())

        plt.bar(bucket_ranges, bucket_samples)

        plt.xlabel("Clock ticks range")
        plt.ylabel("No. of misses")
        plt.title("Cache misses vs. Clock ticks range")
        plt.xticks(rotation=90)
        plt.show()
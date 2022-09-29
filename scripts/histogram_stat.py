import plotly.express as px
from time import sleep

MEAN_STR = "mean"
SAMPLES_STR = "samples"
TOTAL_STR = "total"
L2_STR = "l2"
L3_STR = "l3"

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
    #-------------------------------------------------

    @classmethod
    def is_stat_line_contains_mean(cls, split_line):
        bucket_stat_string = split_line[0].split("::")[1]
        if MEAN_STR == bucket_stat_string:
            return float(split_line[1])
        else:
            return None

    #-------------------------------------------------

    @classmethod
    def is_stat_line_contains_total_samples(cls, split_line):
        bucket_stat_string = split_line[0].split("::")[1]
        if SAMPLES_STR == bucket_stat_string:
            return int(split_line[1])
        else:
            return None


#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------

class HistogramStatsList:
    def __init__(self, stat_filter = None, name = None, plot_title_name = None):
        self.listName = name
        self.statFilter = stat_filter
        self.plotTitle = plot_title_name

        self.plotColor = "blue" if L2_STR.upper() in plot_title_name else "orange"
        self.mean = -1
        self.samples_num = -1
        self.histStatsList = []

    #--------------------------------------------------

    def get_benchmark_name(self):
        return self.plotTitle

    #--------------------------------------------------

    def get_mean(self):
        return self.mean
    
    #--------------------------------------------------

    def get_samples_num(self):
        return self.samples_num
    #--------------------------------------------------


    def check_if_line_has_special_stat_and_set(self, split_line):
        mean_val = HistogramStat.is_stat_line_contains_mean(split_line)
        if mean_val != None:
            self.mean = mean_val if mean_val < 10.0 else int(mean_val)
            return
        
        samples_num_val = HistogramStat.is_stat_line_contains_total_samples(split_line)
        if samples_num_val != None:
            self.samples_num = samples_num_val

    #--------------------------------------------------

    def append_line_to_histogram_list(self, split_line):
        is_histogram_line = HistogramStat.is_histogram_stat_line(split_line)
        if self.statFilter != None:
            is_stat_contains_string = HistogramStat.is_stat_line_contains_string(split_line, self.statFilter)
        else:
            is_stat_contains_string = True
        
        if is_stat_contains_string:
            if is_histogram_line:
                hist_stat = HistogramStat(split_line)
                self.histStatsList.append(hist_stat)
            else:
                self.check_if_line_has_special_stat_and_set(split_line)

    #--------------------------------------------------

    def plot_histogram(self):
        bucket_ranges = []
        bucket_samples = []

        for hist_stat in self.histStatsList:
            bucket_ranges.append(hist_stat.get_bucket_range())
            bucket_samples.append(hist_stat.get_bucket_samples_num())

        print("{} samples num = {}".format(self.statFilter, self.samples_num))
        print("{} mean = {}".format(self.statFilter, self.mean))

        title = self.plotTitle + ": " if self.plotTitle != None else ""
        title += "Cache miss latencies vs. Clock ticks range. "
        title += "Average L2 latency = {} clock ticks".format(self.mean)

        fig = px.bar(x=bucket_ranges, y=bucket_samples,
                     title=title)
        fig.update_traces(marker_color=self.plotColor)
        fig.update_layout(xaxis_title="Miss latency clock ticks range",
                          yaxis_title="Number of latency samples within ticks range")
        fig.show()
        sleep(0.5) # Added 0.5sec of wait between plots for functional stability.

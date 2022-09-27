#SRCS = $(wildcard *.c)

#PROGS = $(patsubst(SRCS))

#all: $(PROGS)
#all: $(SRCS)

#%: %.c


#LEVEL = ../../..
LDFLAGS += -lm
FP_TOLERANCE = 0.001

ifdef BENCHMARKING_ONLY
PROGRAMS_TO_SKIP += IntMM
endif

#include $(LEVEL)/SingleSource/Makefile.singlesrc

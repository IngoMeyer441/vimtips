ifeq ($(shell uname -s), Darwin)
DEFAULT_TARGET = unblank_check
else
DEFAULT_TARGET =
endif

INCLUDES =
CFLAGS = -Wall -O2 -mmacosx-version-min=10.5 $(INCLUDES)
LIBS= -framework IOKit -framework CoreFoundation
LDFLAGS = $(LIBS)

all: $(DEFAULT_TARGET)

unblank_check: unblank_check.o
	$(CC) -o $@ $^ $(LDFLAGS)

%.o: %.c
	$(CC) -c $(CFLAGS) $<

clean:
	rm -f unblank_check *.o

.PRECIOUS: %.o
.PHONY: all clean

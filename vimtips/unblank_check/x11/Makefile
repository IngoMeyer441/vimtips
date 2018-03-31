ifeq ($(shell uname -s), Linux)
DEFAULT_TARGET = unblank_check
else
DEFAULT_TARGET =
endif

INCLUDES =
CFLAGS = -Wall -O2 $(INCLUDES)
LIBS= -lXext -lX11
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

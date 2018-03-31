SUBDIRS := $(shell find . -mindepth 1 -maxdepth 1 -type d)

all: subdirs

subdirs:
	for d in $(SUBDIRS); do \
		if [ -f "$${d}/Makefile" ]; then \
			$(MAKE) -C $${d}; \
		fi; \
	done

clean:
	for d in $(SUBDIRS); do \
		if [ -f "$${d}/Makefile" ]; then \
			$(MAKE) -C $${d} clean; \
		fi; \
	done

.PHONY: subdirs clean

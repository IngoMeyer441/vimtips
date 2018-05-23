#!/bin/bash

xscreensaver-command -watch | awk '$1 == "UNBLANK" { print "unblank"; fflush(stdout) }'

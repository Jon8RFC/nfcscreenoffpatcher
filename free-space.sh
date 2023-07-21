#!/bin/sh
ls -td data/*/ | tail -n +10 | xargs rm -rf

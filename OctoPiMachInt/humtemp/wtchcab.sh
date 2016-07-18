#!/bin/bash

# if there is no gpiod daemon running run it

# use watch to run the python sensor reading script
watch -n10 ./gethumtemp.py


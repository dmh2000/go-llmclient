#!/bin/sh

cli="../../cmd/sqirvy-cli"

plan="I want to build a clone of the tetris game that runs in the shell. it will be implemented in python in a single file. use any\
libraries that make it easier.\
"

code=""

review=""

echo $plan | go run $cli plan -m gemini-2.5-flash   >plan.md

go run $cli code -m claude-sonnet-4 plan.md         >tetris.py

go run $cli review -m gpt-5-mini tetris.py         >review.md




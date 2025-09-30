#!/bin/bash

BINDIR=../bin
TESTDIR=./test
TARGET=


check_return_code() {
    local ret=$?
    if [ $ret -ne 0 ]; then
        echo "Command failed with exit code $ret"
        exit 1
    fi
}


plan="create a plan for scafolding a single page web app using the vit framework. \
   the app should be sleek and modern. \
   the app should have a responsive layout that works on desktop and mobile. \
   the app should have a dark theme. \
   the app should have a sidebar that can be toggled on and off. 
   the functionality of the app will be determined later.
   the app should be built using the latest version of vit. \
   the app should be built using the latest version of typescript.
   this is a plan only, do not generate any code."

code="create a simple webpage with a counter and buttons to increment and decrement the counter. \
   the counter should be stored in a cookie so that it persists across page reloads. \
   the counter should be initialized to 0 when the page is first loaded. \
   the counter should be incremented by 1 when the increment button is clicked. \
   the counter should be decremented by 1 when the decrement button is clicked. \
   the counter should never be less than 0. \
   the counter should be displayed in the center of the page. \
   the increment and decrement buttons should be displayed below the counter. \
   the increment and decrement buttons should be centered horizontally. \
   the increment and decrement buttons should be styled so that they are visually distinct. \
   use html, css and javascript in a single file"

query="what is the sum of 1 + 2 + 3"   

mkdir -p $TESTDIR

echo "-------------------------------"
echo "sqirvy no flags or args"
go run .         
check_return_code

echo "-------------------------------"
echo "sqirvy -h"
go run . -h                                                          >$TESTDIR/help.md
check_return_code

echo "-------------------------------"
echo "sqirvy  plan"
echo $plan | go run . plan -m gemini-2.5-flash main.go               >$TESTDIR/plan.md
check_return_code

echo "-------------------------------"
echo "sqirvy  code"
echo $code | go run . code                                           >$TESTDIR/code.html
check_return_code

echo "-------------------------------"
echo "sqirvy review"
echo $review | go run . review -m gemini-2.5-flash main.go           >$TESTDIR/review.md
check_return_code

echo "-------------------------------"
echo "sqirvy query"
echo $query  | go run . query -m claude-3-5-haiku-20241022 main.go   >$TESTDIR/query1.md
check_return_code

echo "-------------------------------"

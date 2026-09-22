#!/usr/bin/env bash
# bash_basics.sh - shebang, variables, input/output, conditions, loops
NAME="$(whoami)"                       # no spaces around =
read -rp "Enter a number: " NUM
echo "Hello $NAME, you typed $NUM"

if [ "$NUM" -gt 10 ]; then echo "bigger than 10"
elif [ "$NUM" -eq 10 ]; then echo "exactly 10"
else echo "smaller than 10"; fi

for i in 1 2 3; do echo "for loop: $i"; done
count=0
while [ "$count" -lt 3 ]; do echo "while loop: $count"; count=$((count + 1)); done
echo "script: $0 | first arg: ${1:-none} | arg count: $#"

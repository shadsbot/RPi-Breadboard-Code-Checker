#!/bin/bash

A="$(python -m pyflakes $1 &>asdf)"

#while read line
#do
#	echo $line
#done <asdf

line=$(head -n 1 asdf)

echo "$(echo $line | cut -d':' -f 2)"

rm asdf

exit 0

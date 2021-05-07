#!/bin/sh

FILE=`readlink -f $0`
DIR=`dirname $FILE`

pip3 install "$DIR"
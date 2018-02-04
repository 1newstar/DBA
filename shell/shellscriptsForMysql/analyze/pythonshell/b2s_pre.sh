#!/bin/bash
# 该脚本用来转换格式
# Usage： bash b2s_pre.sh filename
# 输出filname.new
mysqlbinlog -vv --base64-output=DECODE-ROWS $1 > tmp$1
awk  '$0~/^###/ || $0~/end_log_pos.*flags/ {print $0}' tmp$1 | sed 's/^### //;s@\/\*.*\*\/@@' > ${1}.new
rm -rf tmp$1

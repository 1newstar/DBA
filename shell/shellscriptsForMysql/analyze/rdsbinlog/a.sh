#!/bin/bash

cp $0 bac
i=0
while read line 
do
	i=$(($i+1))
	echo $i
	sed  -i "s/@$i=/$line=/g" bac
done < $1

#!/bin/bash

for host in 35.95.27.22 35.87.176.209 52.34.140.159 34.220.162.24 54.149.143.251 
do
	echo $host
	ssh "$shost" "pwd"
done

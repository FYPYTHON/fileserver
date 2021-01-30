#!/bin/bash

useage=$(PYTHONPATH=/opt/midware/FSTornado/python3_fs/lib/python3.5/site-packages /opt/midware/python3.5/bin/python3 /opt/midware/study/src/script/diskusage.py $1)

echo "use" $useage 

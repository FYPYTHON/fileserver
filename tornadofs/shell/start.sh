#!/bin/bash

#PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/opt/midware/sharelib/leptonica/lib/pkgconfig
#export PKG_CONFIG_PATH
#CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:/opt/midware/sharelib/leptonica/include/leptonica
#export CPLUS_INCLUDE_PATH
#C_INCLUDE_PATH=$C_INCLUDE_PATH:/opt/midware/sharelib/leptonica/include/leptonica
#export C_INCLUDE_PATH
#LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/midware/sharelib/leptonica/lib
#export LD_LIBRARY_PATH
#LIBRARY_PATH=$LIBRARY_PATH:/opt/midware/sharelib/leptonica/lib
#export LIBRARY_PATH
#LIBLEPT_HEADERSDIR=/opt/midware/sharelib/leptonica/include/leptonica
#export LIBLEPT_HEADERSDIR
#
#PATH=$PATH:/opt/midware/sharelib/tesseract/bin
#export PATH
#
#LD_LIBRARY_PATH=/opt/midware/sharelib/tesseract/lib:$LD_LIBRARY_PATH
#TESSDATA_PREFIX=/opt/midware/sharelib/tesseract/share/tessdata
#export TESSDATA_PREFIX

# /opt/midware/sharelib/tesseract/bin/tesseract -v


find /opt/midware/FSTornado/python3_fs  -type d -name __pycache__ | xargs rm -rf
# PYTHONPATH=/opt/midware/FSTornado/python3_baselib/lib/python3.5/site-packages:/opt/midware/FSTornado/python3_fs/lib/python3.5/site-packages
PYTHONPATH=/opt/midware/FSTornado/python3_fs/lib/python3.5/site-packages /opt/midware/python3.5/bin/python3 /opt/midware/FSTornado/main_app.py & > /dev/null 2>&1

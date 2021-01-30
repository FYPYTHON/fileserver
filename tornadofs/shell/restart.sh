#!/bin/bash
cd /opt/midware/FSTornado
./shell/stop.sh
./shell/start.sh

ps -ef | grep "tornadofs"

#!/bin/bash
ps -ef | grep "start.sh" | grep -v grep | awk '{print $2}' | xargs kill -9

ps -ef | grep "main" | grep -v grep | awk '{print $2}' | xargs kill -9

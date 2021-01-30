#!/bin/bash

ps -ef | grep "tornadofs" | grep -v grep | awk '{print $2}' | xargs kill -9



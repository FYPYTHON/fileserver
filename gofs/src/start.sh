#!/bin/bash

export GOROOT=/opt/midware/go
export GOPATH=/opt/midware/study

go build -o ../bin/beego
# go install
go run main.go &

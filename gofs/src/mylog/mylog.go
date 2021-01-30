package mylog

import (
	"fmt"
	"io"
	"log"
	"os"
	"runtime"
)

var (
	Info *log.Logger
	Warning *log.Logger
	Error * log.Logger
)

//const logpath string = "E:/opt/log/go/"

func init(){
	sysType := runtime.GOOS
	var logpath string
	if sysType == "linux" {
		// LINUX系统
		logpath = "/opt/log/go/"
	} else {
		logpath = "E:/opt/log/go/"
	}

	_, err := os.Stat(logpath)
	// fmt.Println(err)
	if err != nil{
		fmt.Println("make dir")
		err:=os.MkdirAll(logpath, os.ModePerm)
		if err!=nil{
			fmt.Println(err)
		} else {
			fmt.Println(err)
		}
	}
	infoFile,err1:=os.OpenFile(logpath + "info.log",os.O_CREATE|os.O_WRONLY|os.O_APPEND,0666)
	warnFile,err2:=os.OpenFile(logpath + "warn.log",os.O_CREATE|os.O_WRONLY|os.O_APPEND,0666)
	errFile,err3:=os.OpenFile(logpath + "errors.log",os.O_CREATE|os.O_WRONLY|os.O_APPEND,0666)

	if err1!=nil || err2 != nil || err3!=nil{
		fmt.Println(infoFile, warnFile, errFile)
		log.Fatalln("打开日志文件失败：",err1, err2, err3)

	}

	Info = log.New(os.Stdout,"Info:",log.Ldate | log.Ltime | log.Lshortfile)
	Warning = log.New(os.Stdout,"Warning:",log.Ldate | log.Ltime | log.Lshortfile)
	Error = log.New(io.MultiWriter(os.Stderr,errFile),"Error:",log.Ldate | log.Ltime | log.Lshortfile)

	Info = log.New(io.MultiWriter(os.Stderr,infoFile),"Info:",log.Ldate | log.Ltime | log.Lshortfile)
	Warning = log.New(io.MultiWriter(os.Stderr,warnFile),"Warning:",log.Ldate | log.Ltime | log.Lshortfile)
	Error = log.New(io.MultiWriter(os.Stderr,errFile),"Error:",log.Ldate | log.Ltime | log.Lshortfile)


}
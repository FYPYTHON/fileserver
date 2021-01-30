package main

import (
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/logs"
	_ "mytask"
	_ "myweb"
	"time"
)

func main(){
	//myfunc.GetDaysAgo(10)
	//myfunc.WeSay()
	//runtime.GOMAXPROCS(2)
	logs.SetLogFuncCallDepth(3)
	logs.Info("gofs start...", time.Now().String())
	beego.Run()
}

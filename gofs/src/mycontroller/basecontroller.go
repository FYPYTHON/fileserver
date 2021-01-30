package mycontroller

import (
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/logs"
	"github.com/astaxie/beego/orm"
	"golang.org/x/exp/errors/fmt"
	"mydata"
	"mydb"
	"myfunc"
	"os"
	"strings"
	"time"
)

type baseController struct {
	beego.Controller
	o  orm.Ormer
	controllerName string
	actionName string
	loginname  string
	user 	   *mydb.TblAccount
}

func (this *baseController) Prepare() {
	//logs.Info(this.Ctx.Input.Context.Request.Form)
	logs.Info(this.getRunInfo(), this.getClientIP(), this.Ctx.Request.Method, this.Ctx.Request.URL, this.Ctx.Input.Context.Request.Form)
	controllerName, actionName := this.GetControllerAndAction()
	// logs.Info(controllerName, actionName)
	this.controllerName = strings.ToLower(controllerName[0 : len(controllerName)-10])
	this.actionName = strings.ToLower(actionName)
	this.o = orm.NewOrm()
	if strings.HasPrefix(this.Ctx.Request.URL.Path, "/download") &&
		this.Ctx.Request.Method == "GET"{
		// download not check
		this.history()
	} else {
		loginname := this.GetString("loginname")
		baseresp := &mydata.BaseResp{}
		if loginname == "" {
			logs.Error("loginname:", loginname)
			baseresp.Error_code = 1
			baseresp.Msg = "用户名不能为空"
			this.Data["json"] = baseresp
			this.ServeJSON()
			this.StopRun()
			return
		}
		// logs.Info("prepare:", loginname)
		user := &mydb.TblAccount{}
		//user.AddUser()
		qsuser, count := user.GetUserSingle(loginname)
		if count != 1 {
			baseresp.Error_code = 1
			baseresp.Msg = "账号不存在"
			this.Data["json"] = baseresp
			this.ServeJSON()
			this.StopRun()
			return
		} else {
			baseresp.Error_code = 0
			baseresp.Msg = ""
			this.loginname = loginname
			//this.history()
			this.user = &qsuser
			// fmt.Println("qsuer:", qsuser)

			if this.Ctx.Request.URL.Path == "/login" {

			} else {
				this.checkToken()
			}
		}
	}
}

func (this *baseController) Finish() {
	//logs.Info("finish:", this.Ctx.Request.URL.Path)

	this.o = nil
	this.user = nil
	this.loginname = ""

}

func (this *baseController) getRemoteIp() string {
	remote_ip := strings.Split(this.Ctx.Request.RemoteAddr, ":")
	return remote_ip[0]
}

func (this *baseController) getRunInfo() string {
	port := strings.Split(this.Ctx.Request.RemoteAddr, ":")[1]
	pid := os.Getpid()
	info := fmt.Sprintf("pid:%d clientport:%s", pid, port)
	return info

}
func (this *baseController) getClientIP() string {
	ip := this.Ctx.Request.Header.Get("X-Forwarded-For")
	if strings.Contains(ip, "127.0.0.1") || ip == "" {
		ip = this.Ctx.Request.Header.Get("X-real-ip")
	}
	if ip == "" {
		return "127.0.0.1"
	}
	return ip
}

func (this *baseController) history() {
	// logs.Info("baseController history: ")
	remoteip := this.getClientIP()
	nowdatetime := time.Now()
	ndate := nowdatetime.Format(myfunc.Godate2)
	ntime := nowdatetime.Format(myfunc.Gotime2)
	tblhistory := &mydb.TblBrowsingHistory{}
	tblhistory.Browsing_date = ndate
	tblhistory.Browsing_time = ntime
	tblhistory.Request_method = this.Ctx.Request.Method
	tblhistory.User_ip = remoteip
	tblhistory.User_account = this.loginname
	tblhistory.Uri = this.Ctx.Request.URL.String()
	tblhistory.User_agent = this.Ctx.Request.UserAgent()
	//tblhistory.Status = this.Ctx.Request.Response.Status
	tblhistory.Status = "200"
	// logs.Info(tblhistory)
	id, err := this.o.Insert(tblhistory)
	if err == nil {
		// logs.Info("history add", id)
	} else {
		logs.Error(this.loginname, "history add error:", id, err)
	}
}

func (this *baseController) checkToken() {
	// logs.Info("user:", this.user)
	token := this.GetString("token")
	resp := mydata.BaseResp{}
	checkstatus := false
	if token == ""{
		resp.Error_code = 1
		resp.Msg = "无效token"
		this.Data["json"] = resp
		this.ServeJSON()
		this.StopRun()
		return
	}
	last_login_time := this.user.Last_logintime.Format(myfunc.Godatetime)
	minute_ago := myfunc.GetMintuesAgo(10)
	if token == this.user.Token {
		if minute_ago < last_login_time{
			checkstatus = true
		} else {
			resp.Msg = "登录过期，请重新登录"
			logs.Info("user:", this.user.Loginname , minute_ago, "check out last:", last_login_time)
		}
	} else {
		logs.Info("checkToken:", this.loginname, last_login_time, minute_ago, checkstatus)
		if minute_ago < last_login_time {
			resp.Error_code = 1
			resp.Msg = "账号在其他地方登录,如不是本人操作，请修改密码!"
			this.Data["json"] = resp
			this.ServeJSON()
			this.StopRun()
			return
		} else {
			//checkstatus = true
			resp.Msg = "登录过期，请重新登录"
		}
	}
	//logs.Info("checkToken:", this.loginname, last_login_time, minute_ago, checkstatus)
	if checkstatus{
		this.user.Last_logintime = myfunc.GetLocalTime()
		this.user.UpdateUser(this.user)
		this.history()
	} else {
		// logs.Error("user:", this.user)
		this.Data["json"] = resp
		this.ServeJSON()
		this.StopRun()
		return
	}

}
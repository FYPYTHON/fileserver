package mycontroller

import (
	"fmt"
	"github.com/astaxie/beego/logs"
	"io/ioutil"
	. "mydata"
	"myfunc"
	"os"
	"os/exec"
	"path"
	"runtime"
	"strings"
	"time"
)

type MainController struct {
	baseController
}

func (this *MainController) Get(){
	fmt.Println("tis", this.Ctx.Request.Method)
	fmt.Println(this.GetString("param"))
	fmt.Println(this.GetString(":param"))
	this.Ctx.WriteString("hello word")
}
func (this *MainController) Home() {
	fmt.Println(this.GetString("param"))
	fmt.Println(this.GetString(":param"))
	this.Ctx.WriteString( this.Ctx.Request.Method + " -> home" + "" +
		": param=" + this.GetString(":param"))
}

func GetDiskUsage(curpath string) string{
	realpath := path.Join(TOPPATH, curpath)
	cmd := exec.Command("/bin/bash", "/opt/midware/study/src/script/diskusage.sh", realpath)
	// fmt.Println(cmd.Args)

	sysType := runtime.GOOS
	if sysType != "linux"{
		return "暂无信息"
	}
	bytes, err := cmd.Output()
	if err != nil {
		logs.Error("cmd output:", err, "args:", cmd.Args)
		return "暂无信息"
	}
	return string(bytes)
}

func GetPath(filedir, action string)(files , dirs []string, err_msg string){
	realpath := path.Join(TOPPATH, filedir)
	if action == SUPER {
		realpath = path.Dir(realpath)
		fmt.Println(SUPER, realpath)
	}
	logs.Info("GetPath:", realpath)
	if _, err := os.Stat(realpath); err != nil {
		logs.Error(realpath, err)
		return nil, nil, "文件路径不存在"
	}

	lists, err := ioutil.ReadDir(realpath)
	if err != nil {
		logs.Error(realpath, err)
		return nil, nil, "获取文件列表失败"
	}

	for _, file := range lists {
		if file.IsDir() {
			dirs = append(dirs, file.Name())
		} else {
			files = append(files, file.Name())
		}
	}
	return files, dirs, ""
}
func (this *MainController) Login() {
	//userAccount := this.GetString("userAccount")
	password := this.GetString("password")
	inputCode := this.GetString("inputCode")
	//fmt.Println(userAccount, password, inputCode)
	//logs.Info(userAccount, password, inputCode)
	data := &LoginResp{}
	data.Error_code = 0
	data.Msg = ""
	data.Token = ""
	data.User = this.loginname
	md5pwd := myfunc.MD5(password)
	if inputCode != "APP" || !strings.Contains(this.Ctx.Request.UserAgent(), "Mobile"){
		//logs.Info(strings.Contains(this.Ctx.Request.UserAgent(), "Mobile"))
		//logs.Info(this.Ctx.Request.UserAgent())
		data.Error_code = 1
		data.Msg = "不支持登录"
		this.Data["json"] = data
		this.ServeJSON()
		this.StopRun()
	}
	if md5pwd != this.user.Password {
		data.Error_code = 1
		data.Msg = "账号或密码不正确"
		this.Data["json"] = data
		this.ServeJSON()
		this.StopRun()
	}
	data.Token = myfunc.MD5(time.Now().Local().String() + "APP" + this.user.Loginname)
	this.user.Token = data.Token
	// this.user.Register_time = time.Now().String()
	this.user.Last_logintime = myfunc.GetLocalTime()
	// fmt.Println("--", this.user.Last_logintime)
	ok := this.user.UpdateUser(this.user)
	if !ok {
		data.Error_code = 1
		data.Msg = "登录失败"
	} else {

	}
	this.Data["json"] = data
	this.ServeJSON()
}

func (this *MainController) FsMain(){
	curpath := this.GetString("curpath")
	action := this.GetString("action")
	logs.Info(curpath, action)
	files, dirs, err_msg := GetPath(curpath, action)
	data := &FsMainResp{}
	data.Msg = err_msg
	data.Curpath = curpath

	if err_msg == "" {
		data.Error_code = 0
	} else {
		data.Error_code = 1
	}
	if files == nil {
		data.Files = []string{}
	} else {
		data.Files = files
	}
	if dirs == nil {
		data.Dirs = []string{}
	} else {
		data.Dirs = dirs
	}

	data.Shortcut_list = []string{}
	data.Useage = GetDiskUsage(curpath)


	this.Data["json"] = data
	this.ServeJSON()
}

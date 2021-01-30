package mycontroller

import (
	"github.com/astaxie/beego/logs"
	. "mydata"
	"os"
	"path"
)

type DirController struct {
	baseController
}

// @router /app/dir [post]
func (this *DirController) Post(){
	logs.Info(this.Ctx.Request.URL, this.Ctx.Request.RemoteAddr,
		this.Ctx.Request.Method)
	newname := this.GetString("newname")
	curpath := this.GetString("curpath")

	real_newname := path.Join(TOPPATH, curpath, newname)
	baseresp := &BaseResp{}
	baseresp.Error_code = 1
	if newname == "" || curpath == "" {
		logs.Error(newname, curpath)
		baseresp.Msg = "参数错误，不能为空"
	} else if _, err := os.Stat(real_newname); err == nil {
		logs.Error(real_newname, err)
		baseresp.Msg = "文件目录已存在"
	} else {
		err = os.MkdirAll(real_newname, os.ModePerm)
		if err != nil {
			logs.Error(err)
			baseresp.Msg = "创建失败"
		} else {
			baseresp.Error_code = 0
		}
	}
	this.Data["json"] = baseresp
	this.ServeJSON()
}

// @router /app/dir [put]
func (this *DirController) Put(){
	logs.Info(this.Ctx.Request.URL, this.Ctx.Request.RemoteAddr,
		this.Ctx.Request.Method)
	newname := this.GetString("newname")
	oldname := this.GetString("oldname")
	curpath := this.GetString("curpath")

	real_newname := path.Join(TOPPATH, curpath, newname)
	real_oldname := path.Join(TOPPATH, curpath, oldname)
	baseresp := &BaseResp{}
	baseresp.Error_code = 1
	if newname == "" || curpath == "" || oldname == ""{
		logs.Error(newname, oldname, curpath)
		baseresp.Msg = "参数错误，不能为空"
	} else if _, err := os.Stat(real_newname); err == nil {
		logs.Error(real_newname, err)
		baseresp.Msg = newname + " 已存在"
	} else if _, err := os.Stat(real_oldname); err != nil {
		logs.Error(real_oldname, err)
		baseresp.Msg = oldname + " 不存在"
	} else {
		err = os.Rename(real_oldname, real_newname)
		if err != nil {
			logs.Error(err)
			baseresp.Msg = "重命名失败"
		} else {
			baseresp.Error_code = 0
		}
	}
	this.Data["json"] = baseresp
	this.ServeJSON()
}

// @router /app/dir [delete]
func (this *DirController) Delete(){
	logs.Info(this.Ctx.Request.URL, this.Ctx.Request.RemoteAddr,
		this.Ctx.Request.Method)
	filename := this.GetString("filename")
	curpath := this.GetString("curpath")

	real_newname := path.Join(TOPPATH, curpath, filename)
	baseresp := &BaseResp{}
	baseresp.Error_code = 1
	if filename == "" || curpath == "" {
		logs.Error(filename, curpath)
		baseresp.Msg = "参数错误，不能为空"
	} else if _, err := os.Stat(real_newname); err != nil {
		logs.Error(real_newname, err)
		baseresp.Msg = "文件目录不存在"
	} else {
		err = os.RemoveAll(real_newname)
		if err != nil {
			logs.Error(err)
			baseresp.Msg = "删除失败"
		} else {
			baseresp.Error_code = 0
		}
	}
	this.Data["json"] = baseresp
	this.ServeJSON()
}
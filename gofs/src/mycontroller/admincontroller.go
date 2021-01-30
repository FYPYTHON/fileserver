package mycontroller

import (
	"mydata"
	"mydb"
)

type AdminController struct {
	baseController
}

// @router /app/version [get]
func (this *AdminController) GetVersion() {
	tblversion := &mydb.TblAdmin{}
	version := tblversion.GetVersion()
	resp := mydata.VersionResp{}
	resp.Error_code = 1
	resp.Version = version
	if version == ""{
		resp.Msg = "获取版本失败"
	} else {
		resp.Error_code = 0
	}
	this.Data["json"] = resp
	this.ServeJSON()
}
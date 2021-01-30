package mydb

import (
	"github.com/astaxie/beego/logs"
	"github.com/astaxie/beego/orm"
)

type TblAdmin struct {
	Id       int64   `orm:"unique"`
	Name     string
	Value    string
	Type     int
}

func (tbl *TblAdmin) TableName() string {
	return "tbl_admin"
}

func (tbl *TblAdmin) GetVersion() string {
	o := orm.NewOrm()
	qs := o.QueryTable(tbl).Filter("name", "appversion")
	versioninfo := TblAdmin{}
	err := qs.One(&versioninfo)
	if err == nil {
		logs.Info("GetVersion:", versioninfo.Value)
	} else {
		logs.Error(err)
	}
	return versioninfo.Value
}
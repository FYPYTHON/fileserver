package mydb

import (
	"github.com/astaxie/beego/logs"
	"github.com/astaxie/beego/orm"
)

type TblBrowsingHistory struct {
	Id  int64      `orm:"unique"`
	User_ip string
	User_account string
	Uri string
	Request_method string
	Status string
	Browsing_date string
	Browsing_time string
	User_agent string
}

func (h *TblBrowsingHistory) TableName() string {
	return "tbl_browsing_history"
}

func (h *TblBrowsingHistory) GetHistoryList(limit, page int)[]orm.Params {
	if page < 1{
		page = 1
	}
	o := orm.NewOrm()
	qs := o.QueryTable(h)
	qs = qs.Limit(limit).Offset((page-1) * limit)
	cnt, err := qs.Count()
	logs.Info("sq ,count:", cnt, err)
	var maps []orm.Params
	num, err := qs.Values(&maps)
	if err == nil {
		logs.Info("History List Result Nums: %d\n", num)
	}
	return maps
}
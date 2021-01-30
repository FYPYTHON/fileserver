package mydb

import (
	"github.com/astaxie/beego/logs"
	"github.com/astaxie/beego/orm"
	"time"
)

// https://www.cnblogs.com/show58/p/12377946.html

type TblAccount struct {
	Id				int64    `orm:"unique"`
	Loginname		string   `orm:"unique;size(20)"`
	Nickname		string
	Password 		string
	Email 			string
	Userstate       int
	Userrole        int
	Register_time   string
	Token 			string
	Last_logintime  time.Time   `orm:"type(datetime)"`

}

func (this *TblAccount) UpdateUser(user *TblAccount)bool{
	o := orm.NewOrm()
	num, err := o.Update(user)
	if err != nil {
		logs.Error("UpdateUser", num, err)
		return false
	} else {
		return true
	}
}

func (this *TblAccount) AddUser(user *TblAccount) (int, string){
	logs.Info("AddUser :", user.Loginname)
	error_code, msg := 0, ""
	o := orm.NewOrm()
	id, err := o.Insert(user)
	if err == nil {
		logs.Info(user.Loginname , id, "add success")
		error_code = 0
	} else {
		logs.Error(user.Loginname, err)
		error_code = 1
		msg = err.Error()
	}
	return error_code, msg
}

func (user *TblAccount) GetUserList(limit, page int)[]orm.Params {
	o := orm.NewOrm()
	if page < 1{
		page = 1
	}
	//qs := o.QueryTable(user).Filter("Loginname", loginname)
	qs := o.QueryTable(user)
	qs = qs.Limit(limit).Offset((page-1) * limit)
	cnt, err := qs.Count()
	logs.Info("sq ,count:", cnt, err)
	var maps []orm.Params
	num, err := qs.Values(&maps)
	if err == nil {
		logs.Info("User List Result Nums: %d\n", num)
		//for _, m := range maps {
		//	logs.Info(m)
		//}
	}
	return maps
}

func (user *TblAccount) GetUserSingle(loginname string) (TblAccount, int64){
	o := orm.NewOrm()
	//qs := o.QueryTable(user).Filter("Loginname", loginname)
	u := TblAccount{}
	qs := o.QueryTable(&user)
	qs = qs.Filter("Loginname", loginname)
	count, errc := qs.Count()
	if errc != nil {
		logs.Error("GetUserSingle error:", errc)
	}
	if count < 1 {
		logs.Error("GetUserSingle no user count:", count)
	}
	err := qs.One(&u)
	if err == nil {
		//logs.Info("GetUserSingle:", u.Loginname)
	} else {
		logs.Error(err)
	}

	//qs.Limit(10)
	return u, count
}

func (user *TblAccount) GetUserByid(uid int) (TblAccount, int64){
	o := orm.NewOrm()
	//qs := o.QueryTable(user).Filter("Loginname", loginname)
	u := TblAccount{}
	qs := o.QueryTable(&user)
	qs = qs.Filter("Id", uid)
	count, errc := qs.Count()
	if errc != nil {
		logs.Error("GetUserSingle error:", errc)
	}
	if count < 1 {
		logs.Error("GetUserSingle no user count:", count)
	}
	err := qs.One(&u)
	if err == nil {
		logs.Info("GetUserSingle:", u)
	} else {
		logs.Error(err)
	}
	//qs.Limit(10)
	return u, count
}

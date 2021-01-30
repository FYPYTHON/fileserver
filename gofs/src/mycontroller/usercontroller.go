package mycontroller

import (
	"github.com/astaxie/beego/logs"
	"github.com/astaxie/beego/orm"
	. "mydata"
	"mydb"
	"myfunc"
	"strconv"
	"time"
)
type UserController struct {
	baseController
}

// @router /user/:uid [put]
func (this *UserController) Put(){
	logs.Info(this.Ctx.Request.URL, this.Ctx.Request.RemoteAddr,
		this.Ctx.Request.Method)
	id, err := this.GetInt(":uid")
	Nickname := this.GetString("nickname")
	Email := this.GetString("email")
	password := this.GetString("password")
	if err != nil {
		logs.Error(id, err)
		this.Data["json"] = BaseResp{Error_code:1,Msg:"参数错误"}
	} else {
		user := &mydb.TblAccount{}
		data, count := user.GetUserByid(id)
		if count != 1 {
			this.Data["json"] = BaseResp{Error_code:1,Msg:"用户信息获取失败"}
		} else {
			data.Nickname = Nickname
			data.Email = Email
			data.Password = myfunc.MD5(password)
			o := orm.NewOrm()
			num, err := o.Update(&data)
			if err != nil {
				logs.Error(num, err)
				this.Data["json"] = BaseResp{Error_code:1,Msg:"用户信息修改失败"}
			} else {
				this.Data["json"] = BaseResp{Error_code:0,Msg:"用户信息修改成功"}
			}
		}
	}
	this.ServeJSON()
}

// @router /user/:uid [delete]
func (this *UserController) Delete() {
	logs.Info(this.Ctx.Request.URL, this.Ctx.Request.RemoteAddr,
		this.Ctx.Request.Method)
	id, err := this.GetInt(":uid")
	if err != nil {
		logs.Error(id, err)
		this.Data["json"] = BaseResp{Error_code:1,Msg:"参数错误"}
	} else {
		o := orm.NewOrm()
		num, err := o.QueryTable(&mydb.TblAccount{}).Filter("Id", id).Delete()
		if err != nil {
			logs.Error(num, err)
			this.Data["json"] = BaseResp{Error_code:1,Msg:"删除失败"}
		} else {
			this.Data["json"] = BaseResp{Error_code:0,Msg:"删除成功"}
		}
	}
	this.ServeJSON()
}

// @router /user [post]
func (this *UserController) Post(){
	logs.Info(this.Ctx.Request.URL, this.Ctx.Request.RemoteAddr,
		this.Ctx.Request.Method)
	newuser := &mydb.TblAccount{}
	newuser.Loginname = this.GetString("loginname")
	newuser.Nickname = this.GetString("nickname")
	newuser.Email = this.GetString("email")
	password := this.GetString("password")
	newuser.Password = password
	newuser.Register_time = time.Now().Format(myfunc.Godatetime)
	newuser.Userrole = 0
	newuser.Userstate = 0
	st := strconv.FormatInt(time.Now().UnixNano(),10)
	// fmt.Println(st)
	newuser.Token = myfunc.MD5(st)
	newuser.Last_logintime = time.Now()
	resp := BaseResp{}

	if newuser.Loginname == "" || newuser.Nickname == "" ||
		newuser.Email == "" || newuser.Password == "" {
		logs.Error(newuser)
		resp.Error_code = 1
		resp.Msg = "参数不能为空"
	} else {
		newuser.Password = myfunc.MD5(password)
		o_user, num := newuser.GetUserSingle(newuser.Loginname)
		if num == 1 && o_user.Loginname == newuser.Loginname{
			resp.Error_code = 1
			resp.Msg = "用户已存在"
		} else {
			error_code, msg := newuser.AddUser(newuser)
			resp.Error_code = error_code
			resp.Msg = msg
		}
	}
	this.Data["json"] = resp
	this.ServeJSON()
}

// @router /user [get]
func (this *UserController) Get(){
	logs.Info(this.Ctx.Request.URL, this.Ctx.Request.RemoteAddr,
		this.Ctx.Request.Method)
	user := &mydb.TblAccount{}
	//user.AddUser()
	loginname := this.GetString("loginname")
	datas, count := user.GetUserSingle(loginname)

	resp := &UserResp{}
	if count < 1 {
		resp.Error_code = 1
		resp.Msg = "用户信息查询失败"
	} else {
		resp.Error_code = 0
		resp.Msg = ""
		resp.User = datas
	}
	this.Data["json"] = resp
	this.ServeJSON()
}


// @router /user/:page [get]
func (this *UserController) GetAll(){
	logs.Info(this.Ctx.Request.URL, this.Ctx.Request.RemoteAddr,
		this.Ctx.Request.Method)
	user := &mydb.TblAccount{}
	//user.AddUser()
	page, err := this.GetInt(":uid")
	if err != nil {
		logs.Error(page, err)
		this.Data["json"] = BaseResp{Error_code:1,Msg:"参数错误"}
	} else {
		datas := user.GetUserList(PageSize, page)

		resp := &UserListResp{}
		resp.UserList = datas
		resp.Error_code = 0
		resp.Msg = ""
		this.Data["json"] = resp
	}
	this.ServeJSON()
}
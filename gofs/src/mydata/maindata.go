package mydata

import (
	"github.com/astaxie/beego/orm"
	"mydb"
)

type BaseResp struct {
	Error_code int
	Msg 	   string
}

type VersionResp struct {
	BaseResp
	Version string
}
type LoginResp struct {
	BaseResp
	Token 	   string
	User 	   string
}

type FsMainResp struct {
	BaseResp
	Dirs 	  []string
	Files     []string
	Curpath   string
	Shortcut_list []string
	Useage    string
}

type UserResp struct {
	User mydb.TblAccount
	BaseResp
}

type UserListResp struct {
	UserList []orm.Params
	BaseResp
}

type HistoryListResp struct {
	HistoryList []orm.Params
	BaseResp
}
type PlayResp struct {
	BaseResp
	Vsrc string
	Img  string
	Type string
	Index int
	Nowfile string
}

type JiJinData struct {
	Jdate []string
	Jvalue []string
	Jmax   string
	Jmin   string
	Monday string
	Sunday string
}

type JiJinResp struct {
	BaseResp
	Jdata JiJinData
	Jdata0 JiJinData
	Jdata1 JiJinData
	Jid    string
	Jids   []string
}


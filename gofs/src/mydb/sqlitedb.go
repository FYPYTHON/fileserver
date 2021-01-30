package mydb

import (
	"github.com/astaxie/beego/orm"
	_ "github.com/mattn/go-sqlite3"
	"runtime"
)

func init(){
	//dbhost := beego.AppConfig.String("dbhost")
	//dbport := beego.AppConfig.String("dbport")
	//dbuser := beego.AppConfig.String("dbuser")
	//dbpassword := beego.AppConfig.String("dbpassword")
	//dbname := beego.AppConfig.String("dbname")

	_ = orm.RegisterDriver("sqlite", orm.DRSqlite)
	sysType := runtime.GOOS
	if sysType != "linux"{
		//_ = orm.RegisterDataBase("default", "sqlite3", "D:/project/notes/FSTornado/wfs.db")
		_ = orm.RegisterDataBase("default", "sqlite3",
			"D:\\workSpace\\go\\study\\src\\wfs.db")
	} else {
		// linux env use wfs.db (was shared with python)
		//_ = orm.RegisterDataBase("default", "sqlite3", "/opt/midware/FSTornado/wfs.db")
		_ = orm.RegisterDataBase("default", "sqlite3","/opt/midware/study/src/wfs.db")


	}
	orm.RegisterModel(new(TblAccount), new(TblBrowsingHistory), new(TblJijin),
		new(TblAdmin))
	_ = orm.RunSyncdb("default", false, false)
}


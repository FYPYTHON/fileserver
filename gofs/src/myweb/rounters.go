package myweb

import (
	"github.com/astaxie/beego"
	. "mycontroller"
)
func init()  {
	beego.Router("/pass", &PassController{}, "get:Get")
	beego.Router("/index/:param", &MainController{}, "*:Get")
	beego.Router("/home/:param", &MainController{}, "*:Home")
	beego.Router("/login", &MainController{}, "post:Login")
	beego.Router("/app/fsmain", &MainController{}, "get:FsMain")
	beego.Router("/app/user", &UserController{}, "get:Get;post:Post")
	beego.Router("/app/user/:uid", &UserController{}, "get:GetAll;put:Put;delete:Delete")
	beego.Router("/app/dir", &DirController{}, "post:Post;put:Put;delete:Delete")
	beego.Router("/app/play/:filename", &ImageVideoController{}, "get:Get;post:Post")
 	beego.Router("/app/history", &ViewController{}, "get:Get")
	beego.Router("/app/view", &ViewController{}, "get:GetAll;post:Post")
	beego.Router("/app/version", &AdminController{}, "get:GetVersion")
	beego.Router("/download", &DownLoadController{}, "get:Get;post:Post")
	beego.Router("/app/upload", &UpLoadController{},"post:Post")
	beego.Router("/app/uploadlist", &UpLoadController{}, "post:UploadList")
	// (?P<filename>.*)  /app/play/?:filename
}

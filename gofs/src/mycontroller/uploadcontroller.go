package mycontroller

import (
	"github.com/astaxie/beego/logs"
	"io"
	"io/ioutil"
	"mydata"
	"net/http"
	"os"
	"path"
)

type UpLoadController struct {
	baseController
}

type DownLoadController struct {
	baseController
}

// @router /download [get]
func (this *DownLoadController) Get() {
	filename := this.GetString("filename")
	logs.Info("download:", filename)
	real_file := path.Join(mydata.TOPPATH, filename)
	resp := mydata.BaseResp{}
	fname := path.Base(real_file)
	//dir := path.Dir(real_file)
	if _, err := os.Stat(real_file); err != nil {
		logs.Error(real_file, err)
		resp.Msg = "文件不存在"
		resp.Error_code = 1
		this.Data["json"] = resp
		this.ServeJSON()
	} else {
		//this.Ctx.Output.Download(mydata.TOPPATH + "/" + dir, fname)
		// logs.Info(dir, fname, real_file)
		//this.Ctx.Output.Download(dir, fname)
		fn := "filename=" + fname
		this.Ctx.Output.Header("Content-Disposition", "attachment; "+fn)
		this.Ctx.Output.Header("Content-Description", "File Transfer")
		this.Ctx.Output.Header("Content-Type", "application/octet-stream")
		this.Ctx.Output.Header("Content-Transfer-Encoding", "binary")
		this.Ctx.Output.Header("Expires", "0")
		this.Ctx.Output.Header("Cache-Control", "must-revalidate")
		this.Ctx.Output.Header("Pragma", "public")
		http.ServeFile(this.Ctx.Output.Context.ResponseWriter, this.Ctx.Output.Context.Request, real_file)
		//this.StopRun()
	}
}

func (this *DownLoadController) Post(){
	filename := this.GetString("filename")
	real_file := path.Join(mydata.TOPPATH, filename)
	resp := mydata.BaseResp{}
	if _, err := os.Stat(real_file); err != nil {
		logs.Error(real_file, err)
		resp.Msg = "文件不存在"
		resp.Error_code = 1
	} else {
		file, err := os.Open(real_file)
		defer file.Close()
		if err != nil {
			resp.Msg = "文件打开失败"
			resp.Error_code = 1
		} else {
			fd, err := ioutil.ReadAll(file)
			if err != nil {
				resp.Msg = "文件读取失败"
				resp.Error_code = 1
			} else {
				resp.Error_code = 0
				fcontent := string(fd)
				this.Ctx.WriteString(fcontent)
				//logs.Info(len(fd))
				//for i:=0; i * 2048 < len(fd) ; i++{
				//	logs.Info(i, len(fd))
				//	start:= i * 2048
				//	end := (i+1) * 2048
				//	if end > len(fd){
				//		end = len(fd) -1
				//	}
				//	this.Ctx.WriteString(fcontent[start: end])
				//}

				//this.StopRun()
			}
		}
	}
	this.Data["json"] = resp
	this.ServeJSON()
}

func (this *UpLoadController) Post() {
	file, head, err := this.GetFile("file")
	curpath := this.GetString("curpath")
	resp := mydata.BaseResp{}
	resp.Error_code = 1
	if err != nil {
		logs.Error(err)
		resp.Msg = "获取文件失败"
		this.Data["json"] = resp
		this.ServeJSON()
		this.StopRun()
		return
	}
	defer file.Close()

	realpath := path.Join(mydata.TOPPATH, curpath)
	filename := head.Filename
	if _, err := os.Stat(realpath); err != nil {
		logs.Error(realpath, err)
		resp.Msg = "文件目录不存在"
	} else if _, err := os.Stat(realpath + "/" + filename); err == nil {
		logs.Error(realpath,filename, "is exist")
		resp.Msg = "文件已存在"
	} else {
		err = this.SaveToFile("file", realpath + "/" + filename)
		if err != nil {
			logs.Error("upload fail:", filename, err)
			resp.Msg = filename + "上传失败."
		} else {
			resp.Error_code = 1
			resp.Msg = filename + "上传成功"
		}
	}
	this.Data["json"] = resp
	this.ServeJSON()
}

func (this *UpLoadController) UploadList(){
	// logs.Info(this.Ctx.Request.MultipartForm.File)
	files, err := this.GetFiles("files")
	curpath := this.GetString("curpath")
	resp := mydata.BaseResp{}
	resp.Error_code = 1
	if err != nil {
		logs.Error(err)
		resp.Msg = "获取文件失败"
		this.Data["json"] = resp
		this.ServeJSON()
		this.StopRun()
		return
	}
	realpath := path.Join(mydata.TOPPATH, curpath)
	if _, err := os.Stat(realpath); err != nil {
		logs.Error(realpath, err)
		resp.Msg = curpath + "文件目录不存在"
		this.Data["json"] = resp
		this.ServeJSON()
		this.StopRun()
		return
	}
	resp.Error_code = 0
	msgch := make(chan string)
	for i, _ := range files {

		filename := files[i].Filename
		realpath := path.Join(mydata.TOPPATH, curpath)
		file, err := files[i].Open()
		defer file.Close()
		if err != nil {
			resp.Msg = resp.Msg + files[i].Filename + "获取文件失败" + "\n"
			resp.Error_code = 1
		}
		//
		go this.processfile(file,realpath, filename, &resp, msgch)
		//
		//if _, err := os.Stat(realpath + "/" + filename); err == nil {
		//	logs.Error(realpath, filename, "is exist")
		//	resp.Msg = resp.Msg + filename + "文件已存在" + "\n"
		//	resp.Error_code = 1
		//} else {
		//	dst, err := os.Create(realpath + "/" + filename)
		//	defer dst.Close()
		//	if err != nil {
		//		resp.Msg = resp.Msg + filename + "文件保存失败." + "\n"
		//		resp.Error_code = 1
		//	}
		//
		//	if _, err := io.Copy(dst, file);err != nil {
		//		logs.Error("upload fail:", realpath, filename, err)
		//		resp.Msg = resp.Msg + filename + "上传失败." + "\n"
		//		resp.Error_code = 1
		//	} else {
		//		logs.Info(filename, "上传成功")
		//		resp.Msg = resp.Msg + filename + "上传成功" + "\n"
		//		//this.Data["json"] = `{"Error_code": 0, "Msg":`+ filename+` 上传成功}`
		//		//this.ServeJSON()
		//	}
		//}
	}
	// msg chan
	for i:= 0; i < len(files); i++ {
		//<- msgch
		msg := <- msgch
		resp.Msg += msg
	}

	if resp.Error_code == 1{
		logs.Error(resp.Msg)
	}
	this.Data["json"] = resp
	this.ServeJSON()
}


func (this *UpLoadController) processfile(file io.Reader,realpath, filename string,
	  resp *mydata.BaseResp, msgch chan string){
	if _, err := os.Stat(realpath + "/" + filename); err == nil {
		logs.Error(realpath, filename, "is exist", os.Getpid())
		//resp.Msg = resp.Msg + filename + "文件已存在" + "\n"
		resp.Error_code = 1
		msgch <- filename + "文件已存在" + "\n"
	} else {
		dst, err := os.Create(realpath + "/" + filename)
		defer dst.Close()
		if err != nil {
			//resp.Msg = resp.Msg + filename + "文件保存失败." + "\n"
			logs.Error("文件保存失败:", realpath, filename, err)
			resp.Error_code = 1
			msgch <- filename + "文件保存失败." + "\n"
		}
		//err = this.SaveToFile("files", realpath + "/" +filename)
		//if err != nil {
		if _, err := io.Copy(dst, file);err != nil {
			logs.Error("upload fail:", realpath, filename, err)
			//resp.Msg = resp.Msg + filename + "上传失败." + "\n"
			resp.Error_code = 1
			msgch <- filename + "上传失败." + "\n"
		} else {
			logs.Info(filename, "上传成功")
			//resp.Msg = resp.Msg + filename + "上传成功" + "\n"
			msgch <- filename + "上传成功" + "\n"
		}
	}
}


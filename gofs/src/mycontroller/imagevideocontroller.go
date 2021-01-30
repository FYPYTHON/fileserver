package mycontroller

import (
	"bytes"
	"encoding/base64"
	"github.com/astaxie/beego/logs"
	"github.com/nfnt/resize"
	"image"
	"image/jpeg"
	"io/ioutil"
	"mydata"
	"os"
	"path"
	"strings"
)

type ImageVideoController struct {
	baseController
}

func ImageResize(filename string) string{
	//"E:\\IMG_20190503_123846.jpg"
	file, err := os.Open(filename)
	if err != nil {
		logs.Error(err)
		return ""
	}
	defer file.Close()
	f, err := file.Stat()
	if err == nil {
		logs.Info("file size:", f.Size())
	}
	img, err := jpeg.Decode(file)
	if err != nil {
		logs.Error(err)
		return ""
	}
	// m := resize.Resize(100, 100, img, resize.Lanczos3)
	m := resize.Thumbnail(30,30, img ,resize.Lanczos3)
	// save file
	out, err := os.Create("testresize.jpg")
	if err != nil {
		logs.Error(err)
		return ""
	}
	_ = jpeg.Encode(out, m, nil)
	defer out.Close()

	// base64
	emptyBuff := bytes.NewBuffer(nil)
	_ = jpeg.Encode(emptyBuff, m, nil)
	//dist := make([]byte, 5000)
	//rlen := myfunc.GetImageBaseResize(len(emptyBuff.Bytes()))
	dist := make([]byte, len(emptyBuff.Bytes()) * 2)
	//dist := make([]byte, len(emptyBuff.Bytes()) * 4 / 3 + 2)
	//dist := []byte{}
	//println(len(dist), len(emptyBuff.Bytes()), rlen)
	base64.StdEncoding.Encode(dist, emptyBuff.Bytes())
	//_, _ = fmt.Println(cap(dist), len(dist))
	dist = bytes.Trim(dist, "\x00")
	logs.Info(cap(dist), len(dist))
	return string(dist)
}

func ImageNext(filename string) string{
	//"E:\\IMG_20190503_123846.jpg"
	file, err := os.Open(filename)
	if err != nil {
		logs.Error(err)
		return ""
	}
	defer file.Close()
	f, err := file.Stat()
	if err == nil {
		size := f.Size() / 1024 / 1024
		if size <= 0{
			size = f.Size() / 1024
			logs.Info("file size: %v%v", f.Size()/1024/1024, "K")
		} else {
			logs.Info("file size: %v%v", f.Size()/1024/1024, "M")
		}
		logs.Info("%v %v", 1/0.3, 2)
	}
	img, err := jpeg.Decode(file)
	if err != nil {
		logs.Error(err)
		return ""
	}
	// m := resize.Resize(100, 100, img, resize.Lanczos3)
	m := resize.Thumbnail(600,600, img ,resize.Lanczos3)
	// save file
	out, err := os.Create("testresize.jpg")
	if err != nil {
		logs.Error(err)
		return ""
	}
	_ = jpeg.Encode(out, m, nil)
	defer out.Close()

	// base64
	emptyBuff := bytes.NewBuffer(nil)
	_ = jpeg.Encode(emptyBuff, m, nil)
	//dist := make([]byte, 5000)
	//rlen := myfunc.GetImageBaseResize(len(emptyBuff.Bytes()))
	dist := make([]byte, len(emptyBuff.Bytes()) * 2)
	//dist := make([]byte, len(emptyBuff.Bytes()) * 4 / 3 + 2)
	//dist := []byte{}
	//println(len(dist), len(emptyBuff.Bytes()), rlen)
	base64.StdEncoding.Encode(dist, emptyBuff.Bytes())
	//_, _ = fmt.Println(cap(dist), len(dist))
	dist = bytes.Trim(dist, "\x00")
	logs.Info("image base64:", cap(dist), len(dist))
	return string(dist)
}

func ImageSub(){
	ff, _ := ioutil.ReadFile("E:\\IMG_20190503_123846.jpg")       //我还是喜欢用这个快速读文件
	bbb := bytes.NewBuffer(ff)
	m,_,_ :=image.Decode(bbb)
	rgbImg := m.(*image.YCbCr)
	subImg := rgbImg.SubImage(image.Rect(0, 0, 200, 200)).(*image.YCbCr)
	f, _ := os.Create("test.jpg")   //创建文件
	defer f.Close()                 //关闭文件
	_ = jpeg.Encode(f, subImg, nil) //写入文件
}

// @router /app/play/:filename [get]
func (this *ImageVideoController) Get(){
	logs.Info(this.Ctx.Request.URL, this.Ctx.Request.RemoteAddr,
		this.Ctx.Request.Method)
	filename := this.GetString("filename")
	curpath := this.GetString("curpath")
	real_name := path.Join(mydata.TOPPATH, curpath, filename)
	logs.Info("filename:", filename, "curpath:", curpath)
	baseresp := &mydata.PlayResp{}
	baseresp.Error_code = 1
	if filename == ""  || curpath == ""{
		logs.Error(filename, curpath)
		baseresp.Msg = "参数错误，不能为空"
		this.Data["json"] = baseresp
		this.ServeJSON()
		this.StopRun()
		return
	}

	if _, err := os.Stat(real_name); err != nil {
		logs.Error(real_name, err)
		baseresp.Msg = "文件不存在"
		this.Data["json"] = baseresp
		this.ServeJSON()
		this.StopRun()
		return
	}
	sufix := path.Ext(filename)[1:]
	sufix = strings.ToLower(sufix)
	baseresp.Type = sufix
	if !(sufix == "jpg" || sufix == "png" || sufix == "jpeg" || sufix == "gif") {
		baseresp.Msg = filename + "文件格式错误(仅支持.png,.jpg,.gif,.jpeg)"
		logs.Error(baseresp.Msg)
	} else {
		baseresp.Error_code = 0
		baseresp.Img = ImageResize(real_name)
	}
	this.Data["json"] = baseresp
	this.ServeJSON()
}

// @router /app/play/:filename [post]
func (this *ImageVideoController) Post(){
	action := this.GetString("action", "next")
	filename := this.GetString(":filename", "")
	curpath := this.GetString("curpath", "")
	index, _ := this.GetInt("index", 0)
	ftype := this.GetString("ftype", "")
	real_name := path.Join(mydata.TOPPATH, curpath)
	logs.Info("filename:", filename, "curpath:", curpath, "index:", index, "ftype:", ftype, "action", action)
	baseresp := &mydata.PlayResp{}
	baseresp.Error_code = 1
	if curpath == "" || ftype == ""{
		baseresp.Msg = "参数错误"
		this.Data["json"] = baseresp
		this.ServeJSON()
		this.StopRun()
	}
	if _, err := os.Stat(real_name);err != nil {
		baseresp.Msg = filename + " 文件目录不存在"
		this.Data["json"] = baseresp
		this.ServeJSON()
		this.StopRun()
	}
	if action == "next" {
		index += 1
	} else {
		index -= 1
	}
	filelist, _, _ := GetPath(curpath, "keep")
	logs.Info("files length:", len(filelist), "curindex:", index)
	if index >= len(filelist) && action == "next"{
		baseresp.Msg = "最后一张"
		baseresp.Error_code = 1
		this.Data["json"] = baseresp
		this.ServeJSON()
		this.StopRun()
	}
	if index <= 0 && action == "previous"{
		baseresp.Msg = "第一张"
		baseresp.Error_code = 1
		this.Data["json"] = baseresp
		this.ServeJSON()
		this.StopRun()
	}
	nowfile := path.Join(curpath, filelist[index])
	real_file := path.Join(mydata.TOPPATH, nowfile)
	sufix := path.Ext(filename)[1:]
	sufix = strings.ToLower(sufix)
	if !(sufix == "jpg" || sufix == "png" || sufix == "jpeg" || sufix == "gif") {
		baseresp.Msg = filename + "文件格式错误(仅支持.png,.jpg,.gif,.jpeg)"
	} else {
		baseresp.Error_code = 0
		baseresp.Img = ImageNext(real_file)
		baseresp.Nowfile = nowfile
		baseresp.Index = index
	}
	this.Data["json"] = baseresp
	this.ServeJSON()
}
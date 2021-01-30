package mycontroller

import (
	"fmt"
	"github.com/astaxie/beego/logs"
	"math"
	"mydata"
	"mydb"
	"myfunc"
	"strconv"
)

type ViewController struct {
	baseController
}

func getListMinAndMax(data []string) (m, x string) {

	min, max := math.MaxFloat64, 0.0
	for i := 0; i < len(data); i++ {
		if data[i] == ""{
			continue
		}
		if vv, err :=strconv.ParseFloat(data[i], 64); err ==nil {
			// fmt.Println(vv, data[i], min, max)
			if vv > max{
				max = vv
			}
			if vv < min {
				min = vv
			}
		} else {
			fmt.Println(err)
		}
	}
	return strconv.FormatFloat(min, 'f', 4, 64),strconv.FormatFloat(max, 'f', 4, 64)
}

func (this *ViewController) Get(){
	logs.Info("ViewController: Get")
	historydb := &mydb.TblBrowsingHistory{}
	page, err := this.GetInt("page")
	hlresp := mydata.HistoryListResp{}
	if err != nil {
		hlresp.Msg = "参数错误"
		hlresp.Error_code = 1
		this.Data["json"] = hlresp
		this.ServeJSON()
		this.StopRun()
		return
	}
	datas := historydb.GetHistoryList(mydata.PageHistorySize, page)
	hlresp.HistoryList = datas
	this.Data["json"] = hlresp
	this.ServeJSON()
}

func (this *ViewController) Post(){
	jid := this.GetString("jid")
	jdate := this.GetString("jdate")
	jvalue := this.GetString("jvalue")
	tbljijin := mydb.TblJijin{}
	resp := mydata.BaseResp{}
	// logs.Info(jid, jdate, jvalue)
	if !myfunc.CheckStringInter(jvalue){
		resp.Msg = "参数错误：" + jvalue
		resp.Error_code = 1
		this.Data["json"] = resp
		this.ServeJSON()
		return
	}
	if !myfunc.CheckDate(jdate){
		resp.Msg = "参数错误,时间格式为：" + myfunc.Godate
		resp.Error_code = 1
		this.Data["json"] = resp
		this.ServeJSON()
		return
	}
	err := this.o.QueryTable(&tbljijin).Filter("jid", jid).Filter("jdate", jdate).One(&tbljijin)
	if err == nil {
		// logs.Info(tbljijin)
		res := tbljijin.UpdateJijin(this.o)
		if res {
			resp.Msg = "更新成功"
		} else {
			resp.Msg = "更新失败"
		}

	} else {
		tbljijin.Jid = jid
		tbljijin.Jdate = jdate
		tbljijin.Jvalue = jvalue
		err_code, msg := tbljijin.AddJijin(&tbljijin)
		resp.Error_code = err_code
		resp.Msg = msg
		logs.Error(err)
	}
	this.Data["json"] = resp
	this.ServeJSON()
}

func (this *ViewController) GetAll(){
	jid := this.GetString("jid")
	all := this.GetString("all")
	resp := mydata.JiJinResp{}
	resp.Error_code = 1
	if jid == "" {
		logs.Error(jid)
		resp.Msg = "参数错误"
		this.Data["json"] = resp
	} else {
		resp.Jid = jid
		tbljijin := &mydb.TblJijin{}
		gids := tbljijin.GetGids()
		resp.Jids = gids
		if all == "all" {
			jdate, jvalue := tbljijin.GetAllData(jid, 30)
			resp.Jdata.Jdate = jdate
			resp.Jdata.Jvalue = jvalue
			min, max := getListMinAndMax(jvalue)
			resp.Jdata.Jmin = min
			resp.Jdata.Jmax = max
			//fmt.Println(resp.Jdata)
		} else {
			// jdata0
			jdate0, jvalue0, monday0, sunday0 := tbljijin.GetRangeData(jid, 3)
			resp.Jdata0.Jdate = jdate0
			resp.Jdata0.Jvalue = jvalue0
			resp.Jdata0.Monday = monday0
			resp.Jdata0.Sunday = sunday0
			min0, max0 := getListMinAndMax(jvalue0)
			resp.Jdata0.Jmin = min0
			resp.Jdata0.Jmax = max0
			//fmt.Println(resp.Jdata0)

			// jdata0
			jdate1, jvalue1, monday1, sunday1 := tbljijin.GetRangeData(jid, 1)
			resp.Jdata1.Jdate = jdate1
			resp.Jdata1.Jvalue = jvalue1
			resp.Jdata1.Monday = monday1
			resp.Jdata1.Sunday = sunday1
			min1, max1 := getListMinAndMax(jvalue0)
			resp.Jdata1.Jmin = min1
			resp.Jdata1.Jmax = max1
			//fmt.Println(resp.Jdata1)
		}
		resp.Error_code = 0
		resp.Msg = ""
	}
	this.Data["json"] = resp
	this.ServeJSON()
}

func (this *ViewController) GetAllData(){
	jid := this.GetString("jid")
	resp := mydata.JiJinResp{}
	resp.Error_code = 1
	if jid == "" {
		logs.Error(jid)
		resp.Msg = "参数错误"
		this.Data["json"] = resp
	} else {
		resp.Jid = jid
		tbljijin := &mydb.TblJijin{}
		gids := tbljijin.GetGids()
		resp.Jids = gids
		// jdata0
		jdate, jvalue := tbljijin.GetAllData(jid, 30)
		resp.Jdata.Jdate = jdate
		resp.Jdata.Jvalue = jvalue
		min, max := getListMinAndMax(jvalue)
		resp.Jdata.Jmin = min
		resp.Jdata.Jmax = max
		fmt.Println(resp.Jdata0)

		resp.Error_code = 0
		resp.Msg = ""
	}
	this.Data["json"] = resp
	this.ServeJSON()
}

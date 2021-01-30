package mydb

import (
	"github.com/astaxie/beego/logs"
	"github.com/astaxie/beego/orm"
	"myfunc"
)

type TblJijin struct {
	Id     int64    `orm:"unique"`
	Jid    string
	Jdate  string
	Jvalue string
}


func (tbl *TblJijin) TableName() string{
	return "tbl_jijin"
}

func (this *TblJijin) AddJijin(jijin *TblJijin) (int, string){
	logs.Info("AddJijin :", jijin.Jid, jijin.Jdate)
	error_code, msg := 0, ""
	o := orm.NewOrm()
	id, err := o.Insert(jijin)
	if err == nil {
		logs.Info(jijin.Jid, jijin.Jdate , id, "add success")
		error_code = 0
		msg = "添加成功"
	} else {
		logs.Error(jijin.Jid, jijin.Jdate, err)
		error_code = 1
		msg = err.Error()
	}
	return error_code, msg
}
func (tbl *TblJijin) UpdateJijin(o orm.Ormer) bool {
	num, err := o.Update(tbl)
	if err != nil {
		logs.Error("UpdateJijin", num, err)
		return false
	} else {
		return true
	}
}

func (tbl *TblJijin) GetGids() []string{
	// fmt.Println("go...")
	o := orm.NewOrm()
	qs := o.QueryTable(tbl)
	qs = qs.Distinct()
	var maps []orm.ParamsList
	num, err := qs.ValuesList(&maps, "jid")
	if err == nil {
		logs.Info("Jid List Result Nums: %d", num)
		data := make([]string, num)
		for index, row := range maps{
			if row[0].(string) != "" {
				// fmt.Println(row[0], index)
				//data = append(data, row[0].(string))
				data[index] = row[0].(string)
				//fmt.Println(num, len(data), cap(data))
			}
		}
		return data
	}
	return nil
}

func (tbl *TblJijin) GetRangeData(gid string, weekbefore int) (data, value []string,
	mon, sun string) {
	o := orm.NewOrm()
	qs := o.QueryTable(tbl)
	monday, sunday := myfunc.GetMonSunday(weekbefore)
	// fmt.Println(monday, sunday)
	qs = qs.Filter("jdate__gte", monday).Filter("jdate__lte", sunday).Filter("jid", gid)
	// qs.OrderBy("jdate")
	//qs = qs.Filter("id__gte", 1).Filter("id__lte", 20).Filter("jid", gid)
	cnt, err := qs.Count()
	logs.Info("weeekbefore:", weekbefore, "sq ,count:", cnt, err)
	qs = qs.OrderBy("jdate")
	var maps []orm.ParamsList
	num, err := qs.ValuesList(&maps, "jdate", "jvalue")
	if err == nil {
		data := make([]string, num)
		value := make([]string, num)
		logs.Info("Jijin List Result Nums: %d", num)
		for index, row := range maps{
			// fmt.Println(index, row[0], row[1])
			//if row[0].(string) == "" || row[1].(string) == "" {
			//	continue
			//}
			data[index] = row[0].(string)
			value[index] = row[1].(string)
			//data.Jvalue = append(data.Jdate, row[index].(string))
		}
		//fmt.Println(data)
		//fmt.Println(value)
		return data, value, monday, sunday
	}
	return nil, nil, monday, sunday
}

func (tbl *TblJijin) GetAllData(gid string, limit int) (data, value []string) {
	o := orm.NewOrm()
	qs := o.QueryTable(tbl)
	qs = qs.Filter("jid", gid).Limit(limit)
	qs = qs.OrderBy("-jdate")
	//qs = qs.Filter("id__gte", 1).Filter("id__lte", 20).Filter("jid", gid)
	// qs = qs.OrderBy("-jdate")
	
	cnt, err := qs.Count()
	logs.Info("Tbljijin ,count:", cnt, err)

	var maps []orm.ParamsList
	num, err := qs.ValuesList(&maps, "jdate", "jvalue")
	if err == nil {
		data := make([]string, num)
		value := make([]string, num)
		logs.Info("Jijin List Result Nums: %d", num)
		for index, row := range maps{
			// fmt.Println(index, row[0], row[1])
			//if row[0].(string) == "" || row[1].(string) == "" {
			//	continue
			//}
			data[index] = row[0].(string)
			value[index] = row[1].(string)
			//data.Jvalue = append(data.Jdate, row[index].(string))
		}
		//fmt.Println(data)
		//fmt.Println(value)
		return data, value
	}
	return nil, nil
}
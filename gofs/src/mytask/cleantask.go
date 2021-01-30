package mytask

import (
	"github.com/astaxie/beego/logs"
	"github.com/astaxie/beego/orm"
	"github.com/astaxie/beego/toolbox"
	"fmt"
	"mydb"
	"myfunc"
)

func cleanhistory() error{
	logs.Info("timed task clean history start.")
	tblhistory := mydb.TblBrowsingHistory{}
	o := orm.NewOrm()
	_, err := o.QueryTable(tblhistory).Filter("Browsing_date__lt", myfunc.GetDaysAgo(3)).Delete()
	if err != nil {
		logs.Error(nil)
	}
	return err
}

func init(){
	tk := toolbox.NewTask("cleanhistory", "0 0 */1 * * *", cleanhistory)
	err := tk.Run()
	if err != nil {
		fmt.Println(err)
	}
	toolbox.AddTask("cleanhistory", tk)
	toolbox.StartTask()
}
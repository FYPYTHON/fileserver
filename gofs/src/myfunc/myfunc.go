package myfunc

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"strconv"
	"time"
)
const (
	Godate string = "2006-01-02"
	Godate2 string = "20060102"
	Gotime string = "15:04:05"
	Gotime2 string = "150405"
	Godatetime string = "2006-01-02 15:04:05"
	Godatetime2 string = "2006/01/02 15:04:05"
	MY_SECRET string = "PyTHoN3)JavaWMakY6C#Hn/VB9oXwQt8C++&Mysql/xJ89E="
)

func MD5(data string) string{
	secret_byte := []byte(MY_SECRET)
	mymd5 := md5.New()
	mymd5.Write(secret_byte)
	data_byte := []byte(data)
	mymd5.Write(data_byte)
	sec_data := hex.EncodeToString(mymd5.Sum(nil))
	// fmt.Println(sec_data)
	return sec_data
}

func Test(){
	fmt.Println("myfunc ... ")
}
func ChanTest(){
	c := make(chan int , 10)
	go fibonacci(cap(c), c)
	for i:= range c {
		fmt.Println(i)
	}
}
func fibonacci(n int, c chan int) {
	x, y := 1, 1
	for i:=0; i < n; i++ {
		c <- x
		x, y = y, x + y
	}
	close(c)
}
func GetData(){
	t:= time.Now()
	fmt.Println(time.Now().UTC())
	fmt.Println(time.Now().Local())
	fmt.Println(time.Now())
	fmt.Println(t.String())
	fmt.Println(t.Unix())
	fmt.Println(t.UnixNano())
	fmt.Println(t.Format(Godate))
	fmt.Println(t.Format(Gotime))
	fmt.Println(t.Format(Godatetime))
	fmt.Println(t.Format(Godatetime2))
	st := strconv.FormatInt(time.Now().UnixNano(),10)
	fmt.Println(st)
}

func InterfaceFloat64ToInt64(e interface{}) int64 {
	var f64 = e.(float64)
	var i64 = int64(f64)
	return i64
}
func GetMapValueByKey(dict map[string] interface{}, key string) interface{}{
	for k := range dict{
		if k == key{
			// fmt.Println(k, dict[k])
			return dict[key]
		}
	}
	return nil
}

func GetMonSunday(weekbefore int) (string, string) {
	now := time.Now()
	offset := int(time.Monday - now.Weekday())
	if offset > 0 {
		offset = -6
	}
	offset = offset + (-7) * weekbefore
	weekStart := time.Date(now.Year(), now.Month(), now.Day(),
		0, 0, 0, 0, time.Local).AddDate(0, 0, offset)
	weekEnd := time.Date(now.Year(), now.Month(), now.Day(),
		0, 0, 0, 0, time.Local).AddDate(0, 0, offset+6)
	monday := weekStart.Format(Godate)
	sunday := weekEnd.Format(Godate)
	//fmt.Println(weekStart, weekEnd, offset)
	return monday, sunday
}

func GetLocalTime() time.Time{
	return time.Now().Add(+time.Hour * 8)
}

func GetMintuesAgo(mins time.Duration) string {
	now := time.Now().Add(-time.Minute * mins)
	return now.Format(Godatetime)
	//return now.UTC().String()
}

func GetDaysAgo(days int) string {
	now := time.Now().AddDate(0, 0, -days)
	return now.Format(Godate2)
}
func GetMillionSecond(t2 time.Time) int64{
	return t2.UnixNano() / int64(time.Millisecond) / 1e3
}

func GetImageBaseResize(size int) int {
	return size * 4/3 + size *4 % 3

}
func CheckStringInter(str string) bool {
	if _, err :=strconv.ParseFloat(str, 64); err == nil {
		return true
	} else {
		return false
	}
}

func CheckDate(strdate string) bool {
	_, err := time.Parse(Godate, strdate)
	if err == nil {
		return true
	} else {
		return false
	}
}
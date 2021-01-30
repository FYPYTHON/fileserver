package myfunc

import (
	"fmt"
)

type Person interface {
	Say() string
	work()
}
func Work(per Person){
	per.work()
}

//
type Teacher struct {

}

type Student struct {

}

type Worker struct {

}

// teacher
func (t Teacher) Say() string{
	return "teacher"
}
func (t Teacher) work(){
	fmt.Println("teacher teach")
}

// student
func (s Student) Say() string{
	return "student"
}

func (s Student) work(){
	fmt.Println("student study")
}
// worker
func (w Worker) Say() string {
	return "worker"
}

func (w Worker) work() {
	fmt.Println("worker work")
}

func WeSay(){
	persons := []Person{Student{}, Teacher{}, Worker{}}
	for _, per := range persons{
		fmt.Println(per.Say())
		Work(per)

	}
	a := []int{4,5,6}   // slice
	b := [...]string{"app", "web", "ios"}  // array
	a = append(a, 1)
	a = append(a, 2)
	fmt.Println(a)
	fmt.Println(b)
}




//  check list
//function getCheckedlist(){
//	var fchecks = []
//	var fsul = document.getElementById("fsul");
//	var flist = fsul.getElementsByTagName('input');
//	for(var i = 0; i < flist.length; i++) {
//		// console.log(i);
//	 //    console.log(flist[i].checked);
//	    if (flist[i].checked == true){
//	    	fchecks.push("{{curpath}}"+ "/" + flist[i].value);
//	    }
//
//	}
//	return fchecks;
//}
//var fchecks = getCheckedlist();

// api delete fs file
function fsdelete(curpath){
    var flist = getCheckedlist();
//    var curpath = $("#curpath").val();
//	console.log(flist);
//	var formData = new FormData();
//	formData.append("curpath", curpath);
//	formData.append("filelist", flist);
	if (flist.length <= 0){
		alert("请选择文件");
		return 0;
	}
	else{
		$.ajax({
	        type: "DELETE",
	        url: "/delete",
	        dataType : "json",
	        async: true,
	        data: {"filelist": flist, "curpath":curpath},
//            data: formData,
	        success: function (data){
	        	// console.log(data.msg);
	       		if (data.code == 1){
	       			alert(data.msg);
	       		}else{
	       		    alert(data.msg);
	       			window.location.href = "/fsmain?curpath=" + curpath;
	       		}
	        }
	    })
	}
}
// <li class="active"><a href="{{ home }}">Home</a></li>
// <li><a href="{{ about }}">About</a></li>
"use strict";
// 解决兼容问题 
// Block-scoped declarations (let, const, function, class) not yet supported outside strict mode
// 文件列表
let region = ['AiData', 'meetingData', 'mtLog', 'platformData', 'platformLog']
let store = {
    conenteId:'search',
    filelist: {
        data: [],
        type: 0,
    },
    actions: {
        checkpath:function(path){
            if(path == "" || path == null)
            {
                return false;
            }else{
                return true;
            }

        },
        getFileList: function(path, ftype){
            $.ajax({
                url: '/api/',
                async : false,
                type: 'GET',
                headers:{
                    type: atype,
                    home: hometype
                },
                data: {
                    path: path,
                    type: ftype
                },
                dataType: 'json',
                success: function (data) {

                    var all_file_directory = data.filelist.directory.concat(data.filelist.file)
                    store.filelist.data = all_file_directory
                }
            })
        },
        getFileListSync: function(path, ftype, atype, hometype){
            $.getJSON({
                url: '/api/',
                type: 'GET',
                headers:{
                    type: atype,
                    home: hometype,
                    'filesize':520,
                },
                data: {
                    path: path,
                    type: ftype
                },
                dataType: 'json',
                success: function (data) {
                    console.log("search ok...");
                    $("#searchResultSync li").html("");
                    var result = parseInt(data.repmsg.success);
                    if(result == 0){
                        alert("errorcode:"+ data.repmsg.errorcode + "\nderccription:" + data.repmsg.description);
                    }
                    else{
                        var all_file_directory = data.filelist.directory.concat(data.filelist.file);
                        store.filelist.data = all_file_directory;
                        console.log(all_file_directory);
                        $("#searchResultSync").html("");
                        for (var i = 0; i < all_file_directory.length; i++) {
                            var item = '<li>' + all_file_directory[i] + '</li>';
                            $("#searchResultSync").append(item);  
                        }
                    }
                }
            })
        },
        deleteSync:function(path, ftype, atype, hometype){
            $.ajax({
                url:'/api/',
                type:'delete',
                headers:{
                    type: atype,
                    home: hometype
                },
                data: {
                    path: path,
                    type: ftype
                },
                dataType: 'json',
                success: function (data) {
                    var result = parseInt(data.repmsg.success);
                    if(result == 0){
                        alert("errorcode:"+ data.repmsg.errorcode + "\nderccription:" + data.repmsg.description);
                    }
                    else{
                        alert("删除成功！");
                    }

                }

            })
        },
        newSync:function(path, ftype, atype, hometype){
            $.ajax({
                url:'/api/',
                type:'put',
                headers:{
                    type: atype,
                    home: hometype
                },
                data: {
                    path: path,
                    type: ftype
                },
                dataType: 'json',
                success: function (data) {
                    var result = parseInt(data.repmsg.success);
                    if(result == 0){
                        alert("errorcode:"+ data.repmsg.errorcode + "\nderccription:" + data.repmsg.description);
                    }
                    else{
                        alert("新建成功！");
                    }

                }

            })
        },
        uploadFile:function(formdata, filesize, atype, hometype){
            $.ajax({
                url:'/api/',
                type:'put',
                headers:{
                    type: atype,
                    home: hometype,
                    'file-size':filesize,  // 参数中横线（-）的处理，后端获取为： HTTP_FILE_SIZE  
                },
                data: formdata,
                dataType: 'json',
                contentType:false,
                processData: false, // tell jquery not to process the data
                success: function (data) {
                    var result = parseInt(data.repmsg.success);
                    if(result == 0){
                        alert("errorcode:"+ data.repmsg.errorcode + "\nderccription:" + data.repmsg.description);
                    }
                    else{
                        alert(data.repmsg.description);
                    }

                }

            })
        },
        // 测试下载
        test:function(file, hometype){
            $.getJSON({
                url:'/download/',
                type:'GET',
                headers:{
                    path: file,
                    home: hometype,
                },
                dataType: 'json',
                success: function (data) {
                    console.log("file:" + " " + file);
                    $("#mydownload").href = data.furl;


                }

            })
        },
        // GET 不能使用表单提交
        downloadFile:function(file, atype, hometype){
            $.getJSON({
                url:'/api/',
                type:'GET',
                headers:{
                    type: atype,
                    home: hometype,
                },
                data: {
                    path:file,
                },
                dataType: 'json',
                success: function (data) {
                    console.log("file:" + " " + file);
                    
                    var result = parseInt(data.repmsg.success);
                    if(result == 0){
                        alert("errorcode:"+ data.repmsg.errorcode + "\nderccription:" + data.repmsg.description);
                    }
                    else{
                        let alink = document.createElement('a');
                        alink.href = "data:text/json;charset=utf-8,"+ data.body;
                        alink.download = file;
                        alink.click();
                        console.log("clicked ...", data.repmsg.description);
                        alert(data.repmsg.description);
                    }

                }

            })
        },
        copyFile:function(formdata,  atype, hometype){
            console.log("copy file ajax...");
            $.ajax({
                url:'/api/',
                type:'put',
                headers:{
                    type: atype,
                    home: hometype,
                },
                data: formdata,  // formdata使用讲processData设为false，不处理data数据
                dataType: 'json',
                contentType:false,
                processData: false, // tell jquery not to process the data
                success: function (data) {
                    var result = parseInt(data.repmsg.success);
                    if(result == 0){
                        alert("errorcode:"+ data.repmsg.errorcode + "\nderccription:" + data.repmsg.description);
                    }
                    else{
                        alert(data.repmsg.description);
                    }

                }

            })
        },
        postList:function(path, ftype, alist){
            $.ajax({
                url:'/api/',
                type:'post',
                headers:{
                    type: 'posttest',
                },
                data: {
                    path: path,
                    type: ftype,
                    ids:['1',2],
                    als: alist,
                },
                dataType: 'json',
//                contentType:false,
//                processData: true, // tell jquery not to process the data
//                traditional:true,   // get list data
                success: function (data) {
                    var result = parseInt(data.repmsg.success);
                    if(result == 0){
                        alert("errorcode:"+ data.repmsg.errorcode + "\nderccription:" + data.repmsg.description);
                    }
                    else{
                        alert("新建成功！");
                    }

                }

            })
        },

    }
}
let navBar = {
    template:`
    <nav class="navbar navbar-default">
        <div class="container-fluid">
              <ul class="nav navbar-nav">
                <li class="active">{{home}}</li>
                <li>{{about}}</li>               
              </ul>
        </div>
    </nav>
    `,
    data:function(){
        return {
            home:'Home',
            about:'About'
        }
    }
}

let mainContent = {
    template:`
    <h1 class="fs-title testonly">{{ content }}</h1>
    `,
    data:function(){
        return {
            content:'文件服务器demo'
        }
    }
}
// let leftMenu = {
//     template:`
//     <div class="col-sm-4 mymenu myborder">
//         <div class="mytempdiv testonly" style="background:#33CCFF">操作</div>
//         <ul class="list-unstyled">
//             <li><button class="btn btn-info mybtn" id="search_con" @click="showsearch">查询</button></li>
//             <li><button class="btn btn-info mybtn" id="new_con">新建</button></li>
//             <li><button class="btn btn-info mybtn" id="modify_con">修改</button></li>
//             <li><button class="btn btn-info mybtn" id="copy_con">复制</button></li>
//             <li><button class="btn btn-info mybtn" id="delete_con" @click="showdelete">删除</button></li>
//             <li><button class="btn btn-info mybtn" id="delete_con">上传 </button></li>
//             <li><button class="btn btn-info mybtn" id="delete_con">下载</button></li>
//         </ul>
//     </div>
//     `,
//     methods:{
//         showsearch(){
//             $("#search_con").click().addClass("active");
//             alert("search path click");
//             store.conenteId = 'searchContent';
//             rightContent.data.which_to_show = 'searchContent';
//             alert(rightContent.data.which_to_show);
//         },
//         showdelete(){
//             $("delete_con").click().addClass("active");
//             alert("delete item click");
//             store.conenteId = 'deleteContent';
//             rightContent.data.which_to_show = 'deleteContent';
//             alert(rightContent.data.which_to_show);
//         }
//     }
// }
let searchContent = {
    template:`
    <div class="form form-group" id="searchContent">
        <div class="col-sm-4 testonly">
            <label style="float:left;">请选择目录：</label>
        </div>
        <div class="col-sm-8">
            <select class="selectpicker myselect" id="hometype" name="hometype">
                <option value="0">AiData</option>
                <option value="1">MeetingData</option>
                <option value="2">MtLog</option>
                <option value="3">PlatformData</option>
                <option value="4">PlatformLog</option>
            </select>
        </div>
        <div class="col-sm-12 myseperator"></div>
        <div class="col-sm-4 testonly">
            <label style="float:left;">请输入路径：</label>
        </div>
        <div class="col-sm-8 testonly">
            <input type="text" class="form-control" v-model="inputpath" ref="refpath" 
             placeholder="请输入绝对路径" value="/">
        </div>
        <div class="col-sm-12 mytempdiv">  </div>
        <div class="col-sm-3">
            <button class="btn btn-primary mybtn" @click="search_path(type)">查询</button>
        </div>
        <div class="col-sm-12 mytempdiv">  </div>
        <div class="col-sm-12" >
            <ul class="list-unstyled" v-for="item in filelist">
                <li>{{item}}</li>
            </ul>
        </div>
        <div class="col-sm-12" >
            <ul class="list-unstyled" id="searchResultSync">
            </ul>
        </div>
    </div>
    `,
    data() {
        return {
            type : 1,
            inputpath:null,
            filelist:store.filelist.data
        }
    },
    methods:{
        search_path(type){
            // input取值 使用ref 或 v-model
            // alert($("#ipath").val());
            var pathtype = $("#pathtype").val();
            pathtype = 1
            var hometype = $("#hometype").val();
            var operation = 'show';
            // var path = this.$refs.refpath.value
            var path = this.inputpath
            if(pathtype==0)
            { 
                // store.actions.getFileList(path, pathtype); //同步
                // this.filelist = store.filelist.data;   // 同步
                store.actions.getFileListSync(path, pathtype, operation, hometype); // 异步
                
            }
            else
                store.actions.getFileListSync(path, pathtype, operation, hometype); // 异步
        }
    }
}
let newContent = {
    template:`
    <div class="form form-group" id="deleteContent">
        <div class="col-sm-4 testonly">
            <label style="float:left;">请选择目录：</label>
        </div>
        <div class="col-sm-8">
            <select class="selectpicker myselect" id="hometype" name="hometype">
                <option value="0">AiData</option>
                <option value="1">MeetingData</option>
                <option value="2">MtLog</option>
                <option value="3">PlatformData</option>
                <option value="4">PlatformLog</option>
            </select>
        </div>
        <div class="col-sm-12 myseperator"></div>
        <div class="col-sm-4 testonly">
            <label style="float:left;">请输入新建目录：</label>
        </div>
        <div class="col-sm-8 testonly">
            <input type="text" class="form-control" v-model="inputpath" ref="refpath" 
             placeholder="请输入绝对路径">
        </div>
        <div class="col-sm-12 mytempdiv">  </div>
        <div class="col-sm-3">
            <button class="btn btn-primary mybtn" @click="new_path">新建</button>
        </div>
    </div>
    `,
    data(){
        return {
            inputpath:null,
        }
    },
    methods:{
        new_path(){
            // var pathtype = $("#pathtype").val();
            var pathtype = 1
            var hometype = $("#hometype").val();
            var operation = 'create_directory';
            // var path = this.$refs.refpath.value
            var path = this.inputpath
            store.actions.newSync(path, pathtype, operation, hometype); // 异步 
        }
    }

}
let deleteContent = {
    template:`
    <div class="form form-group" id="deleteContent">
        <div class="col-sm-4 testonly">
            <label style="float:left;">请选择目录：</label>
        </div>
        <div class="col-sm-8">
            <select class="selectpicker myselect" id="hometype" name="hometype">
                <option value="0">AiData</option>
                <option value="1">MeetingData</option>
                <option value="2">MtLog</option>
                <option value="3">PlatformData</option>
                <option value="4">PlatformLog</option>
            </select>
        </div>
        <div class="col-sm-12 myseperator"></div>
        <div class="col-sm-4 testonly">
            <label style="float:left;">请选择类型：</label>
        </div>
        <div class="col-sm-8">
            <select class="selectpicker myselect" id="pathtype" name="pathtype">
                <option value="0">文件</option>
                <option value="1">目录</option>
            </select>
        </div>
        <div class="col-sm-12 myseperator"></div>
        <div class="col-sm-4 testonly">
            <label style="float:left;">请输入路径：</label>
        </div>
        <div class="col-sm-8 testonly">
            <input type="text" class="form-control" v-model="inputpath" ref="refpath" 
             placeholder="请输入绝对路径">
        </div>
        <div class="col-sm-12 mytempdiv">  </div>
        <div class="col-sm-3">
            <button class="btn btn-primary mybtn" @click="delete_path(type)">删除</button>
        </div>
    </div>
    `,
    data() {
        return {
            type : 1,
            inputpath:null,
        }
    },
    methods:{
        delete_path(type){
            alert("delete ???");
            var pathtype = $("#pathtype").val();
            var hometype = $("#hometype").val();
            var operation = 'directory';
            var path = this.inputpath
            store.actions.deleteSync(path, pathtype, operation, hometype); // 异步     
        }
    }
}
let uploadContent = {
    template:`
    <div class="form form-group" id="uploadContent">
        <div class="col-sm-4 testonly">
            <label style="float:left;">请选择目录：</label>
        </div>
        <div class="col-sm-8">
            <select class="selectpicker myselect" id="hometype" name="hometype">
                <option value="0">AiData</option>
                <option value="1">MeetingData</option>
                <option value="2">MtLog</option>
                <option value="3">PlatformData</option>
                <option value="4">PlatformLog</option>
            </select>
        </div>
        <div class="col-sm-12 myseperator"></div>
        <div class="col-sm-4 testonly">
            <label style="float:left;">请输入上传目录：</label>
        </div>
        <div class="col-sm-8 testonly">
            <input type="text" class="form-control" v-model="inputpath" ref="refpath" 
             placeholder="请输入绝对路径">
        </div>
        <div class="col-sm-12 myseperator"></div>
        <div class="col-sm-4 testonly">
            <label style="float:left;">请选择文件：</label>
        </div>
        <div class="col-sm-8">
            <input type="file" name="uploadfile" id="uploadfile" />
        </div>
        <div class="col-sm-12 mytempdiv">  </div>
        <div class="col-sm-3">
            <button class="btn btn-primary mybtn" @click="upload_file">上传</button>
        </div>
    </div>
    `,
    data(){
        return {
            inputpath:null,
        }
    },
    methods:{
        upload_file(){
            alert("upload file ???");
            var path = this.inputpath
            var hometype = $("#hometype").val();
            var file = $('#uploadfile')[0].files[0];
            var operation = 'upload';
            var formData=new FormData();
            formData.append("path", path);
            formData.append("data", file);
            if(!file){
                alert("上传文件为空，请选择！");
                return
            }
            if(store.actions.checkpath(path) == false)
            {
                alert("文件目录为空，请输入！");
                return
            }
            // console.log(file);
            // console.log(file.size);
            var filesize = file.size;
            store.actions.uploadFile(formData, filesize, operation, hometype); // 异步     
        }
    }
}
let downloadContent = {
    template:`
    <div class="form form-group" id="deleteContent">
        <div class="col-sm-5 testonly">
            <label style="float:left;">请选择目录：</label>
        </div>
        <div class="col-sm-7">
            <select class="selectpicker myselect" id="hometype" name="hometype">
                <option value="0">AiData</option>
                <option value="1">MeetingData</option>
                <option value="2">MtLog</option>
                <option value="3">PlatformData</option>
                <option value="4">PlatformLog</option>
            </select>
        </div>
        <div class="col-sm-12 myseperator"></div>
        <div class="col-sm-5 testonly">
            <label style="float:left;">请输入需要下载的文件：</label>
        </div>
        <div class="col-sm-7 testonly">
            <input type="text" class="form-control" v-model="inputfile" ref="refpath" 
             placeholder="请输入绝对路径">
        </div>
        <div class="col-sm-12 myseperator"></div>
        <div class="col-sm-12 mytempdiv">  </div>
        <div class="col-sm-3">
            <button class="btn btn-primary mybtn" @click="download_file">下载</button>
        </div>
    </div>
    `,
    data(){
        return {
            inputfile:null,
        }
    },
    methods:{
        download_file(){
            var path = this.inputfile;
            var hometype = $("#hometype").val();
            var operation = 'download';
            if (store.actions.checkpath(path) == false){
                alert("下载的文件不能为空，请输入！");
            }else{
                store.actions.downloadFile(path, operation, hometype);
            }

        }
    }

}
let testContent = {
    template:`
    <div class="form form-group" id="deleteContent">
        <div class="col-sm-5 testonly">
            <label style="float:left;">请选择目录：</label>
        </div>
        <div class="col-sm-7">
            <select class="selectpicker myselect" id="hometype" name="hometype">
                <option value="0">AiData</option>
                <option value="1">MeetingData</option>
                <option value="2">MtLog</option>
                <option value="3">PlatformData</option>
                <option value="4">PlatformLog</option>
            </select>
        </div>
        <div class="col-sm-12 myseperator"></div>
        <div class="col-sm-5 testonly">
            <label style="float:left;">请输入需要下载的文件：</label>
        </div>
        <div class="col-sm-7 testonly">
            <input type="text" class="form-control" v-model="inputfile" ref="refpath"
             placeholder="请输入绝对路径">
        </div>
        <div class="col-sm-12 myseperator"></div>
        <div class="col-sm-12 mytempdiv">  </div>
        <div class="col-sm-3">
            <a id="mydownload" href="" download="" @click="test_file">下载</a>
        </div>
    </div>
    `,
    data(){
        return {
            inputfile:null,
        }
    },
    methods:{
        test_file(){
            var path = this.inputfile;
            var hometype = $("#hometype").val();
            var operation = 'download';
            if (store.actions.checkpath(path) == false){
                alert("下载的文件不能为空，请输入！");
            }else{
                store.actions.test(path, hometype);
            }

        }
    }

}
let copyContent = {
    template:`
    <div class="form form-group" id="deleteContent">
        <div class="col-sm-5 testonly">
            <label style="float:left;">请选择目录：</label>
        </div>
        <div class="col-sm-7">
            <select class="selectpicker myselect" id="hometype" name="hometype">
                <option value="0">AiData</option>
                <option value="1">MeetingData</option>
                <option value="2">MtLog</option>
                <option value="3">PlatformData</option>
                <option value="4">PlatformLog</option>
            </select>
        </div>
        <div class="col-sm-12 myseperator"></div>
        <div class="col-sm-5 testonly">
            <label style="float:left;">请选择类型：</label>
        </div>
        <div class="col-sm-7">
            <select class="selectpicker myselect" id="pathtype" name="pathtype">
                <option value="0">文件</option>
                <option value="1">目录</option>
            </select>
        </div>
        <div class="col-sm-12 myseperator"></div>
        <div class="col-sm-5 testonly">
            <label style="float:left;">请输入需要复制的文件：</label>
        </div>
        <div class="col-sm-7 testonly">
            <input type="text" class="form-control" v-model="inputfilesrc" ref="refpathsrc" 
             placeholder="请输入绝对路径">
        </div>
        <div class="col-sm-12 myseperator"></div>
        <div class="col-sm-5 testonly">
            <label style="float:left;">请输入目标路径：</label>
        </div>
        <div class="col-sm-7 testonly">
            <input type="text" class="form-control" v-model="inputfiledst" ref="refpathdst" 
             placeholder="请输入绝对路径">
        </div>
        <div class="col-sm-12 myseperator"></div>
        <div class="col-sm-12 mytempdiv">  </div>
        <div class="col-sm-3">
            <button class="btn btn-primary mybtn" @click="copy_file">复制</button>
        </div>
    </div>
    `,
    data(){
        return {
            inputfilesrc:null,
            inputfiledst:null,
        }
    },
    methods:{
        copy_file(){
            var path = this.inputfilesrc;
            var dstpath = this.inputfiledst;
            if (store.actions.checkpath(path) == false){
                alert("复制文件(夹)不能为空，请输入！");
            }
            else if (store.actions.checkpath(dstpath) == false) {
                alert("目标路径不能为空，请输入！");
            }
            else{
                var hometype = $("#hometype").val();
                var pathtype = $("#pathtype").val();
                var operation = 'copy';
                var formData=new FormData();
                formData.append("path", path);
                formData.append("dstpath", dstpath);
                formData.append("type", pathtype);
                alert("copy file");
                console.log(path,dstpath,hometype,pathtype,operation);
                store.actions.copyFile(formData, operation, hometype);
            }

        }
    }

}
let renameContent = {
    template:`
    <div class="form form-group" id="deleteContent">
        <div class="col-sm-5 testonly">
            <label style="float:left;">请选择目录：</label>
        </div>
        <div class="col-sm-7">
            <select class="selectpicker myselect" id="hometype" name="hometype">
                <option value="0">AiData</option>
                <option value="1">MeetingData</option>
                <option value="2">MtLog</option>
                <option value="3">PlatformData</option>
                <option value="4">PlatformLog</option>
            </select>
        </div>
        <div class="col-sm-12 myseperator"></div>
        <div class="col-sm-5 testonly">
            <label style="float:left;">请输入需要重命名的文件(夹)：</label>
        </div>
        <div class="col-sm-7 testonly">
            <input type="text" class="form-control" v-model="inputfilesrc" ref="refpathsrc"
             placeholder="请输入绝对路径">
        </div>
        <div class="col-sm-12 myseperator"></div>
        <div class="col-sm-5 testonly">
            <label style="float:left;">请输入新名字：</label>
        </div>
        <div class="col-sm-7 testonly">
            <input type="text" class="form-control" v-model="inputfiledst" ref="refpathdst"
             placeholder="请输入绝对路径">
        </div>
        <div class="col-sm-12 myseperator"></div>
        <div class="col-sm-12 mytempdiv">  </div>
        <div class="col-sm-3">
            <button class="btn btn-primary mybtn" @click="rename_file">重命名</button>
        </div>
    </div>
    `,
    data(){
        return {
            inputfilesrc:null,
            inputfiledst:null,
        }
    },
    methods:{
        rename_file(){
            var path = this.inputfilesrc;
            var dstpath = this.inputfiledst;
            if (store.actions.checkpath(path) == false){
                alert("文件（夹）不能为空，请输入！");
            }
            else if (store.actions.checkpath(dstpath) == false) {
                alert("新名字不能为空，请输入！");
            }
            else{
                var hometype = $("#hometype").val();
                var pathtype = 1;
                var operation = 'rename';
                var formData=new FormData();
                formData.append("path", path);
                formData.append("dstpath", dstpath);
                formData.append("type", pathtype);
                console.log(path,dstpath,hometype,pathtype,operation);
                store.actions.copyFile(formData, operation, hometype);
            }

        }
    }
}
//<a id="mydownload" href="" download="" @click="test_file">下载</a>
let postContent = {
    template:`
    <div class="form form-group" id="deleteContent">
        <div class="col-sm-5 testonly">
            <label style="float:left;">请选择目录：</label>
        </div>
        <div class="col-sm-7">
            <select class="selectpicker myselect" id="hometype" name="hometype">
                <option value="0">AiData</option>
                <option value="1">MeetingData</option>
                <option value="2">MtLog</option>
                <option value="3">PlatformData</option>
                <option value="4">PlatformLog</option>
            </select>
        </div>
        <div class="col-sm-12 myseperator"></div>
        <div class="col-sm-5 testonly">
            <label style="float:left;">请输入需要下载的文件：</label>
        </div>
        <div class="col-sm-7 testonly">
            <input type="text" class="form-control" v-model="inputfile" ref="refpath"
             placeholder="请输入绝对路径">
        </div>
        <div class="col-sm-12 myseperator"></div>
        <div class="col-sm-12 mytempdiv">  </div>
        <div class="col-sm-3">

            <button class="btn btn-primary mybtn" @click="test_file">下载</button>
        </div>
    </div>
    `,
    data(){
        return {
            inputfile:null,
        }
    },
    methods:{
        test_file(){
            var path = this.inputfile;
            var hometype = $("#hometype").val();
            var operation = 'download';
            var alist = Array(3);
            alist[0] = 1
            alist[2] = 2
            alist[3] = 3
            if (store.actions.checkpath(path) == false){
                alert("下载的文件不能为空，请输入！");
            }else{
                store.actions.postList(path, hometype, alist);
            }

        }
    }

}
let bodyContent = {
    template:`
    <div class="col-sm-12">
        <div class="col-sm-4 mymenu myborder">
            <div class="mytempdiv testonly" style="background:#33CCFF">操作</div>
            <ul class="list-unstyled">
                <li><button class="btn btn-info mybtn" id="search_con" @click="showsearch">查询</button></li>
                <li><button class="btn btn-info mybtn" id="new_con" @click="shownew">新建</button></li>
                <li><button class="btn btn-info mybtn" id="rename_con" @click="showrename">重命名</button></li>
                <li><button class="btn btn-info mybtn" id="copy_con" @click="showcopy">复制</button></li>
                <li><button class="btn btn-info mybtn" id="upload_con" @click="showupload">上传 </button></li>
                <li><button class="btn btn-info mybtn" id="delete_con" @click="showdownload">下载</button></li>
                <li><button class="btn btn-info mybtn" id="delete_con" @click="showdelete">删除</button></li>
                <li><button class="btn btn-info mybtn" id="down_con" @click="showtest">下载测试</button></li>
                <li><button class="btn btn-info mybtn" id="post_con" @click="showpost">Post测试</button></li>
            </ul>
        </div>
        <div class="col-sm-8 mycontent testonly" id="compID">
            <div class="mytempdiv testonly" style="background:#33CCFF">内容</div>
            <componentb v-bind:is="compID"></componentb>
        </div>
    </div>
    `,
    data(){
        return {
            compID: store.conenteId,
        }
    },
    components:{
        'search': searchContent,
        'delete': deleteContent,
        'new': newContent,
        'upload': uploadContent,
        'download': downloadContent,
        'copy': copyContent,
        'rename':renameContent,
        'test': testContent,
        'post': postContent,
    },
    methods:{
        showsearch(){
            this.compID = 'search';
            store.filelist.data = []
        },
        shownew(){
            this.compID = 'new';
        },
        showdelete(){
            this.compID = 'delete';
        },
        showupload(){
            this.compID = 'upload';
        },
        showdownload(){
            this.compID = 'download';
        },
        showcopy(){
            this.compID = 'copy';
        },
        showmodify(){
            this.compID = 'modify';
        },
        showrename(){
            this.compID = 'rename';
        },
        showtest(){
            this.compID = 'test';
        },
        showpost(){
            this.compID = 'post';
        },

    }
}
let app = {
    template:`
    <div class="container">
        <div class="row">
            <nav-bar></nav-bar>
        </div>
        <div class="row" style="background:#33FFCC;">
            <main-content></main-content>
        </div>
        <div class="container-fluid">`+
            // <leftMenu></leftMenu>
            // <rightContent></rightContent>
            `<bodyContent></bodyContent>
        </div>
    </div>
    `,
    components:{
        'nav-bar':navBar,
        'main-content':mainContent,
        // 'leftMenu':leftMenu,
        // 'rightContent':rightContent,
        'bodyContent':bodyContent,
    }
}

let root = new Vue({
    el:'#app',
    template:`<app></app>`,
    components:{
        'app':app
    },
})
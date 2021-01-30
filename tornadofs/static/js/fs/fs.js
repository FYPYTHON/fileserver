// get params from url
function getUrl(){
    var url = location.search;
    var theRequest = new Object();
    if (url.indexOf("?") != -1) {
        var str = url.substr(1);
        strs = str.split("&")
        for (var i = 0; i < strs.length; i++) {
            theRequest[strs[i].split("=")[0]] = decodeURI(strs[i].split("=")[1]);
        }
    }
    return theRequest;
};
function getCookie(name) {
    console.log(document.cookie);
    // var reg = "(^| )"+name+"=([^;]*)(;|$)";
    var r = document.cookie.match("\\b"+name+"=([^:; ]*)\\b");
    return r ? r[1] : "undefined";
};
$(document).ready(function () {
    var Request = new Object();
    Request = getUrl();
    var val= Request["msg"];
    $("#msgSignin").html(val).css("color","red");
});
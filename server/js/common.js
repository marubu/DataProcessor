
function notice_api_result(res, st){
    var $notice = $("header>span");
    var exit_code = res["exit_code"];
    if(exit_code != 0){
        $notice
            .text("API call fails: " + res["message"])
            .css("color", "red");
    }
}
var auth = false;
var uuid = "";
function init()
{
    console.log("Setting js loading.")
    websocket = new WebSocket("ws://127.0.0.1:10000/ws");
    connect_web();
    $("#login_submit").click(function(e) {
        login();
    });
}
function connect_web() 
{
    console.log("try to connect");
    mc("Connecting ...");
    websocket.onopen = function(evt) {onOpen(evt)};
    websocket.onerror = function(evt) {onError(evt)}
    websocket.onmessage = function(evt) {onMessage(evt)};
    websocket.onclose = function(evt) {onClose(evt)};
}
function onOpen(evt) 
{
    mc("Local server connected.");
}
function onError(evt) 
{ 
	mc("Can't connect, will try again in 10 seconds.");
    setTimeout(connect_web,10000);
}  
function mc(msg)
{
    $("#status").html(msg);
}
function onClose(evt)
{
    mc("Connect closed, will try again in 10 seconds.");
    setTimeout(connect_web,10000);
}
function onMessage(evt) 
{ 
    var s = JSON.parse(evt.data);
    console.log(s);
    if(uuid == "")
    {
        uuid = s.uuid;
    }
    else if(!auth)
    {
        if(s.code == 200)
        {
            auth = true;
            mc('login successful');
            var data = {
                type: "get_setting_data"
            };
            websocket.send(JSON.stringify(data));
        }
        else
        {
            mc('Login fail, password or username error.');
        }
    }
}
function login()
{
    if(auth)
        return;
    if(uuid == "")
    {
        mc("Server not connected.");
        return;
    }
    mc("Sending data");
    var password = $.md5($("#user_pass").val()) + uuid;
    password = $.md5(password);
    
    var data = {
        type: "login",
        content:{
            user: $("#user_name").val(),
            pass: password
        }
    };
    websocket.send(JSON.stringify(data));
   // console.log(data);
}
var wsUri = "ws://goofydog.me:10000/ws";
var output;
function init()
{
    alert_msg("正在載入...",0);
    output = document.getElementById("output");
    alert_msg("正在連接伺服器",0);
    connect_web();

}
            
function connect_web() 
{
    console.log("try to connect");
    websocket = new WebSocket(wsUri);
    websocket.onopen = function(evt) {onOpen(evt)};
    websocket.onclose = function(evt) {onClose(evt)};
    websocket.onmessage = function(evt) {onMessage(evt)};
    websocket.onerror = function(evt) {onError(evt)};
}
function onOpen(evt) 
{
    alert_msg("與本機連線成功",1);
    login();
}  
function onClose(evt) 
{ 
    
}  
function onMessage(evt) 
{ 
    var s = JSON.parse(evt.data);
    console.log(s);
    if(s.type == 'login')
    {
        if(s.code == 200)
            alert_msg('驗證成功','1');
        else
            alert_msg('連結無效，請重新索取','0');
    }
    else if(s.type == 'msg')
    {
         alert_msg(s.nick + ": " + s.msg,'2');
    }
   // alert_msg(s,'1');
}  
function onError(evt) 
{ 
    connect_web_again();
}  
function doSend(message)
{ 
    //writeToScreen("SENT: " + message);
    websocket.send(message); 
}  
function writeToScreen(message) 
{ 
    var pre = document.createElement("p"); 
    pre.style.wordWrap = "break-word";
    pre.innerHTML = message; 
    output.appendChild(pre); 
}  
window.addEventListener("load", init, false);  
function login()
{
    var pass = location.search.replace('%20','');
    try
    {

        var user = pass.split('!')[0].replace('?','').replace('%20','')
        var token = pass.split('!')[1]
        var data = {
            user:user,
            token:token,
            type:'token_login'
        }
        console.log(data);
        doSend(JSON.stringify(data));
    }
    catch(e)
    {
        alert_msg('連結無效，請重新索取','0');
    }
    
}
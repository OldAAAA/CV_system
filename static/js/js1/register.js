
function check(){
  var x=document.getElementById("email");
  x.setCustomValidity("");
  if(x.checkValidity()==false){
    x.setCustomValidity("Your e-mail address is wrong!");
    return;
  }
  var vv=document.getElementById("password");
  vv.setCustomValidity("");
  if(vv.value.length<6)
  {
    vv.setCustomValidity('Your password must include at least six characters');
    return;
  }
  var cv=document.getElementById("confirm_password");
  cv.setCustomValidity("");
  if(cv.value!=vv.value)
  {
    cv.setCustomValidity('Passwords mismatch');
    return;
  }
  var email=$("email").val();
  var pass=$("userPsd").val();
  var user={mail:email,password:pass};
}
function check2(){
  var x=document.getElementById("email");
  var vv=document.getElementById("password");
  vv.setCustomValidity("");
  x.setCustomValidity("");
  if(x.value=='admin'&&vv.value=='')
  {
     window.location.href="administrator.html";
     return;
  }
  if(x.checkValidity()==false){
    x.setCustomValidity("Your e-mail address is wrong!");
    return;
  }
  if(vv.value.length<6)
  {
    vv.setCustomValidity('Your password must include at least six characters');
    return;
  }
  var email=$("#email").val();
  var pass=$("#password").val();

}
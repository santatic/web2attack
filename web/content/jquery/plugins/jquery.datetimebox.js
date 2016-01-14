/**
 * jQuery EasyUI 1.3.1
 * 
 * Licensed under the GPL terms
 * To use it on other terms please contact us
 *
 * Copyright(c) 2009-2012 stworthy [ stworthy@gmail.com ] 
 * 
 */
(function($){
function _1(_2){
var _3=$.data(_2,"datetimebox");
var _4=_3.options;
$(_2).datebox($.extend({},_4,{onShowPanel:function(){
var _5=$(_2).datetimebox("getValue");
_9(_2,_5,true);
_4.onShowPanel.call(_2);
},formatter:$.fn.datebox.defaults.formatter,parser:$.fn.datebox.defaults.parser}));
$(_2).removeClass("datebox-f").addClass("datetimebox-f");
$(_2).datebox("calendar").calendar({onSelect:function(_6){
_4.onSelect.call(_2,_6);
}});
var _7=$(_2).datebox("panel");
if(!_3.spinner){
var p=$("<div style=\"padding:2px\"><input style=\"width:80px\"></div>").insertAfter(_7.children("div.datebox-calendar-inner"));
_3.spinner=p.children("input");
var _8=_7.children("div.datebox-button");
var ok=$("<a href=\"javascript:void(0)\" class=\"datebox-ok\"></a>").html(_4.okText).appendTo(_8);
ok.hover(function(){
$(this).addClass("datebox-button-hover");
},function(){
$(this).removeClass("datebox-button-hover");
}).click(function(){
_f(_2);
});
}
_3.spinner.timespinner({showSeconds:_4.showSeconds,separator:_4.timeSeparator}).unbind(".datetimebox").bind("mousedown.datetimebox",function(e){
e.stopPropagation();
});
_9(_2,_4.value);
};
function _a(_b){
var c=$(_b).datetimebox("calendar");
var t=$(_b).datetimebox("spinner");
var _c=c.calendar("options").current;
return new Date(_c.getFullYear(),_c.getMonth(),_c.getDate(),t.timespinner("getHours"),t.timespinner("getMinutes"),t.timespinner("getSeconds"));
};
function _d(_e,q){
_9(_e,q,true);
};
function _f(_10){
var _11=$.data(_10,"datetimebox").options;
var _12=_a(_10);
_9(_10,_11.formatter.call(_10,_12));
$(_10).combo("hidePanel");
};
function _9(_13,_14,_15){
var _16=$.data(_13,"datetimebox").options;
$(_13).combo("setValue",_14);
if(!_15){
if(_14){
var _17=_16.parser.call(_13,_14);
$(_13).combo("setValue",_16.formatter.call(_13,_17));
$(_13).combo("setText",_16.formatter.call(_13,_17));
}else{
$(_13).combo("setText",_14);
}
}
var _17=_16.parser.call(_13,_14);
$(_13).datetimebox("calendar").calendar("moveTo",_17);
$(_13).datetimebox("spinner").timespinner("setValue",_18(_17));
function _18(_19){
function _1a(_1b){
return (_1b<10?"0":"")+_1b;
};
var tt=[_1a(_19.getHours()),_1a(_19.getMinutes())];
if(_16.showSeconds){
tt.push(_1a(_19.getSeconds()));
}
return tt.join($(_13).datetimebox("spinner").timespinner("options").separator);
};
};
$.fn.datetimebox=function(_1c,_1d){
if(typeof _1c=="string"){
var _1e=$.fn.datetimebox.methods[_1c];
if(_1e){
return _1e(this,_1d);
}else{
return this.datebox(_1c,_1d);
}
}
_1c=_1c||{};
return this.each(function(){
var _1f=$.data(this,"datetimebox");
if(_1f){
$.extend(_1f.options,_1c);
}else{
$.data(this,"datetimebox",{options:$.extend({},$.fn.datetimebox.defaults,$.fn.datetimebox.parseOptions(this),_1c)});
}
_1(this);
});
};
$.fn.datetimebox.methods={options:function(jq){
return $.data(jq[0],"datetimebox").options;
},spinner:function(jq){
return $.data(jq[0],"datetimebox").spinner;
},setValue:function(jq,_20){
return jq.each(function(){
_9(this,_20);
});
}};
$.fn.datetimebox.parseOptions=function(_21){
var t=$(_21);
return $.extend({},$.fn.datebox.parseOptions(_21),$.parser.parseOptions(_21,["timeSeparator",{showSeconds:"boolean"}]));
};
$.fn.datetimebox.defaults=$.extend({},$.fn.datebox.defaults,{showSeconds:true,timeSeparator:":",keyHandler:{up:function(){
},down:function(){
},enter:function(){
_f(this);
},query:function(q){
_d(this,q);
}},formatter:function(_22){
var h=_22.getHours();
var M=_22.getMinutes();
var s=_22.getSeconds();
function _23(_24){
return (_24<10?"0":"")+_24;
};
var _25=$(this).datetimebox("spinner").timespinner("options").separator;
var r=$.fn.datebox.defaults.formatter(_22)+" "+_23(h)+_25+_23(M);
if($(this).datetimebox("options").showSeconds){
r+=_25+_23(s);
}
return r;
},parser:function(s){
if($.trim(s)==""){
return new Date();
}
var dt=s.split(" ");
var d=$.fn.datebox.defaults.parser(dt[0]);
if(dt.length<2){
return d;
}
var _26=$(this).datetimebox("spinner").timespinner("options").separator;
var tt=dt[1].split(_26);
var _27=parseInt(tt[0],10)||0;
var _28=parseInt(tt[1],10)||0;
var _29=parseInt(tt[2],10)||0;
return new Date(d.getFullYear(),d.getMonth(),d.getDate(),_27,_28,_29);
}});
})(jQuery);


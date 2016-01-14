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
function _1(_2,_3){
var _4=$.data(_2,"combo").options;
var _5=$.data(_2,"combo").combo;
var _6=$.data(_2,"combo").panel;
if(_3){
_4.width=_3;
}
_5.appendTo("body");
if(isNaN(_4.width)){
_4.width=_5.find("input.combo-text").outerWidth();
}
var _7=0;
if(_4.hasDownArrow){
_7=_5.find(".combo-arrow").outerWidth();
}
_5.find("input.combo-text").width(0);
_5._outerWidth(_4.width);
_5.find("input.combo-text").width(_5.width()-_7);
_6.panel("resize",{width:(_4.panelWidth?_4.panelWidth:_5.outerWidth()),height:_4.panelHeight});
_5.insertAfter(_2);
};
function _8(_9){
var _a=$.data(_9,"combo").options;
var _b=$.data(_9,"combo").combo;
if(_a.hasDownArrow){
_b.find(".combo-arrow").show();
}else{
_b.find(".combo-arrow").hide();
}
};
function _c(_d){
$(_d).addClass("combo-f").hide();
var _e=$("<span class=\"combo\"></span>").insertAfter(_d);
var _f=$("<input type=\"text\" class=\"combo-text\">").appendTo(_e);
$("<span><span class=\"combo-arrow\"></span></span>").appendTo(_e);
$("<input type=\"hidden\" class=\"combo-value\">").appendTo(_e);
var _10=$("<div class=\"combo-panel\"></div>").appendTo("body");
_10.panel({doSize:false,closed:true,cls:"combo-p",style:{position:"absolute",zIndex:10},onOpen:function(){
$(this).panel("resize");
}});
var _11=$(_d).attr("name");
if(_11){
_e.find("input.combo-value").attr("name",_11);
$(_d).removeAttr("name").attr("comboName",_11);
}
_f.attr("autocomplete","off");
return {combo:_e,panel:_10};
};
function _12(_13){
var _14=$.data(_13,"combo").combo.find("input.combo-text");
_14.validatebox("destroy");
$.data(_13,"combo").panel.panel("destroy");
$.data(_13,"combo").combo.remove();
$(_13).remove();
};
function _15(_16){
var _17=$.data(_16,"combo");
var _18=_17.options;
var _19=$.data(_16,"combo").combo;
var _1a=$.data(_16,"combo").panel;
var _1b=_19.find(".combo-text");
var _1c=_19.find(".combo-arrow");
$(document).unbind(".combo").bind("mousedown.combo",function(e){
var _1d=$("body>div.combo-p>div.combo-panel");
var p=$(e.target).closest("div.combo-panel",_1d);
if(p.length){
return;
}
_1d.panel("close");
});
_19.unbind(".combo");
_1a.unbind(".combo");
_1b.unbind(".combo");
_1c.unbind(".combo");
if(!_18.disabled){
_1b.bind("mousedown.combo",function(e){
e.stopPropagation();
}).bind("keydown.combo",function(e){
switch(e.keyCode){
case 38:
_18.keyHandler.up.call(_16);
break;
case 40:
_18.keyHandler.down.call(_16);
break;
case 13:
e.preventDefault();
_18.keyHandler.enter.call(_16);
return false;
case 9:
case 27:
_26(_16);
break;
default:
if(_18.editable){
if(_17.timer){
clearTimeout(_17.timer);
}
_17.timer=setTimeout(function(){
var q=_1b.val();
if(_17.previousValue!=q){
_17.previousValue=q;
_1e(_16);
_18.keyHandler.query.call(_16,_1b.val());
_2a(_16,true);
}
},_18.delay);
}
}
});
_1c.bind("click.combo",function(){
if(_1a.is(":visible")){
_26(_16);
}else{
$("div.combo-panel").panel("close");
_1e(_16);
}
_1b.focus();
}).bind("mouseenter.combo",function(){
$(this).addClass("combo-arrow-hover");
}).bind("mouseleave.combo",function(){
$(this).removeClass("combo-arrow-hover");
}).bind("mousedown.combo",function(){
return false;
});
}
};
function _1e(_1f){
var _20=$.data(_1f,"combo").options;
var _21=$.data(_1f,"combo").combo;
var _22=$.data(_1f,"combo").panel;
if($.fn.window){
_22.panel("panel").css("z-index",$.fn.window.defaults.zIndex++);
}
_22.panel("move",{left:_21.offset().left,top:_23()});
_22.panel("open");
_20.onShowPanel.call(_1f);
(function(){
if(_22.is(":visible")){
_22.panel("move",{left:_24(),top:_23()});
setTimeout(arguments.callee,200);
}
})();
function _24(){
var _25=_21.offset().left;
if(_25+_22._outerWidth()>$(window)._outerWidth()+$(document).scrollLeft()){
_25=$(window)._outerWidth()+$(document).scrollLeft()-_22._outerWidth();
}
if(_25<0){
_25=0;
}
return _25;
};
function _23(){
var top=_21.offset().top+_21._outerHeight();
if(top+_22._outerHeight()>$(window)._outerHeight()+$(document).scrollTop()){
top=_21.offset().top-_22._outerHeight();
}
if(top<$(document).scrollTop()){
top=_21.offset().top+_21._outerHeight();
}
return top;
};
};
function _26(_27){
var _28=$.data(_27,"combo").options;
var _29=$.data(_27,"combo").panel;
_29.panel("close");
_28.onHidePanel.call(_27);
};
function _2a(_2b,_2c){
var _2d=$.data(_2b,"combo").options;
var _2e=$.data(_2b,"combo").combo.find("input.combo-text");
_2e.validatebox(_2d);
if(_2c){
_2e.validatebox("validate");
}
};
function _2f(_30,_31){
var _32=$.data(_30,"combo").options;
var _33=$.data(_30,"combo").combo;
if(_31){
_32.disabled=true;
$(_30).attr("disabled",true);
_33.find(".combo-value").attr("disabled",true);
_33.find(".combo-text").attr("disabled",true);
}else{
_32.disabled=false;
$(_30).removeAttr("disabled");
_33.find(".combo-value").removeAttr("disabled");
_33.find(".combo-text").removeAttr("disabled");
}
};
function _34(_35){
var _36=$.data(_35,"combo").options;
var _37=$.data(_35,"combo").combo;
if(_36.multiple){
_37.find("input.combo-value").remove();
}else{
_37.find("input.combo-value").val("");
}
_37.find("input.combo-text").val("");
};
function _38(_39){
var _3a=$.data(_39,"combo").combo;
return _3a.find("input.combo-text").val();
};
function _3b(_3c,_3d){
var _3e=$.data(_3c,"combo").combo;
_3e.find("input.combo-text").val(_3d);
_2a(_3c,true);
$.data(_3c,"combo").previousValue=_3d;
};
function _3f(_40){
var _41=[];
var _42=$.data(_40,"combo").combo;
_42.find("input.combo-value").each(function(){
_41.push($(this).val());
});
return _41;
};
function _43(_44,_45){
var _46=$.data(_44,"combo").options;
var _47=_3f(_44);
var _48=$.data(_44,"combo").combo;
_48.find("input.combo-value").remove();
var _49=$(_44).attr("comboName");
for(var i=0;i<_45.length;i++){
var _4a=$("<input type=\"hidden\" class=\"combo-value\">").appendTo(_48);
if(_49){
_4a.attr("name",_49);
}
_4a.val(_45[i]);
}
var tmp=[];
for(var i=0;i<_47.length;i++){
tmp[i]=_47[i];
}
var aa=[];
for(var i=0;i<_45.length;i++){
for(var j=0;j<tmp.length;j++){
if(_45[i]==tmp[j]){
aa.push(_45[i]);
tmp.splice(j,1);
break;
}
}
}
if(aa.length!=_45.length||_45.length!=_47.length){
if(_46.multiple){
_46.onChange.call(_44,_45,_47);
}else{
_46.onChange.call(_44,_45[0],_47[0]);
}
}
};
function _4b(_4c){
var _4d=_3f(_4c);
return _4d[0];
};
function _4e(_4f,_50){
_43(_4f,[_50]);
};
function _51(_52){
var _53=$.data(_52,"combo").options;
var fn=_53.onChange;
_53.onChange=function(){
};
if(_53.multiple){
if(_53.value){
if(typeof _53.value=="object"){
_43(_52,_53.value);
}else{
_4e(_52,_53.value);
}
}else{
_43(_52,[]);
}
}else{
_4e(_52,_53.value);
}
_53.onChange=fn;
};
$.fn.combo=function(_54,_55){
if(typeof _54=="string"){
return $.fn.combo.methods[_54](this,_55);
}
_54=_54||{};
return this.each(function(){
var _56=$.data(this,"combo");
if(_56){
$.extend(_56.options,_54);
}else{
var r=_c(this);
_56=$.data(this,"combo",{options:$.extend({},$.fn.combo.defaults,$.fn.combo.parseOptions(this),_54),combo:r.combo,panel:r.panel,previousValue:null});
$(this).removeAttr("disabled");
}
$("input.combo-text",_56.combo).attr("readonly",!_56.options.editable);
_8(this);
_2f(this,_56.options.disabled);
_1(this);
_15(this);
_2a(this);
_51(this);
});
};
$.fn.combo.methods={options:function(jq){
return $.data(jq[0],"combo").options;
},panel:function(jq){
return $.data(jq[0],"combo").panel;
},textbox:function(jq){
return $.data(jq[0],"combo").combo.find("input.combo-text");
},destroy:function(jq){
return jq.each(function(){
_12(this);
});
},resize:function(jq,_57){
return jq.each(function(){
_1(this,_57);
});
},showPanel:function(jq){
return jq.each(function(){
_1e(this);
});
},hidePanel:function(jq){
return jq.each(function(){
_26(this);
});
},disable:function(jq){
return jq.each(function(){
_2f(this,true);
_15(this);
});
},enable:function(jq){
return jq.each(function(){
_2f(this,false);
_15(this);
});
},validate:function(jq){
return jq.each(function(){
_2a(this,true);
});
},isValid:function(jq){
var _58=$.data(jq[0],"combo").combo.find("input.combo-text");
return _58.validatebox("isValid");
},clear:function(jq){
return jq.each(function(){
_34(this);
});
},getText:function(jq){
return _38(jq[0]);
},setText:function(jq,_59){
return jq.each(function(){
_3b(this,_59);
});
},getValues:function(jq){
return _3f(jq[0]);
},setValues:function(jq,_5a){
return jq.each(function(){
_43(this,_5a);
});
},getValue:function(jq){
return _4b(jq[0]);
},setValue:function(jq,_5b){
return jq.each(function(){
_4e(this,_5b);
});
}};
$.fn.combo.parseOptions=function(_5c){
var t=$(_5c);
return $.extend({},$.fn.validatebox.parseOptions(_5c),$.parser.parseOptions(_5c,["width","separator",{panelWidth:"number",editable:"boolean",hasDownArrow:"boolean",delay:"number"}]),{panelHeight:(t.attr("panelHeight")=="auto"?"auto":parseInt(t.attr("panelHeight"))||undefined),multiple:(t.attr("multiple")?true:undefined),disabled:(t.attr("disabled")?true:undefined),value:(t.val()||undefined)});
};
$.fn.combo.defaults=$.extend({},$.fn.validatebox.defaults,{width:"auto",panelWidth:null,panelHeight:200,multiple:false,separator:",",editable:true,disabled:false,hasDownArrow:true,value:"",delay:200,keyHandler:{up:function(){
},down:function(){
},enter:function(){
},query:function(q){
}},onShowPanel:function(){
},onHidePanel:function(){
},onChange:function(_5d,_5e){
}});
})(jQuery);


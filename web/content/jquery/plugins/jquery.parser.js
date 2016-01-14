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
$.parser={auto:true,onComplete:function(_1){
},plugins:["draggable","droppable","resizable","pagination","linkbutton","menu","menubutton","splitbutton","progressbar","tree","combobox","combotree","combogrid","numberbox","validatebox","searchbox","numberspinner","timespinner","calendar","datebox","datetimebox","slider","layout","panel","datagrid","propertygrid","treegrid","tabs","accordion","window","dialog"],parse:function(_2){
var aa=[];
for(var i=0;i<$.parser.plugins.length;i++){
var _3=$.parser.plugins[i];
var r=$(".easyui-"+_3,_2);
if(r.length){
if(r[_3]){
r[_3]();
}else{
aa.push({name:_3,jq:r});
}
}
}
if(aa.length&&window.easyloader){
var _4=[];
for(var i=0;i<aa.length;i++){
_4.push(aa[i].name);
}
easyloader.load(_4,function(){
for(var i=0;i<aa.length;i++){
var _5=aa[i].name;
var jq=aa[i].jq;
jq[_5]();
}
$.parser.onComplete.call($.parser,_2);
});
}else{
$.parser.onComplete.call($.parser,_2);
}
},parseOptions:function(_6,_7){
var t=$(_6);
var _8={};
var s=$.trim(t.attr("data-options"));
if(s){
var _9=s.substring(0,1);
var _a=s.substring(s.length-1,1);
if(_9!="{"){
s="{"+s;
}
if(_a!="}"){
s=s+"}";
}
_8=(new Function("return "+s))();
}
if(_7){
var _b={};
for(var i=0;i<_7.length;i++){
var pp=_7[i];
if(typeof pp=="string"){
if(pp=="width"||pp=="height"||pp=="left"||pp=="top"){
_b[pp]=parseInt(_6.style[pp])||undefined;
}else{
_b[pp]=t.attr(pp);
}
}else{
for(var _c in pp){
var _d=pp[_c];
if(_d=="boolean"){
_b[_c]=t.attr(_c)?(t.attr(_c)=="true"):undefined;
}else{
if(_d=="number"){
_b[_c]=t.attr(_c)=="0"?0:parseFloat(t.attr(_c))||undefined;
}
}
}
}
}
$.extend(_8,_b);
}
return _8;
}};
$(function(){
if(!window.easyloader&&$.parser.auto){
$.parser.parse();
}
});
$.fn._outerWidth=function(_e){
if(_e==undefined){
if(this[0]==window){
return this.width()||document.body.clientWidth;
}
return this.outerWidth()||0;
}
return this.each(function(){
if(!$.support.boxModel&&$.browser.msie){
$(this).width(_e);
}else{
$(this).width(_e-($(this).outerWidth()-$(this).width()));
}
});
};
$.fn._outerHeight=function(_f){
if(_f==undefined){
if(this[0]==window){
return this.height()||document.body.clientHeight;
}
return this.outerHeight()||0;
}
return this.each(function(){
if(!$.support.boxModel&&$.browser.msie){
$(this).height(_f);
}else{
$(this).height(_f-($(this).outerHeight()-$(this).height()));
}
});
};
$.fn._propAttr=$.fn.prop||$.fn.attr;
})(jQuery);


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
var _3=$.data(_2,"pagination");
var _4=_3.options;
var bb=_3.bb={};
var _5={first:{iconCls:"pagination-first",handler:function(){
if(_4.pageNumber>1){
_d(_2,1);
}
}},prev:{iconCls:"pagination-prev",handler:function(){
if(_4.pageNumber>1){
_d(_2,_4.pageNumber-1);
}
}},next:{iconCls:"pagination-next",handler:function(){
var _6=Math.ceil(_4.total/_4.pageSize);
if(_4.pageNumber<_6){
_d(_2,_4.pageNumber+1);
}
}},last:{iconCls:"pagination-last",handler:function(){
var _7=Math.ceil(_4.total/_4.pageSize);
if(_4.pageNumber<_7){
_d(_2,_7);
}
}},refresh:{iconCls:"pagination-load",handler:function(){
if(_4.onBeforeRefresh.call(_2,_4.pageNumber,_4.pageSize)!=false){
_d(_2,_4.pageNumber);
_4.onRefresh.call(_2,_4.pageNumber,_4.pageSize);
}
}}};
var _8=$(_2).addClass("pagination").html("<table cellspacing=\"0\" cellpadding=\"0\" border=\"0\"><tr></tr></table>");
var tr=_8.find("tr");
function _9(_a){
var a=$("<a href=\"javascript:void(0)\"></a>").appendTo(tr);
a.wrap("<td></td>");
a.linkbutton({iconCls:_5[_a].iconCls,plain:true}).unbind(".pagination").bind("click.pagination",_5[_a].handler);
return a;
};
if(_4.showPageList){
var ps=$("<select class=\"pagination-page-list\"></select>");
ps.bind("change",function(){
_4.pageSize=parseInt($(this).val());
_4.onChangePageSize.call(_2,_4.pageSize);
_d(_2,_4.pageNumber);
});
for(var i=0;i<_4.pageList.length;i++){
$("<option></option>").text(_4.pageList[i]).appendTo(ps);
}
$("<td></td>").append(ps).appendTo(tr);
$("<td><div class=\"pagination-btn-separator\"></div></td>").appendTo(tr);
}
bb.first=_9("first");
bb.prev=_9("prev");
$("<td><div class=\"pagination-btn-separator\"></div></td>").appendTo(tr);
$("<span style=\"padding-left:6px;\"></span>").html(_4.beforePageText).appendTo(tr).wrap("<td></td>");
bb.num=$("<input class=\"pagination-num\" type=\"text\" value=\"1\" size=\"2\">").appendTo(tr).wrap("<td></td>");
bb.num.unbind(".pagination").bind("keydown.pagination",function(e){
if(e.keyCode==13){
var _b=parseInt($(this).val())||1;
_d(_2,_b);
return false;
}
});
bb.after=$("<span style=\"padding-right:6px;\"></span>").appendTo(tr).wrap("<td></td>");
$("<td><div class=\"pagination-btn-separator\"></div></td>").appendTo(tr);
bb.next=_9("next");
bb.last=_9("last");
if(_4.showRefresh){
$("<td><div class=\"pagination-btn-separator\"></div></td>").appendTo(tr);
bb.refresh=_9("refresh");
}
if(_4.buttons){
$("<td><div class=\"pagination-btn-separator\"></div></td>").appendTo(tr);
for(var i=0;i<_4.buttons.length;i++){
var _c=_4.buttons[i];
if(_c=="-"){
$("<td><div class=\"pagination-btn-separator\"></div></td>").appendTo(tr);
}else{
var td=$("<td></td>").appendTo(tr);
$("<a href=\"javascript:void(0)\"></a>").appendTo(td).linkbutton($.extend(_c,{plain:true})).bind("click",eval(_c.handler||function(){
}));
}
}
}
$("<div class=\"pagination-info\"></div>").appendTo(_8);
$("<div style=\"clear:both;\"></div>").appendTo(_8);
};
function _d(_e,_f){
var _10=$.data(_e,"pagination").options;
var _11=Math.ceil(_10.total/_10.pageSize)||1;
_10.pageNumber=_f;
if(_10.pageNumber<1){
_10.pageNumber=1;
}
if(_10.pageNumber>_11){
_10.pageNumber=_11;
}
_12(_e,{pageNumber:_10.pageNumber});
_10.onSelectPage.call(_e,_10.pageNumber,_10.pageSize);
};
function _12(_13,_14){
var _15=$.data(_13,"pagination").options;
var bb=$.data(_13,"pagination").bb;
$.extend(_15,_14||{});
var ps=$(_13).find("select.pagination-page-list");
if(ps.length){
ps.val(_15.pageSize+"");
_15.pageSize=parseInt(ps.val());
}
var _16=Math.ceil(_15.total/_15.pageSize)||1;
bb.num.val(_15.pageNumber);
bb.after.html(_15.afterPageText.replace(/{pages}/,_16));
var _17=_15.displayMsg;
_17=_17.replace(/{from}/,_15.total==0?0:_15.pageSize*(_15.pageNumber-1)+1);
_17=_17.replace(/{to}/,Math.min(_15.pageSize*(_15.pageNumber),_15.total));
_17=_17.replace(/{total}/,_15.total);
$(_13).find("div.pagination-info").html(_17);
bb.first.add(bb.prev).linkbutton({disabled:(_15.pageNumber==1)});
bb.next.add(bb.last).linkbutton({disabled:(_15.pageNumber==_16)});
_18(_13,_15.loading);
};
function _18(_19,_1a){
var _1b=$.data(_19,"pagination").options;
var bb=$.data(_19,"pagination").bb;
_1b.loading=_1a;
if(_1b.showRefresh){
if(_1b.loading){
bb.refresh.linkbutton({iconCls:"pagination-loading"});
}else{
bb.refresh.linkbutton({iconCls:"pagination-load"});
}
}
};
$.fn.pagination=function(_1c,_1d){
if(typeof _1c=="string"){
return $.fn.pagination.methods[_1c](this,_1d);
}
_1c=_1c||{};
return this.each(function(){
var _1e;
var _1f=$.data(this,"pagination");
if(_1f){
_1e=$.extend(_1f.options,_1c);
}else{
_1e=$.extend({},$.fn.pagination.defaults,$.fn.pagination.parseOptions(this),_1c);
$.data(this,"pagination",{options:_1e});
}
_1(this);
_12(this);
});
};
$.fn.pagination.methods={options:function(jq){
return $.data(jq[0],"pagination").options;
},loading:function(jq){
return jq.each(function(){
_18(this,true);
});
},loaded:function(jq){
return jq.each(function(){
_18(this,false);
});
},refresh:function(jq,_20){
return jq.each(function(){
_12(this,_20);
});
},select:function(jq,_21){
return jq.each(function(){
_d(this,_21);
});
}};
$.fn.pagination.parseOptions=function(_22){
var t=$(_22);
return $.extend({},$.parser.parseOptions(_22,[{total:"number",pageSize:"number",pageNumber:"number"},{loading:"boolean",showPageList:"boolean",showRefresh:"boolean"}]),{pageList:(t.attr("pageList")?eval(t.attr("pageList")):undefined)});
};
$.fn.pagination.defaults={total:1,pageSize:10,pageNumber:1,pageList:[10,20,30,50],loading:false,buttons:null,showPageList:true,showRefresh:true,onSelectPage:function(_23,_24){
},onBeforeRefresh:function(_25,_26){
},onRefresh:function(_27,_28){
},onChangePageSize:function(_29){
},beforePageText:"Page",afterPageText:"of {pages}",displayMsg:"Displaying {from} to {to} of {total} items"};
})(jQuery);


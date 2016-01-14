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
var _1;
function _2(_3){
var _4=$.data(_3,"propertygrid");
var _5=$.data(_3,"propertygrid").options;
$(_3).datagrid($.extend({},_5,{cls:"propertygrid",view:(_5.showGroup?_6:undefined),onClickRow:function(_7,_8){
if(_1!=this){
_9();
_1=this;
}
if(_5.editIndex!=_7&&_8.editor){
var _a=$(this).datagrid("getColumnOption","value");
_a.editor=_8.editor;
_9();
$(this).datagrid("beginEdit",_7);
$(this).datagrid("getEditors",_7)[0].target.focus();
_5.editIndex=_7;
}
_5.onClickRow.call(_3,_7,_8);
},onLoadSuccess:function(_b){
$(_3).datagrid("getPanel").find("div.datagrid-group").css("border","");
_5.onLoadSuccess.call(_3,_b);
}}));
$(document).unbind(".propertygrid").bind("mousedown.propertygrid",function(e){
var p=$(e.target).closest("div.propertygrid,div.combo-panel");
if(p.length){
return;
}
_9();
});
function _9(){
var t=$(_1);
if(!t.length){
return;
}
var _c=$.data(_1,"propertygrid").options;
var _d=_c.editIndex;
if(_d==undefined){
return;
}
t.datagrid("getEditors",_d)[0].target.blur();
if(t.datagrid("validateRow",_d)){
t.datagrid("endEdit",_d);
}else{
t.datagrid("cancelEdit",_d);
}
_c.editIndex=undefined;
};
};
$.fn.propertygrid=function(_e,_f){
if(typeof _e=="string"){
var _10=$.fn.propertygrid.methods[_e];
if(_10){
return _10(this,_f);
}else{
return this.datagrid(_e,_f);
}
}
_e=_e||{};
return this.each(function(){
var _11=$.data(this,"propertygrid");
if(_11){
$.extend(_11.options,_e);
}else{
var _12=$.extend({},$.fn.propertygrid.defaults,$.fn.propertygrid.parseOptions(this),_e);
_12.frozenColumns=$.extend(true,[],_12.frozenColumns);
_12.columns=$.extend(true,[],_12.columns);
$.data(this,"propertygrid",{options:_12});
}
_2(this);
});
};
$.fn.propertygrid.methods={};
$.fn.propertygrid.parseOptions=function(_13){
var t=$(_13);
return $.extend({},$.fn.datagrid.parseOptions(_13),$.parser.parseOptions(_13,[{showGroup:"boolean"}]));
};
var _6=$.extend({},$.fn.datagrid.defaults.view,{render:function(_14,_15,_16){
var _17=$.data(_14,"datagrid");
var _18=_17.options;
var _19=_17.data.rows;
var _1a=$(_14).datagrid("getColumnFields",_16);
var _1b=[];
var _1c=0;
var _1d=this.groups;
for(var i=0;i<_1d.length;i++){
var _1e=_1d[i];
_1b.push("<div class=\"datagrid-group\" group-index="+i+" style=\"height:25px;overflow:hidden;border-bottom:1px solid #ccc;\">");
_1b.push("<table cellspacing=\"0\" cellpadding=\"0\" border=\"0\" style=\"height:100%\"><tbody>");
_1b.push("<tr>");
_1b.push("<td style=\"border:0;\">");
if(!_16){
_1b.push("<span style=\"color:#666;font-weight:bold;\">");
_1b.push(_18.groupFormatter.call(_14,_1e.fvalue,_1e.rows));
_1b.push("</span>");
}
_1b.push("</td>");
_1b.push("</tr>");
_1b.push("</tbody></table>");
_1b.push("</div>");
_1b.push("<table class=\"datagrid-btable\" cellspacing=\"0\" cellpadding=\"0\" border=\"0\"><tbody>");
for(var j=0;j<_1e.rows.length;j++){
var cls=(_1c%2&&_18.striped)?"class=\"datagrid-row datagrid-row-alt\"":"class=\"datagrid-row\"";
var _1f=_18.rowStyler?_18.rowStyler.call(_14,_1c,_1e.rows[j]):"";
var _20=_1f?"style=\""+_1f+"\"":"";
var _21=_17.rowIdPrefix+"-"+(_16?1:2)+"-"+_1c;
_1b.push("<tr id=\""+_21+"\" datagrid-row-index=\""+_1c+"\" "+cls+" "+_20+">");
_1b.push(this.renderRow.call(this,_14,_1a,_16,_1c,_1e.rows[j]));
_1b.push("</tr>");
_1c++;
}
_1b.push("</tbody></table>");
}
$(_15).html(_1b.join(""));
},onAfterRender:function(_22){
var _23=$.data(_22,"datagrid").options;
var dc=$.data(_22,"datagrid").dc;
var _24=dc.view;
var _25=dc.view1;
var _26=dc.view2;
$.fn.datagrid.defaults.view.onAfterRender.call(this,_22);
if(_23.rownumbers||_23.frozenColumns.length){
var _27=_25.find("div.datagrid-group");
}else{
var _27=_26.find("div.datagrid-group");
}
$("<td style=\"border:0\"><div class=\"datagrid-row-expander datagrid-row-collapse\" style=\"width:25px;height:16px;cursor:pointer\"></div></td>").insertBefore(_27.find("td"));
_24.find("div.datagrid-group").each(function(){
var _28=$(this).attr("group-index");
$(this).find("div.datagrid-row-expander").bind("click",{groupIndex:_28},function(e){
if($(this).hasClass("datagrid-row-collapse")){
$(_22).datagrid("collapseGroup",e.data.groupIndex);
}else{
$(_22).datagrid("expandGroup",e.data.groupIndex);
}
});
});
},onBeforeRender:function(_29,_2a){
var _2b=$.data(_29,"datagrid").options;
var _2c=[];
for(var i=0;i<_2a.length;i++){
var row=_2a[i];
var _2d=_2e(row[_2b.groupField]);
if(!_2d){
_2d={fvalue:row[_2b.groupField],rows:[row],startRow:i};
_2c.push(_2d);
}else{
_2d.rows.push(row);
}
}
function _2e(_2f){
for(var i=0;i<_2c.length;i++){
var _30=_2c[i];
if(_30.fvalue==_2f){
return _30;
}
}
return null;
};
this.groups=_2c;
var _31=[];
for(var i=0;i<_2c.length;i++){
var _2d=_2c[i];
for(var j=0;j<_2d.rows.length;j++){
_31.push(_2d.rows[j]);
}
}
$.data(_29,"datagrid").data.rows=_31;
}});
$.extend($.fn.datagrid.methods,{expandGroup:function(jq,_32){
return jq.each(function(){
var _33=$.data(this,"datagrid").dc.view;
if(_32!=undefined){
var _34=_33.find("div.datagrid-group[group-index=\""+_32+"\"]");
}else{
var _34=_33.find("div.datagrid-group");
}
var _35=_34.find("div.datagrid-row-expander");
if(_35.hasClass("datagrid-row-expand")){
_35.removeClass("datagrid-row-expand").addClass("datagrid-row-collapse");
_34.next("table").show();
}
$(this).datagrid("fixRowHeight");
});
},collapseGroup:function(jq,_36){
return jq.each(function(){
var _37=$.data(this,"datagrid").dc.view;
if(_36!=undefined){
var _38=_37.find("div.datagrid-group[group-index=\""+_36+"\"]");
}else{
var _38=_37.find("div.datagrid-group");
}
var _39=_38.find("div.datagrid-row-expander");
if(_39.hasClass("datagrid-row-collapse")){
_39.removeClass("datagrid-row-collapse").addClass("datagrid-row-expand");
_38.next("table").hide();
}
$(this).datagrid("fixRowHeight");
});
}});
$.fn.propertygrid.defaults=$.extend({},$.fn.datagrid.defaults,{singleSelect:true,remoteSort:false,fitColumns:true,loadMsg:"",frozenColumns:[[{field:"f",width:16,resizable:false}]],columns:[[{field:"name",title:"Name",width:100,sortable:true},{field:"value",title:"Value",width:100,resizable:false}]],showGroup:false,groupField:"group",groupFormatter:function(_3a,_3b){
return _3a;
}});
})(jQuery);


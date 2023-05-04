var selectItem_manage_tool = null; 
$(function () { 
	initSelectItemManageTool(); //建立SelectItem管理对象
	selectItem_manage_tool.init(); //如果需要通过下拉框查询，首先初始化下拉框的值
	$("#selectItem_manage").datagrid({
		url : '/SelectItem/teacherList',
		queryParams: {
			"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
		},
		fit : true,
		fitColumns : true,
		striped : true,
		rownumbers : true,
		border : false,
		pagination : true,
		pageSize : 5,
		pageList : [5, 10, 15, 20, 25],
		pageNumber : 1,
		sortName : "selectItemId",
		sortOrder : "desc",
		toolbar : "#selectItem_manage_tool",
		columns : [[
			{
				field : "selectItemId",
				title : "选题id",
				width : 70,
			},
			{
				field : "subjectObj",
				title : "论文题目",
				width : 140,
			},

			{
				field : "studentObj",
				title : "选题学生",
				width : 140,
			},
			{
				field : "reason",
				title : "选题原因",
				width : 140,
			},
			{
				field : "selectTime",
				title : "选题时间",
				width : 140,
			},
			{
				field : "shenHeState",
				title : "审核状态",
				width : 140,
			},
			{
				field : "shenHeTime",
				title : "审核时间",
				width : 140,
			},
		]],
	});

	$("#selectItemEditDiv").dialog({
		title : "修改管理",
		top: "50px",
		width : 700,
		height : 515,
		modal : true,
		closed : true,
		iconCls : "icon-edit-new",
		buttons : [{
			text : "提交",
			iconCls : "icon-edit-new",
			handler : function () {
				if ($("#selectItemEditForm").form("validate")) {
					//验证表单 
					if(!$("#selectItemEditForm").form("validate")) {
						$.messager.alert("错误提示","你输入的信息还有错误！","warning");
					} else {
						$("#selectItemEditForm").form({
						    url:"/SelectItem/update/" + $("#selectItem_selectItemId_edit").val(),
						    onSubmit: function(){
								if($("#selectItemEditForm").form("validate"))  {
				                	$.messager.progress({
										text : "正在提交数据中...",
									});
				                	return true;
				                } else { 
				                    return false; 
				                }
						    },
						    success:function(data){
						    	$.messager.progress("close");
						    	console.log(data);
			                	var obj = jQuery.parseJSON(data);
			                    if(obj.success){
			                        $.messager.alert("消息","信息修改成功！");
			                        $("#selectItemEditDiv").dialog("close");
			                        selectItem_manage_tool.reload();
			                    }else{
			                        $.messager.alert("消息",obj.message);
			                    } 
						    }
						});
						//提交表单
						$("#selectItemEditForm").submit();
					}
				}
			},
		},{
			text : "取消",
			iconCls : "icon-redo",
			handler : function () {
				$("#selectItemEditDiv").dialog("close");
				$("#selectItemEditForm").form("reset"); 
			},
		}],
	});
});

function initSelectItemManageTool() {
	selectItem_manage_tool = {
		init: function() {
			$.ajax({
				url : "/Subject/listAll",
				data: {
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
				type : "get",
				success : function (data, response, status) {
					$("#subjectObj_subjectId_query").combobox({ 
					    valueField:"subjectId",
					    textField:"subjectName",
					    panelHeight: "200px",
				        editable: false, //不允许手动输入 
					});
					data.splice(0,0,{subjectId:0,subjectName:"不限制"});
					$("#subjectObj_subjectId_query").combobox("loadData",data); 
				}
			});
			$.ajax({
				url : "/Teacher/listAll",
				data: {
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
				type : "get",
				success : function (data, response, status) {
					$("#teacherObj_teacherNumber_query").combobox({ 
					    valueField:"teacherNumber",
					    textField:"name",
					    panelHeight: "200px",
				        editable: false, //不允许手动输入 
					});
					data.splice(0,0,{teacherNumber:"",name:"不限制"});
					$("#teacherObj_teacherNumber_query").combobox("loadData",data); 
				}
			});
			$.ajax({
				url : "/UserInfo/listAll",
				data: {
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
				type : "get",
				success : function (data, response, status) {
					$("#studentObj_user_name_query").combobox({ 
					    valueField:"user_name",
					    textField:"name",
					    panelHeight: "200px",
				        editable: false, //不允许手动输入 
					});
					data.splice(0,0,{user_name:"",name:"不限制"});
					$("#studentObj_user_name_query").combobox("loadData",data); 
				}
			});
		},
		reload : function () {
			$("#selectItem_manage").datagrid("reload");
		},
		redo : function () {
			$("#selectItem_manage").datagrid("unselectAll");
		},
		search: function() {
			var queryParams = $("#selectItem_manage").datagrid("options").queryParams;
			queryParams["subjectObj.subjectId"] = $("#subjectObj_subjectId_query").combobox("getValue");
			queryParams["teacherObj.teacherNumber"] = $("#teacherObj_teacherNumber_query").combobox("getValue");
			queryParams["studentObj.user_name"] = $("#studentObj_user_name_query").combobox("getValue");
			queryParams["selectTime"] = $("#selectTime").datebox("getValue"); 
			queryParams["shenHeState"] = $("#shenHeState").val();
			queryParams["shenHeTime"] = $("#shenHeTime").datebox("getValue"); 
			queryParams["csrfmiddlewaretoken"] = $('input[name="csrfmiddlewaretoken"]').val();
			$("#selectItem_manage").datagrid("options").queryParams=queryParams; 
			$("#selectItem_manage").datagrid("load");
		},
		exportExcel: function() {
			$("#selectItemQueryForm").form({
			    url:"/SelectItem/OutToExcel?csrfmiddlewaretoken" + $('input[name="csrfmiddlewaretoken"]').val(),
			});
			//提交表单
			$("#selectItemQueryForm").submit();
		},
		remove : function () {
			var rows = $("#selectItem_manage").datagrid("getSelections");
			if (rows.length > 0) {
				$.messager.confirm("确定操作", "您正在要删除所选的记录吗？", function (flag) {
					if (flag) {
						var selectItemIds = [];
						for (var i = 0; i < rows.length; i ++) {
							selectItemIds.push(rows[i].selectItemId);
						}
						$.ajax({
							type : "POST",
							url : "/SelectItem/deletes",
							data : {
								selectItemIds : selectItemIds.join(","),
								"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
							},
							beforeSend : function () {
								$("#selectItem_manage").datagrid("loading");
							},
							success : function (data) {
								if (data.success) {
									$("#selectItem_manage").datagrid("loaded");
									$("#selectItem_manage").datagrid("load");
									$("#selectItem_manage").datagrid("unselectAll");
									$.messager.show({
										title : "提示",
										msg : data.message
									});
								} else {
									$("#selectItem_manage").datagrid("loaded");
									$("#selectItem_manage").datagrid("load");
									$("#selectItem_manage").datagrid("unselectAll");
									$.messager.alert("消息",data.message);
								}
							},
						});
					}
				});
			} else {
				$.messager.alert("提示", "请选择要删除的记录！", "info");
			}
		},
		edit : function () {
			var rows = $("#selectItem_manage").datagrid("getSelections");
			if (rows.length > 1) {
				$.messager.alert("警告操作！", "编辑记录只能选定一条数据！", "warning");
			} else if (rows.length == 1) {
				$.ajax({
					url : "/SelectItem/update/" + rows[0].selectItemId,
					type : "get",
					data : {
						//selectItemId : rows[0].selectItemId,
					},
					beforeSend : function () {
						$.messager.progress({
							text : "正在获取中...",
						});
					},
					success : function (selectItem, response, status) {
						$.messager.progress("close");
						if (selectItem) { 
							$("#selectItemEditDiv").dialog("open");
							$("#selectItem_selectItemId_edit").val(selectItem.selectItemId);
							$("#selectItem_selectItemId_edit").validatebox({
								required : true,
								missingMessage : "请输入选题id",
								editable: false
							});
							$("#selectItem_subjectObj_subjectId_edit").combobox({
								url:"/Subject/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"subjectId",
							    textField:"subjectName",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#selectItem_subjectObj_subjectId_edit").combobox("select", selectItem.subjectObjPri);
									//var data = $("#selectItem_subjectObj_subjectId_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#selectItem_subjectObj_subjectId_edit").combobox("select", data[0].subjectId);
						            //}
								}
							});
							$("#selectItem_teacherObj_teacherNumber_edit").combobox({
								url:"/Teacher/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"teacherNumber",
							    textField:"name",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#selectItem_teacherObj_teacherNumber_edit").combobox("select", selectItem.teacherObjPri);
									//var data = $("#selectItem_teacherObj_teacherNumber_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#selectItem_teacherObj_teacherNumber_edit").combobox("select", data[0].teacherNumber);
						            //}
								}
							});
							$("#selectItem_studentObj_user_name_edit").combobox({
								url:"/UserInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"user_name",
							    textField:"name",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#selectItem_studentObj_user_name_edit").combobox("select", selectItem.studentObjPri);
									//var data = $("#selectItem_studentObj_user_name_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#selectItem_studentObj_user_name_edit").combobox("select", data[0].user_name);
						            //}
								}
							});
							$("#selectItem_reason_edit").val(selectItem.reason);
							$("#selectItem_reason_edit").validatebox({
								required : true,
								missingMessage : "请输入选题原因",
							});
							$("#selectItem_selectTime_edit").datetimebox({
								value: selectItem.selectTime,
							    required: true,
							    showSeconds: true,
							});
							$("#selectItem_shenHeState_edit").val(selectItem.shenHeState);
							$("#selectItem_shenHeState_edit").validatebox({
								required : true,
								missingMessage : "请输入审核状态",
							});
							$("#selectItem_shenHeTime_edit").datetimebox({
								value: selectItem.shenHeTime,
							    required: true,
							    showSeconds: true,
							});
							$("#selectItem_teacherReply_edit").val(selectItem.teacherReply);
						} else {
							$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
						}
					}
				});
			} else if (rows.length == 0) {
				$.messager.alert("警告操作！", "编辑记录至少选定一条数据！", "warning");
			}
		},
	};
}

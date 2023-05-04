var subjectType_manage_tool = null; 
$(function () { 
	initSubjectTypeManageTool(); //建立SubjectType管理对象
	subjectType_manage_tool.init(); //如果需要通过下拉框查询，首先初始化下拉框的值
	$("#subjectType_manage").datagrid({
		url : '/SubjectType/list',
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
		sortName : "subjectTypeId",
		sortOrder : "desc",
		toolbar : "#subjectType_manage_tool",
		columns : [[
			{
				field : "subjectTypeId",
				title : "类型编号",
				width : 70,
			},
			{
				field : "subjectTypeName",
				title : "类型名称",
				width : 140,
			},
			{
				field : "subjectTypeDesc",
				title : "类型说明",
				width : 140,
			},
		]],
	});

	$("#subjectTypeEditDiv").dialog({
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
				if ($("#subjectTypeEditForm").form("validate")) {
					//验证表单 
					if(!$("#subjectTypeEditForm").form("validate")) {
						$.messager.alert("错误提示","你输入的信息还有错误！","warning");
					} else {
						$("#subjectTypeEditForm").form({
						    url:"/SubjectType/update/" + $("#subjectType_subjectTypeId_edit").val(),
						    onSubmit: function(){
								if($("#subjectTypeEditForm").form("validate"))  {
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
			                        $("#subjectTypeEditDiv").dialog("close");
			                        subjectType_manage_tool.reload();
			                    }else{
			                        $.messager.alert("消息",obj.message);
			                    } 
						    }
						});
						//提交表单
						$("#subjectTypeEditForm").submit();
					}
				}
			},
		},{
			text : "取消",
			iconCls : "icon-redo",
			handler : function () {
				$("#subjectTypeEditDiv").dialog("close");
				$("#subjectTypeEditForm").form("reset"); 
			},
		}],
	});
});

function initSubjectTypeManageTool() {
	subjectType_manage_tool = {
		init: function() {
		},
		reload : function () {
			$("#subjectType_manage").datagrid("reload");
		},
		redo : function () {
			$("#subjectType_manage").datagrid("unselectAll");
		},
		search: function() {
			$("#subjectType_manage").datagrid("options").queryParams=queryParams; 
			$("#subjectType_manage").datagrid("load");
		},
		exportExcel: function() {
			$("#subjectTypeQueryForm").form({
			    url:"/SubjectType/OutToExcel?csrfmiddlewaretoken" + $('input[name="csrfmiddlewaretoken"]').val(),
			});
			//提交表单
			$("#subjectTypeQueryForm").submit();
		},
		remove : function () {
			var rows = $("#subjectType_manage").datagrid("getSelections");
			if (rows.length > 0) {
				$.messager.confirm("确定操作", "您正在要删除所选的记录吗？", function (flag) {
					if (flag) {
						var subjectTypeIds = [];
						for (var i = 0; i < rows.length; i ++) {
							subjectTypeIds.push(rows[i].subjectTypeId);
						}
						$.ajax({
							type : "POST",
							url : "/SubjectType/deletes",
							data : {
								subjectTypeIds : subjectTypeIds.join(","),
								"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
							},
							beforeSend : function () {
								$("#subjectType_manage").datagrid("loading");
							},
							success : function (data) {
								if (data.success) {
									$("#subjectType_manage").datagrid("loaded");
									$("#subjectType_manage").datagrid("load");
									$("#subjectType_manage").datagrid("unselectAll");
									$.messager.show({
										title : "提示",
										msg : data.message
									});
								} else {
									$("#subjectType_manage").datagrid("loaded");
									$("#subjectType_manage").datagrid("load");
									$("#subjectType_manage").datagrid("unselectAll");
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
			var rows = $("#subjectType_manage").datagrid("getSelections");
			if (rows.length > 1) {
				$.messager.alert("警告操作！", "编辑记录只能选定一条数据！", "warning");
			} else if (rows.length == 1) {
				$.ajax({
					url : "/SubjectType/update/" + rows[0].subjectTypeId,
					type : "get",
					data : {
						//subjectTypeId : rows[0].subjectTypeId,
					},
					beforeSend : function () {
						$.messager.progress({
							text : "正在获取中...",
						});
					},
					success : function (subjectType, response, status) {
						$.messager.progress("close");
						if (subjectType) { 
							$("#subjectTypeEditDiv").dialog("open");
							$("#subjectType_subjectTypeId_edit").val(subjectType.subjectTypeId);
							$("#subjectType_subjectTypeId_edit").validatebox({
								required : true,
								missingMessage : "请输入类型编号",
								editable: false
							});
							$("#subjectType_subjectTypeName_edit").val(subjectType.subjectTypeName);
							$("#subjectType_subjectTypeName_edit").validatebox({
								required : true,
								missingMessage : "请输入类型名称",
							});
							$("#subjectType_subjectTypeDesc_edit").val(subjectType.subjectTypeDesc);
							$("#subjectType_subjectTypeDesc_edit").validatebox({
								required : true,
								missingMessage : "请输入类型说明",
							});
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

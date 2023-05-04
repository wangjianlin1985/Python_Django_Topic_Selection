$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/SelectItem/update/" + $("#selectItem_selectItemId_modify").val(),
		type : "get",
		data : {
			//selectItemId : $("#selectItem_selectItemId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (selectItem, response, status) {
			$.messager.progress("close");
			if (selectItem) { 
				$("#selectItem_selectItemId_modify").val(selectItem.selectItemId);
				$("#selectItem_selectItemId_modify").validatebox({
					required : true,
					missingMessage : "请输入选题id",
					editable: false
				});
				$("#selectItem_subjectObj_subjectId_modify").combobox({
					url:"/Subject/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"subjectId",
					textField:"subjectName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#selectItem_subjectObj_subjectId_modify").combobox("select", selectItem.subjectObjPri);
						//var data = $("#selectItem_subjectObj_subjectId_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#selectItem_subjectObj_subjectId_edit").combobox("select", data[0].subjectId);
						//}
					}
				});
				$("#selectItem_teacherObj_teacherNumber_modify").combobox({
					url:"/Teacher/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"teacherNumber",
					textField:"name",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#selectItem_teacherObj_teacherNumber_modify").combobox("select", selectItem.teacherObjPri);
						//var data = $("#selectItem_teacherObj_teacherNumber_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#selectItem_teacherObj_teacherNumber_edit").combobox("select", data[0].teacherNumber);
						//}
					}
				});
				$("#selectItem_studentObj_user_name_modify").combobox({
					url:"/UserInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"user_name",
					textField:"name",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#selectItem_studentObj_user_name_modify").combobox("select", selectItem.studentObjPri);
						//var data = $("#selectItem_studentObj_user_name_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#selectItem_studentObj_user_name_edit").combobox("select", data[0].user_name);
						//}
					}
				});
				$("#selectItem_reason_modify").val(selectItem.reason);
				$("#selectItem_reason_modify").validatebox({
					required : true,
					missingMessage : "请输入选题原因",
				});
				$("#selectItem_selectTime_modify").datetimebox({
					value: selectItem.selectTime,
					required: true,
					showSeconds: true,
				});
				$("#selectItem_shenHeState_modify").val(selectItem.shenHeState);
				$("#selectItem_shenHeState_modify").validatebox({
					required : true,
					missingMessage : "请输入审核状态",
				});
				$("#selectItem_shenHeTime_modify").datetimebox({
					value: selectItem.shenHeTime,
					required: true,
					showSeconds: true,
				});
				$("#selectItem_teacherReply_modify").val(selectItem.teacherReply);
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#selectItemModifyButton").click(function(){ 
		if ($("#selectItemModifyForm").form("validate")) {
			$("#selectItemModifyForm").form({
			    url:"SelectItem/update/" + $("#selectItem_selectItemId_modify").val(),
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
                	var obj = jQuery.parseJSON(data);
                    if(obj.success){
                        $.messager.alert("消息","信息修改成功！");
                        $(".messager-window").css("z-index",10000);
                        //location.href="frontlist";
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    } 
			    }
			});
			//提交表单
			$("#selectItemModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});

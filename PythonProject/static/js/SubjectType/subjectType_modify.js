$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/SubjectType/update/" + $("#subjectType_subjectTypeId_modify").val(),
		type : "get",
		data : {
			//subjectTypeId : $("#subjectType_subjectTypeId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (subjectType, response, status) {
			$.messager.progress("close");
			if (subjectType) { 
				$("#subjectType_subjectTypeId_modify").val(subjectType.subjectTypeId);
				$("#subjectType_subjectTypeId_modify").validatebox({
					required : true,
					missingMessage : "请输入类型编号",
					editable: false
				});
				$("#subjectType_subjectTypeName_modify").val(subjectType.subjectTypeName);
				$("#subjectType_subjectTypeName_modify").validatebox({
					required : true,
					missingMessage : "请输入类型名称",
				});
				$("#subjectType_subjectTypeDesc_modify").val(subjectType.subjectTypeDesc);
				$("#subjectType_subjectTypeDesc_modify").validatebox({
					required : true,
					missingMessage : "请输入类型说明",
				});
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#subjectTypeModifyButton").click(function(){ 
		if ($("#subjectTypeModifyForm").form("validate")) {
			$("#subjectTypeModifyForm").form({
			    url:"SubjectType/update/" + $("#subjectType_subjectTypeId_modify").val(),
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
			$("#subjectTypeModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});

$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/ClassInfo/update/" + $("#classInfo_classNumber_modify").val(),
		type : "get",
		data : {
			//classNumber : $("#classInfo_classNumber_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (classInfo, response, status) {
			$.messager.progress("close");
			if (classInfo) { 
				$("#classInfo_classNumber_modify").val(classInfo.classNumber);
				$("#classInfo_classNumber_modify").validatebox({
					required : true,
					missingMessage : "请输入班级编号",
					editable: false
				});
				$("#classInfo_specialName_modify").val(classInfo.specialName);
				$("#classInfo_specialName_modify").validatebox({
					required : true,
					missingMessage : "请输入所在专业",
				});
				$("#classInfo_className_modify").val(classInfo.className);
				$("#classInfo_className_modify").validatebox({
					required : true,
					missingMessage : "请输入班级名称",
				});
				$("#classInfo_startDate_modify").datebox({
					value: classInfo.startDate,
					required: true,
					showSeconds: true,
				});
				$("#classInfo_headTeacher_modify").val(classInfo.headTeacher);
				$("#classInfo_headTeacher_modify").validatebox({
					required : true,
					missingMessage : "请输入班主任",
				});
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#classInfoModifyButton").click(function(){ 
		if ($("#classInfoModifyForm").form("validate")) {
			$("#classInfoModifyForm").form({
			    url:"ClassInfo/update/" + $("#classInfo_classNumber_modify").val(),
			    onSubmit: function(){
					if($("#classInfoEditForm").form("validate"))  {
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
			$("#classInfoModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});

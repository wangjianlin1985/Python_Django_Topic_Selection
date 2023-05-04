$(function () {
    //实例化题目内容编辑器
    tinyMCE.init({
        selector: "#subject_content_modify",
        theme: 'advanced',
        language: "zh",
        strict_loading_mode: 1,
    });
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/Subject/update/" + $("#subject_subjectId_modify").val(),
		type : "get",
		data : {
			//subjectId : $("#subject_subjectId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (subject, response, status) {
			$.messager.progress("close");
			if (subject) { 
				$("#subject_subjectId_modify").val(subject.subjectId);
				$("#subject_subjectId_modify").validatebox({
					required : true,
					missingMessage : "请输入题目编号",
					editable: false
				});
				$("#subject_subjectTypeObj_subjectTypeId_modify").combobox({
					url:"/SubjectType/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"subjectTypeId",
					textField:"subjectTypeName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#subject_subjectTypeObj_subjectTypeId_modify").combobox("select", subject.subjectTypeObjPri);
						//var data = $("#subject_subjectTypeObj_subjectTypeId_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#subject_subjectTypeObj_subjectTypeId_edit").combobox("select", data[0].subjectTypeId);
						//}
					}
				});
				$("#subject_subjectName_modify").val(subject.subjectName);
				$("#subject_subjectName_modify").validatebox({
					required : true,
					missingMessage : "请输入题目名称",
				});
				$("#subject_subjectPhotoImgMod").attr("src", subject.subjectPhoto);
				tinyMCE.editors['subject_content_modify'].setContent(subject.content);
				$("#subject_subjectState_modify").val(subject.subjectState);
				$("#subject_subjectState_modify").validatebox({
					required : true,
					missingMessage : "请输入题目状态",
				});
				$("#subject_personNum_modify").val(subject.personNum);
				$("#subject_personNum_modify").validatebox({
					required : true,
					validType : "integer",
					missingMessage : "请输入限选人数",
					invalidMessage : "限选人数输入不对",
				});
				$("#subject_teacherObj_teacherNumber_modify").combobox({
					url:"/Teacher/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"teacherNumber",
					textField:"name",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#subject_teacherObj_teacherNumber_modify").combobox("select", subject.teacherObjPri);
						//var data = $("#subject_teacherObj_teacherNumber_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#subject_teacherObj_teacherNumber_edit").combobox("select", data[0].teacherNumber);
						//}
					}
				});
				$("#subject_addTime_modify").datetimebox({
					value: subject.addTime,
					required: true,
					showSeconds: true,
				});
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#subjectModifyButton").click(function(){ 
		if ($("#subjectModifyForm").form("validate")) {
			$("#subjectModifyForm").form({
			    url:"Subject/update/" + $("#subject_subjectId_modify").val(),
			    onSubmit: function(){
					if($("#subjectEditForm").form("validate"))  {
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
			$("#subjectModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});

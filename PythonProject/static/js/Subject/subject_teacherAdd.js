$(function () {
	//实例化题目内容编辑器
    tinyMCE.init({
        selector: "#subject_content",
        theme: 'advanced',
        language: "zh",
        strict_loading_mode: 1,
    });
	$("#subject_subjectName").validatebox({
		required : true, 
		missingMessage : '请输入题目名称',
	});

	$("#subject_subjectState").validatebox({
		required : true, 
		missingMessage : '请输入题目状态',
	});

	$("#subject_personNum").validatebox({
		required : true,
		validType : "integer",
		missingMessage : '请输入限选人数',
		invalidMessage : '限选人数输入不对',
	});

	$("#subject_addTime").datetimebox({
	    required : true, 
	    showSeconds: true,
	    editable: false
	});

	//单击添加按钮
	$("#subjectAddButton").click(function () {
		if(tinyMCE.editors['subject_content'].getContent() == "") {
			alert("请输入题目内容");
			return;
		}
		//验证表单 
		if(!$("#subjectAddForm").form("validate")) {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		} else {
			$("#subjectAddForm").form({
			    url:"/Subject/teacherAdd",
				queryParams: {
			    	"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
			    onSubmit: function(){
					if($("#subjectAddForm").form("validate"))  { 
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
                    //此处data={"Success":true}是字符串
                	var obj = jQuery.parseJSON(data); 
                    if(obj.success){ 
                        $.messager.alert("消息","保存成功！");
                        $(".messager-window").css("z-index",10000);
                        $("#subjectAddForm").form("clear");
                        tinyMCE.editors['subject_content'].setContent("");
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    }
			    }
			});
			//提交表单
			$("#subjectAddForm").submit();
		}
	});

	//单击清空按钮
	$("#subjectClearButton").click(function () { 
		//$("#subjectAddForm").form("clear"); 
		location.reload()
	});
});

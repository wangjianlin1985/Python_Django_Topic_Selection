$(function () {
	//实例化教师简介编辑器
    tinyMCE.init({
        selector: "#teacher_introduce",
        theme: 'advanced',
        language: "zh",
        strict_loading_mode: 1,
    });
	$("#teacher_teacherNumber").validatebox({
		required : true, 
		missingMessage : '请输入教师编号',
	});

	$("#teacher_password").validatebox({
		required : true, 
		missingMessage : '请输入登录密码',
	});

	$("#teacher_name").validatebox({
		required : true, 
		missingMessage : '请输入姓名',
	});

	$("#teacher_sex").validatebox({
		required : true, 
		missingMessage : '请输入性别',
	});

	$("#teacher_birthday").datebox({
	    required : true, 
	    showSeconds: true,
	    editable: false
	});

	$("#teacher_professName").validatebox({
		required : true, 
		missingMessage : '请输入职称',
	});

	$("#teacher_inDate").datebox({
	    required : true, 
	    showSeconds: true,
	    editable: false
	});

	//单击添加按钮
	$("#teacherAddButton").click(function () {
		//验证表单 
		if(!$("#teacherAddForm").form("validate")) {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		} else {
			$("#teacherAddForm").form({
			    url:"/Teacher/add",
				queryParams: {
			    	"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
			    onSubmit: function(){
					if($("#teacherAddForm").form("validate"))  { 
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
                        $("#teacherAddForm").form("clear");
                        tinyMCE.editors['teacher_introduce'].setContent("");
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    }
			    }
			});
			//提交表单
			$("#teacherAddForm").submit();
		}
	});

	//单击清空按钮
	$("#teacherClearButton").click(function () { 
		//$("#teacherAddForm").form("clear"); 
		location.reload()
	});
});

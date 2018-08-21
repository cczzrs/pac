// 该文件为输入模板
// 请将下一行'@'与'@'之间的数据，保存到网页收藏标签内容，点击标签执行，即初始化模板数据
// @javascript:(function(){jsCode=document.createElement('script');jsCode.setAttribute('src','/static/js/SH.js');document.body.appendChild(jsCode);}());@
$.fn.auto_show = function(s){
	if(!s)return;
	var ss = s.split('');
	var self = $(this);
	var i = 0;
	var T =  setInterval(function(){
		if(i<ss.length){
			self.val(self.val()+ss[i++]);
		}else{
			self.change();
		}
	},10);// 定时器
}

function pass(dbo){
	// 模板数据
	db_i = {'service_type': '对外招标',
		   			'area': '华南区',
	   			'province': '广东省',
		   			'city': '广州',
		   		'url_type': '1',
				   	'tags': '1',
			   	'run_time': '2018-08-09',
				   	 'bz1': 'bz1',
			   		 'bz2': 'bz2',
   			  	  'url_source': 'http://ghgtw.beijing.gov.cn/module/idea/que_discusslist.jsp?webid=1&appid=1&typeid=2&showtype=all',
		   'resolve_page_wait': '{"wait":"//div[@class=\\"right_left\\"]"}',
		   'resolve_next_page': '{"next":"//input[@value=\\"GO\\"]"}',
			   	'resolve_type': '1',
			   	'resolve_rule': 'XPATH',
	   		 'resolve_sources': '{"trs":[["/html/body/div[3]/div/div/div[1]/div[2]/div/table[2]/tbody/tr/td/a/../.."]]}',
		   	  'resolve_source': '{"tr":{"news_title":[["//td[@height=\\"22\\"]//a/text()"]],"url_source":[["//td[@height=\\"22\\"]//a/@href"]],"news_date":[["//td[2]/text()"]]}}',
		   			  'cpage_type': '1',
				   'cresolve_type': '1',
				   'cresolve_rule': 'XPATH',
			   	 'cresolve_source': '[["//*[@id=\\"container\\"]/div/div/div[1]/div[2]/div/table/tbody/tr/td/table[1]"]]'
		}
	if(!dbo || dbo.length < 1){dbo = db_i;}

	// 第一页，基本信息
	if (dbo['id'])$("input[name='id']").val(dbo['id']);
    $("select[name='service_type']").val(dbo['service_type']).change();
    $("input[name='area']").auto_show(dbo['area']);
    $("input[name='province']").auto_show(dbo['province']);
    $("input[name='city']").auto_show(dbo['city']);
    $("input[name='url_type']").auto_show(dbo['url_type']);
    $("select[name='tags']").val(dbo['tags']).change();
    $("input[name='run_time']").val(dbo['run_time']).change();
   	$("textarea[name='bz1']").auto_show(dbo['bz1']);
   	$("textarea[name='bz2']").auto_show(dbo['bz2']);

	// 第二页，
	$("input[name='url_source']").auto_show(dbo['url_source']);
	$("input[name='resolve_page_wait']").auto_show(dbo['resolve_page_wait']);
	$("input[name='resolve_next_page']").auto_show(dbo['resolve_next_page']);
	$("input[name='resolve_type']").auto_show(dbo['resolve_type']);
	$("input[name='resolve_rule']").auto_show(dbo['resolve_rule']);
	$("input[name='resolve_sources']").auto_show(dbo['resolve_sources']);
	$("input[name='resolve_source']").auto_show(dbo['resolve_source']);

	// 第三页，
    // $("select[name='cpage_type']").val(dbo['content_page_rule']).change();
    content_page_rule = eval("("+dbo['content_page_rule']+")");
    $("input[name='cresolve_type']").auto_show(content_page_rule['resolve_type']);
    $("input[name='cresolve_rule']").auto_show(content_page_rule['resolve_rule']);
    $("input[name='cresolve_source']").auto_show(content_page_rule['resolve_source']);
    
}
if(!pass_show){pass();} // 执行

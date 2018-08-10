// 该文件为输入模板
// 请将下一行'@'与'@'之间的数据，保存到网页收藏标签内容，点击标签执行，即初始化模板数据
// @javascript:(function(){jsCode=document.createElement('script');jsCode.setAttribute('src','http://211.159.163.183:5050/static/js/SH.js');document.body.appendChild(jsCode);}());@
$.fn.auto_show = function(s){
	var ss = s.split('');
	var self = $(this);
	var i = 0;
	var T =  setInterval(function(){
		if(i<s.length){
			self.val(self.val()+s[i++]);
		}else{
			self.change();
		}
	},10);// 定时器
}

function pass(){

	// 第一页，基本信息
    var d0_1 = '对外招标'
    var d0_2 = '华南区'
    var d0_3 = '广东省'
    var d0_4 = '广州'
    var d0_5 = '1'
    var d0_6 = '1'
    var d0_7= '2018-08-09'
    var d0_8 = 'bz1'
    var d0_9 = 'bz2'
    $("select[name='service_type']").val(d0_1).change();
    $("input[name='area']").auto_show(d0_2);
    $("input[name='province']").auto_show(d0_3);
    $("input[name='city']").auto_show(d0_4);
    $("input[name='url_type']").auto_show(d0_5);
    $("select[name='tags']").val(d0_6).change();
    $("input[name='run_time']").val(d0_7).change();
//    $("textarea[name='bz1']").auto_show(d0_8);
//    $("textarea[name='bz2']").auto_show(d0_9);


	// 第二页，
	var d1 = 'http://ghgtw.beijing.gov.cn/module/idea/que_discusslist.jsp?webid=1&appid=1&typeid=2&showtype=all';
	var d2 = '{"wait":"//div[@class=\\"right_left\\"]"}';
	var d3 = '{"next":"//input[@value=\\"GO\\"]"}';
	var d4 = '1';
	var d5 = 'XPATH';
	var d6 = '{"trs":[["/html/body/div[3]/div/div/div[1]/div[2]/div/table[2]/tbody/tr/td/a/../.."]]}'
	var d7 = '{"tr":{"news_title":[["//td[@height=\\"22\\"]//a/text()"]],"url_source":[["//td[@height=\\"22\\"]//a/@href"]],"news_date":[["//td[2]/text()"]]}}';
	$("input[name='url_source']").auto_show(d1);
	$("input[name='resolve_page_wait']").auto_show(d2);
	$("input[name='resolve_next_page']").auto_show(d3);
	$("input[name='resolve_type']").auto_show(d4);
	$("input[name='resolve_rule']").auto_show(d5);
	$("input[name='resolve_sources']").auto_show(d6);
	$("input[name='resolve_source']").auto_show(d7);


	// 第三页，
	var d2_1 = '1';
	var d2_2 = '1';
	var d2_3 = 'XPATH';
	var d2_4 = '[["//*[@id=\\"container\\"]/div/div/div[1]/div[2]/div/table/tbody/tr/td/table[1]"]]';
    $("select[name='cpage_type']").val(d2_1).change();
    $("input[name='cresolve_type']").auto_show(d2_2);
    $("input[name='cresolve_rule']").auto_show(d2_3);
    $("input[name='cresolve_source']").auto_show(d2_4);

}
$(function(){
    pass();
});

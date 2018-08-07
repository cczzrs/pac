$.fn.autotype = function(s){
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

function GOTO(){

	var d1 = 'http://ghgtw.beijing.gov.cn/module/idea/que_discusslist.jsp?webid=1&appid=1&typeid=2&showtype=all';
	var d2 = '{"wait": "//div[@class=\\"right_left\\"]"}';
	var d3 = '{"next": "//input[@value=\\"GO\\"]"}';
	var d4 = '1';
	var d5 = 'XPATH';
	var d6 = '{"trs": [["/html/body/div[3]/div/div/div[1]/div[2]/div/table[2]/tbody/tr/td/a/../.."]]}'
	var d7 = '{"tr": {"news_title": [["//td[@height=\\"22\\"]//a/text()"]],                 "url_source": [["//td[@height=\\"22\\"]//a/@href"]],                 "news_date": [["//td[2]/text()"]]}          }';
	
	var d2_1 = '1';
	var d2_2 = 'XPATH';
	var d2_3 = '[["//*[@id=\\"container\\"]/div/div/div[1]/div[2]/div/table/tbody/tr/td/table[1]/tbody/tr/td[2]/table[2]"]]';
	
	$("input[name='url_source']").autotype(d1);
	$("input[name='resolve_page_wait']").autotype(d2);
	$("input[name='resolve_next_page']").autotype(d3);
	$("input[name='resolve_type']").autotype(d4);
	$("input[name='resolve_rule']").autotype(d5);
	$("input[name='resolve_sources']").autotype(d6);
	$("input[name='resolve_source']").autotype(d7);
	
	// $("input[name='cresolve_type']").autotype(d2_1);
	// $("input[name='cresolve_rule']").autotype(d2_2);
	// $("input[name='cresolve_source']").autotype(d2_3);




}
GOTO();

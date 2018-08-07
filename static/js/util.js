// util.js 公共通用资源

$.prototype.addpAttr = function(name, value){
    function this_one(to, name, value){
        to.attr('style', to.attr(name)?to.attr(name)+value:value);
    }
    var tos = $(this);
    for (var one=0;one<tos.length;one++ ){
        this_one($(tos[one]), name, value);
    }
}

$.prototype.clickTOa = function(){
    function this_one(to){
        to.click(function(){var ba = to.find('a');if(ba.length > 0)ba[0].click()});
    }
    var tos = $(this);
    for (var one=0;one<tos.length;one++ ){
        this_one($(tos[one]));
    }
}

// 全屏背景图
$('html').addpAttr('style', 'height:100%;');
$('body').addpAttr('style', 'height:100%;background-image:url("/static/img/wizard-book.jpg");');

// 标题着色
$('h1').addpAttr('style', 'color:#f44336;');
$('h2').addpAttr('style', 'color:#f44336;');
$('h3').addpAttr('style', 'color:#f44336;');

// button 按钮点击触发所包含的 a 标签点击 click
$('button').clickTOa();



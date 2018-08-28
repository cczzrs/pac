
var charto = {}; // 显示图形集合
 
//饼状图
(function(){
    if(!document.getElementById("pie3"))return; 
var pie3 = echarts.init(document.getElementById("pie3"));

option = {
    title : {
        text: '某站点用户访问来源',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        data: ['直接访问','邮件营销','联盟广告','视频广告','搜索引擎']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {
                show: true,
                type: ['pie', 'funnel']
            },
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    series : [
        {
            name: '访问来源',
            type: 'pie',
            radius : '55%',
            center: ['50%', '60%'],
            selectedMode: 'single',
            data:[
                {value:335, name:'直接访问'},
                {value:310, name:'邮件营销'},
                {value:234, name:'联盟广告'},
                {value:135, name:'视频广告'},
                {value:1548, name:'搜索引擎'}
            ],
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};

pie3.setOption(option);
})();


//饼状大图
var pie3_3 = {};
var pie3_3_option = {};
(function(){
    if(!document.getElementById("pie3_3"))return; 
    pie3_3 = echarts.init(document.getElementById("pie3_3"));
    var db_url_type = {{db_url_type|safe}};
    var db_url_type_name = {{db_url_type_name|safe}};
    var db_url_type_value = {{db_url_type_value|safe}};
    if(db_url_type && db_url_type.length > 1){
        db_url_type[1]['selected'] = true;
    }

    var db_service_type = {{db_service_type|safe}};
    var db_service_type_name = {{db_service_type_name|safe}};
    var db_service_type_value = {{db_service_type_value|safe}};



option = {
    title : {
        text: '数据库实时主数据',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        data: db_url_type_name.update(db_service_type_name)
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {
                show: true,
                type: ['pie', 'funnel']
            },
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    series : [
        {
            name: '数据状态',
            type: 'pie',
            selectedMode: 'single',
            label: {
                normal: {
                    trigger: 'item',
                    formatter: "{b} : {c} ({d}%)"
                }
            },
            radius : '55%',
            center: ['29%', '50%'],
            data: db_url_type,
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }, {
            name:'业务类型',
            type:'pie',
            selectedMode: 'single',
            radius: [0, '30%'],
            center: ['78%', '50%'],
            label: {
                normal: {
                    position: 'inner'
                }
            },
            labelLine: {
                normal: {
                    show: false
                }
            },
            data: db_service_type
        },
        {
            name:'访问来源',
            type:'pie',
            selectedMode: 'single',
            radius: ['40%', '55%'],
            center: ['78%', '50%'],
            data: db_url_type
        }
    ]
};
pie3_3_option = option;
pie3_3.setOption(pie3_3_option);
})();


//大数据量面积图
(function(){
    var obj = document.getElementById("shuju");
    if(!obj)return;
    var shuju = echarts.init(obj);
    
    var base = +new Date(1968, 9, 3);
    var oneDay = 24 * 3600 * 1000;
    var date = [];

    var data = [Math.random() * 300];
    var fdata = [data[0] * -1.00];

    for (var i = 1; i < 100; i++) {
        var now = new Date(base += oneDay);
        date.push([now.getFullYear(), now.getMonth() + 1, now.getDate()].join('/'));
        var datav = Math.round((Math.random() - 0.5) * 20 + data[i - 1]);
        data.push(datav);
        fdata.push(datav * -1.00);
    }

option = {
    tooltip: {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        },
        position: function (pt) {
            return [pt[0], '10%'];
        }
    },
    title: {
        text: '大数据量面积图',
    },
    legend: {
        top: '7%',
        data:['模拟数据','模拟数据2','模拟数据3']
    },
    toolbox: {
        feature: {
            dataZoom: {
                yAxisIndex: 'none'
            },
            restore: {},
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        data: date,
        axisTick: {
            alignWithLabel: true
        }
    },
    yAxis: {
        type: 'value'
    },
    dataZoom: [{
        type: 'inside',
        start: 0,
    }, {
        start: 0,
        handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
        handleSize: '80%',
        handleStyle: {
            color: '#fff',
            shadowBlur: 3,
            shadowColor: 'rgba(0, 0, 0, 0.6)',
            shadowOffsetX: 2,
            shadowOffsetY: 2
        }
    }],
    series: [
        {
            name:'模拟数据',
            type:'bar',
            stack: '总量',
            smooth:true,
            symbol: 'none',
            sampling: 'average',
            itemStyle: {
                normal: {
                    color: 'blue'
                }
            },
            areaStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: 'rgb(255, 158, 68)'
                    }, {
                        offset: 1,
                        color: 'rgb(255, 70, 131)'
                    }])
                }
            },
            data: data
        },
        {
            name:'模拟数据2',
            type:'bar',
            stack: '总量',
            smooth:true,
            symbol: 'none',
            sampling: 'average',
            itemStyle: {
                normal: {
                    color: 'rgb(255, 70, 131)'
                }
            },
            areaStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: 'rgb(255, 158, 68)'
                    }, {
                        offset: 1,
                        color: 'rgb(255, 70, 131)'
                    }])
                }
            },
            data: data
        },
        {
            name:'模拟数据3',
            type:'bar',
            stack: '总量',
            smooth: true,
            symbol: 'none',
            sampling: 'average',
            itemStyle: {
                normal: {
                    color: 'rgb(0, 0, 0)'
                }
            },
            areaStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: 'rgb(255, 158, 68)'
                    }, {
                        offset: 1,
                        color: 'rgb(255, 70, 131)'
                    }])
                }
            },
            data: fdata
        }
    ]
};
    shuju.setOption(option);
})();

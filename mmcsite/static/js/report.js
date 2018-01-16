var file = location.href;
var isEn = false;
if(file.indexOf("/en/") > 0){
    isEn = true;
}

var serverURL;
if(file.indexOf("115.28.32.58") < 0){
	serverURL = "iotpilot.miaomiaoce.com";
}else{
	serverURL = "115.28.32.58";
}

var request = window.sessionStorage.getItem("request");

var expressNumber = window.sessionStorage.getItem("expressNumber"),
    macId = window.sessionStorage.getItem("macId");

var chart;
var warnings = [];//温度异常信息
var newWarning = [];
var isWarning = false;

var highest = window.sessionStorage.getItem("highest_temp"),
    lowest = window.sessionStorage.getItem("lowest_temp");

var points = 0;
var total_temperatures = 0;

var h1,h2,h3,l1,l2;
var h1_total = 0,
    h2_total = 0,
    h3_total = 0,
    l1_total = 0,
    l2_total = 0,
    normal_total = 0,
    _duration = 0;

var alarmAt = null;

//曲线初始参数
var dataT = [];
var rowTime = [];

var chartOptions =
{
    chart:{
        renderTo:'container',
        type:'spline',
        marginLeft:50,
        marginRight:50,
        marginTop:80,
        events: {
           load: function () {
               var label = this.renderer.label('Chart loaded', 100, 120)
               .attr({
                   fill: Highcharts.getOptions().colors[0],
                   padding: 10,
                   r: 5,
                   zIndex: 8
               })
               .css({
                   color: '#FFFFFF'
               })
               .add();
               setTimeout(function () {
                   label.fadeOut();
               }, 1000);
           }
       }
    },
    //版权信息
    credits:{
        enabled:false
    },
    //导出按钮
    exporting:{
        enabled:false
    },
    title:{
        text:isEn?"Temperature[°C]":"温度[°C]",
        style:{
            color:'#1e1e1e',
            fontSize:'20px'
        },
        align:'left'
    },
    xAxis:{
        categories:rowTime,
        gridLineWidth: 1,
        labels: {
            align: 'center',
            style:{
                color:'#919191',
            }
        },
        tickLength:0,
        tickInterval:0,
        lineColor:'#424242',
        lineWidth:1,
    },
    yAxis: {
        title: {text: null},
        labels:{
            style:{
                color:'#6f6f6f',
            },
        },
        lineColor:'#424242',
        lineWidth:1,
        showFirstLabel:false,
        plotLines:[],
    },
    series:[{
        name:' ',
        data:dataT,
        color:'#ff0000',
        zones:[],
    }],
    tooltip: {
        crosshairs:[{
            color:'#999',
            width:1,
            dashStyle:'ShortDot',
        }],
        valueDecimals:1,
        valueSuffix:'℃',
    },
    plotOptions: {
        spline: {
            marker: {
                radius: 4,
                lineColor: '#fff',
                lineWidth: 1,
            }
        },
    },
    legend:{
        enabled:false,
    },
}

$(document).ready(function(){
	getNowFormatDate();
    showChart();
})

/*获取当前日期*/
function getNowFormatDate(){
    var date = new Date(),
    	year = date.getFullYear(),
    	month = date.getMonth() + 1,
    	strDate = date.getDate(),
    	hour = date.getHours(),
    	minute = date.getMinutes(),
    	second = date.getSeconds();

    if (month >= 1 && month <= 9)
    {
        month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9)
    {
        strDate = "0" + strDate;
    }
    if (hour >= 0 && hour <= 9)
    {
        hour = "0" + hour;
    }
    if (minute >= 0 && minute <= 9)
    {
        minute = "0" + minute;
    }
    if (second >= 0 && second <= 9)
    {
        second = "0" + second;
    }
    var currentdate = year + "-" + month + "-" + strDate + " " + hour + ":" + minute + ":" + second;
    $("#created_date").html(currentdate);
}

function showChart()
{
    var Begin = window.sessionStorage.getItem("begin"),
        Finish = window.sessionStorage.getItem("end"),
        lowwarning = window.sessionStorage.getItem("lowwarning"),
        highwarning =  window.sessionStorage.getItem("highwarning");
    lowwarning = Number(lowwarning).toFixed(1);
    highwarning = Number(highwarning).toFixed(1);

	//根据起止时间计算总数据点的个数
    var TM1 = Begin.replace(new RegExp(/(-)/g),"/");
    var TM2 = Finish.replace(new RegExp(/(-)/g),"/");
    var firstTime = new Date(TM1);
	var lastTime = new Date(TM2);
	firstTime = firstTime.getTime();
	lastTime = lastTime.getTime();
	var timeLoading = (lastTime - firstTime)/(5*60*1000);//总数据点个数
	var tickNum = Math.floor(timeLoading/5);//x轴显示个数

//设置曲线颜色
    chartOptions.series[0].zones = [{
            value:lowwarning,
            color:'#0000ff',
            },{
            value:highwarning,
            color:'#000',
        }]
    chartOptions.xAxis.tickInterval = tickNum;

    chart = new Highcharts.Chart(chartOptions);

    getForm(Begin,Finish,macId,highwarning,lowwarning);

    var showMax = Math.ceil(highest + 1),
        showMin = Math.ceil(lowest - 1);

    lowest = parseInt(lowest);
    highest = parseInt(highest);

    if(lowwarning < lowest){
        showMin = parseInt(lowwarning) - 1;
    }
    if(highwarning > highest){
        showMax = parseInt(highwarning) + 1;
    }

    var yAxis = chart.yAxis[0];
    yAxis.options.startOnTick = false;
    yAxis.options.endOnTick = false;
    yAxis.setExtremes(showMin,showMax);

    _duration = new Date(Finish).getTime() - new Date(Begin).getTime();
    var elapsed = formatDuring(_duration);

    h1 = highwarning;
    h2 = parseInt(highwarning) + 5;
    h3 = h2 + 5;
    l1 = lowwarning;
    l2 = parseInt(lowwarning) - 5;

    h2 = h2.toFixed(1);
    h3 = h3.toFixed(1);
    l2 = l2.toFixed(1);

    $("#mac").html(macId);
    $("#courier").html(expressNumber);
    $("#start_time").html(Begin);
    $("#stop_time").html(Finish);
    $("#points").html(points);
    $("#elapsed").html(elapsed);

    $("#h1").html(h1);
    $("#h2").html(h2);
    $("#h3").html(h3);
    $("#l1").html(l1);
    $("#l2").html(l2);
    var normal_zone = isEn?lowwarning + " to " + highwarning:lowwarning + " 至 " + highwarning
    $("#normal").html(normal_zone);

}

//图表展示
function getForm(start,end,mac,high,low)
{

    $.ajax({
        type:"POST",
        contentType:"application/json;charset=utf-8",
        url:"http://" + serverURL + "/iot/temperature/get_compressed/",
        data:JSON.stringify({"start_time":start,"end_time":end,"mac":mac}),
        dataType:"json",
        success: function(messages)
        {
            var temps = messages.temperatures;

            if(!temps)
            {
                return;
            }
            for(var i=0,len=temps.length,temp,time; i<len; i++)
            {
                time = temps[i].tm;
                time = timeToLocal(time);
                temp = temps[i].t;
                temp = parseFloat(temp);//string To float

                total_temperatures += temp;//温度总和
                points += 1;//数据个数

                dataT.push(temp);
                rowTime.push(time);

                /*第一个超温时间点*/
                if(!alarmAt){

                    if(temp < low || temp > high){

                        alarmAt = time;
                    }
                }

                /*获取超温信息*/
                if(temp > h3){

                    h3_total += 1;
                    h2_total += 1;
                    h1_total += 1;

                }else if(temp > h2){

                    h2_total += 1;
                    h1_total += 1;

                }else if(temp > h1){

                    h1_total += 1;

                }else if(temp < l2){

                    l2_total += 1;
                    l1_total += 1;

                }else if(temp < l1){

                    l1_total += 1;

                }else{

                    normal_total += 1;
                }

            }

            chart.series[0].setData(dataT);
            chartOptions.xAxis.categories = rowTime;

            updateWarningLow(low);
            updateWarningHigh(high);

        },
        error:function()
        {
            alert("Chart Data Error");
        },
        complete:function()
        {
            var mkt = getMKT(dataT);

            var average = total_temperatures/points;
            average = average.toFixed(1);

            var h1_time = formatDuring(h1_total*5*60*1000),
                h2_time = formatDuring(h2_total*5*60*1000),
                h3_time = formatDuring(h3_total*5*60*1000),
                l1_time = formatDuring(l1_total*5*60*1000),
                l2_time = formatDuring(l2_total*5*60*1000)
                normal_time = formatDuring(normal_total*5*60*1000);

            lowest = Number(lowest).toFixed(1);
            highest = Number(highest).toFixed(1);

            $("#h1_total").html(h1_time);
            $("#h2_total").html(h2_time);
            $("#h3_total").html(h3_time);
            $("#l1_total").html(l1_time);
            $("#l2_total").html(l2_time);
            $("#normal_total").html(normal_time);

            $("#h1_points").html(h1_total);
            $("#h2_points").html(h2_total);
            $("#h3_points").html(h3_total);
            $("#l1_points").html(l1_total);
            $("#l2_points").html(l2_total);

            $("#highest").html(highest);
            $("#lowest").html(lowest);
            $("#points").html(points);
            $("#average").html(average);
            $("#warning_start").html(alarmAt);
            $("#mkt").html(mkt);

            $("#pdf").css('visibility','visible');
        },
    })
}

function updateWarningLow(newValue)
{
    var series = chart.series[0];
    var yAxis = series.yAxis;
    yAxis.removePlotLine('warning-low');
    yAxis.addPlotLine({
        color:'#0000ff',
        dashStyle:'ShortDot',
        value:newValue,
        width:2,
        zIndex:3,
        label:{
            text:newValue,
            align:'right',
            x:40,
            y:5,
            style:{
                fontSize:'14px',
                color:'#0000ff',
                },
            },
        id:'warning-low',
    });
    chart.redraw();
}

function updateWarningHigh(newValue)
{
    var series = chart.series[0];
    var yAxis = series.yAxis;
    yAxis.removePlotLine('warning-high');
    yAxis.addPlotLine({
        color:'#ff0000',
        dashStyle:'ShortDot',
        value:newValue,
        width:2,
        zIndex:3,
        label:{
            text:newValue,
            align:'right',
            x:40,
            y:5,
            style:{
                fontSize:'14px',
                color:'#ff0000',
                },
            },
        id:'warning-high',
    });
    chart.redraw();
}

/*
value = 初始时间;
second = 初始时间所加的秒数;  */
function getNextSecond(value,second)
{
    var today = value.replace(new RegExp(/(-)/g),"/");
    var d = new Date(today);
    var t = d.getTime();
    t += second*1000;
    d = new Date(t);
    var hh = '0' + d.getHours();
    var mm = '0' + d.getMinutes();
    var ss = '0' + d.getSeconds();
    var M = '0' + (d.getMonth()+1);
    var D = '0' + d.getDate()
    D = d.getFullYear()+'-'+M.substr(M.length-2)+'-'+D.substr(D.length-2)+' '+hh.substr(hh.length-2)+":"+mm.substr(mm.length-2)+":"+ss.substr(ss.length-2);
    return D;
}

function getNextMonth(value)
{
    var today = value.replace(new RegExp(/(-)/g),"/");
    var minute = today.split(" ")[1];
    var t = new Date(today);
    var tm = new Date(t.getFullYear(),t.getMonth(),t.getDate()+30);//30天
    var m = '0' + (tm.getMonth()+1);
    var d = '0' + tm.getDate()
    var date = tm.getFullYear()+'-'+m.substr(m.length-2)+'-'+d.substr(d.length-2)+' '+minute;
    return date;    
}

function timeToLocal(value)
{
	if(value=='')
	{
		return '';
	}
    var x = new Date().getTimezoneOffset();
    value = getNextSecond(value,-x*60);
    return value;
}

function timeToUTC(value){
    
    var x = new Date().getTimezoneOffset();
    value = getNextSecond(value,x*60);
    return value;
}

function formatDuring(mss){

    var days = parseInt(mss / (1000 * 60 * 60 * 24));
    var hours = parseInt((mss % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = parseInt((mss % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = (mss % (1000 * 60)) / 1000;
    var show = days + "D " + hours + "H " + minutes + "M " + seconds + "S";
    return show;
}

function generatePDF() {

    var ua_str = navigator.userAgent.toLowerCase(), 
        ie_Tridents,trident, match_str, ie_aer_rv, browser_chi_Type;

    if("ActiveXObject" in self){
        // ie_aer_rv:  指示IE 的版本.
        // It can be affected by the current document mode of IE.
        ie_aer_rv= (match_str = ua_str.match(/msie ([\d.]+)/)) ?match_str[1] :
              (match_str = ua_str.match(/rv:([\d.]+)/)) ?match_str[1] : 0;

        // ie: Indicate the really version of current IE browser.
        ie_Tridents = {"trident/7.0": 11, "trident/6.0": 10, "trident/5.0": 9, "trident/4.0": 8};
        //匹配 ie8, ie11, edge
        trident = (match_str = ua_str.match(/(trident\/[\d.]+|edge\/[\d.]+)/)) ?match_str[1] : undefined;
        browser_chi_Type = (ie_Tridents[trident] || ie_aer_rv) > 0 ? "ie" : undefined;
    }else{
        
        browser_chi_Type = (match_str = ua_str.match(/edge\/([\d.]+)/)) ? "edge" :
                    //判断firefox 浏览器
                      (match_str = ua_str.match(/firefox\/([\d.]+)/)) ? "firefox" : 
                    //判断chrome 浏览器
                      (match_str = ua_str.match(/chrome\/([\d.]+)/)) ? "chrome" : 
                    //判断opera 浏览器
                      (match_str = ua_str.match(/opera.([\d.]+)/)) ? "opera" : 
                    //判断safari 浏览器
                      (match_str = ua_str.match(/version\/([\d.]+).*safari/)) ? "safari" : undefined;
    }

    if(browser_chi_Type == "edge" || browser_chi_Type == "firefox"){

        $("#chart_canvas_div").css({
            "width":"1000px",
            "height":"600px",
            "margin":"50px auto 0 auto"
        });
        change("highcharts-0","chart_canvas");
        $("#container").css("display","none");
    }

    html2canvas($("#generate"),{

        height: 1680,
        background: "#ffffff",
        allowTaint: true,

        onrendered:function(canvas){
            var contentWidth = canvas.width;
            var contentHeight = canvas.height;

            //一页pdf显示html页面生成的canvas高度;
            var pageHeight = contentWidth / 595.28 * 841.89;
            //未生成pdf的html页面高度
            var leftHeight = contentHeight;
            //页面偏移
            var position = 0;
            //a4纸的尺寸[595.28,841.89]，html页面生成的canvas在pdf中图片的宽高
            var imgWidth = 595.28;
            var imgHeight = 595.28/contentWidth * contentHeight;

            var pageData = canvas.toDataURL('image/jpeg', 1.0);

            var pdf = new jsPDF('', 'pt', 'a4');

            //有两个高度需要区分，一个是html页面的实际高度，和生成pdf的页面高度(841.89)
            //当内容未超过pdf一页显示的范围，无需分页
            if(leftHeight < pageHeight){

                pdf.addImage(pageData, 'JPEG', 0, 0, imgWidth, imgHeight);

            }else{

                while(leftHeight > 0){

                    pdf.addImage(pageData, 'JPEG', 0, position, imgWidth, imgHeight);
                    leftHeight -= pageHeight;
                    position -= 841.89;
                    //避免添加空白页
                    if(leftHeight > 0){

                        pdf.addPage();
                    }
                }
            }

            var download_time = getNowFormatTime();
            var filename = "MMC_" + macId + "_" + expressNumber + "_" + download_time;

            pdf.save(filename + ".pdf");

            $("#container").css("display","block");
            $("#chart_canvas_div").remove();

        },
    })

}

function getNowFormatTime(){
    var date = new Date(),
        year = date.getFullYear(),
        month = date.getMonth() + 1,
        strDate = date.getDate(),
        hour = date.getHours(),
        minute = date.getMinutes(),
        second = date.getSeconds();

    if (month >= 1 && month <= 9)
    {
        month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9)
    {
        strDate = "0" + strDate;
    }
    if (hour >= 0 && hour <= 9)
    {
        hour = "0" + hour;
    }
    if (minute >= 0 && minute <= 9)
    {
        minute = "0" + minute;
    }
    if (second >= 0 && second <= 9)
    {
        second = "0" + second;
    }
    var currentdate = year + "_" + month + "_" + strDate + " " + hour + minute + second;
    return currentdate;
}

function getMKT(temperature_data) {
    var _sum = 0;
    var _total = temperature_data.length + 1;
    var _c = 83.14472/0.008314472;
    for (var i = 0 , _length = temperature_data.length ; i < _length ; i++) {

        var _fahrenheit = temperature_data[i] + 273.15;
        var _intermediate = Math.exp(-83.14472/(0.008314472*_fahrenheit));
        _sum += _intermediate;
    }

    var _MKT = (_c / (-1 * Math.log(_sum/_total))) - 273.15;
    _MKT = _MKT.toFixed(1);
    return _MKT;
}

function change(svg,canvas){
    var svgHtml = document.getElementById(svg).innerHTML.trim();
    var canvasId = document.getElementById(canvas);
    canvg(canvasId,svgHtml);
}

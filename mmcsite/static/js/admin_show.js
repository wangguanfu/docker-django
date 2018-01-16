var isEn = false;
var file = location.href;
if(file.indexOf("/en/") > 0){
	isEn = true;
}

var serverURL;
if(file.indexOf("115.28.32.58") < 0){
	serverURL = "iotpilot.miaomiaoce.com";
}else{
	serverURL = "115.28.32.58";
}

var chart;
var warnings = [];//温度异常信息
var newWarning = [];

//曲线初始参数
var dataT = [];
var rowTime = [];
var chartTitle = isEn?"Temperature Chart":"温度曲线";

var chartOptions =
{
    chart:{
        renderTo:'container',
        type:'spline',
        marginRight:50,
        marginTop:150,
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
        text:chartTitle,
        style:{
            color:'#1e1e1e',
            fontSize:'28px'
        }
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
        color:'#f96969',
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

function splitPage(page,pageSize)
{
	var ptable = document.getElementById(table_id);
	var num = ptable.rows.length;
	//清除tbody
	for(var i=num-1; i>0; i--)
	{
		ptable.deleteRow(i);
	}
	var totalNums = tableDataA.length;//总行数
	var totalPage = Math.ceil(totalNums/pageSize);
	var begin = (page-1)*pageSize;//页起始位置(包括)
	var end = page*pageSize;//页结束位置(不包括)
	end = end>totalNums? totalNums:end;
	//向table中写入数据
	var n = 1;
	for( i=begin;i<end;i++)
	{
		var rowData = tableDataA[i];
		var row = ptable.insertRow(n++);
		row.index = i;
		row.onclick = function(){
			showChart(this);
		};

		var safehighT = rowData.high_temp;
		safehighT = safehighT.toFixed(1);
		var safelowT = rowData.low_temp;
		safelowT = safelowT.toFixed(1);
		rowData["safe_temp"] = safelowT + " - " + safehighT;
		var highestTemp = rowData.highest_temp;
		var lowestTemp = rowData.lowest_temp;
		var status = rowData.status;
		if(status == 1)
		{
			rowData["status_temp"] = isEn?"in transit":"运输途中";
		}
        else if(rowData.highest_temp == -200){
            rowData["status_temp"] = isEn?"No Data":"无数据";
        }
		else if(lowestTemp < safelowT || highestTemp > safehighT)
		{
			rowData["status_temp"] = isEn?"Anomaly":"异常";
		}
		else
		{
			rowData["status_temp"] = isEn?"Normal":"正常";
		}

		rowData["download_temp"] = isEn?"Download":"下载记录";

		for(var j=0,cell,cellData; j<7; j++)
		{
			cell = row.insertCell(j);
			if(j == 0)
			{
				cell.innerHTML = rowData.number;
			}
			else if(j == 1)
			{
				cell.innerHTML = rowData.mac;
			}
			else if(j == 2 || j == 3)
			{
				cellData = j==2? rowData.start_time:(rowData.end_time==''?'':rowData.end_time);
				if(status == 1 && j == 3){
					cellData = rowData.safe_temp;
				}
				//cellData = timeToLocal(cellData);
				cell.innerHTML = cellData;
			}
			else if(j == 4)
			{
				if(status != 1){
					cell.innerHTML = rowData.safe_temp;
				}
			}
			else if(j == 5)
			{
				if(status != 1){
					cellData = rowData.status_temp;
					cell.innerHTML = cellData;
					if(isEn)
					{
						cell.className = cellData == "Normal"?"normal":(cellData == "Anomaly"?"danger":"expressing");
					}
					else
					{
						cell.className = cellData == "正常"?"normal":(cellData == "异常"?"danger":"expressing");
					}
				}
			}
			else
			{
				if(status != 1){
					cell.innerHTML = "<div class='download'>" + rowData.download_temp + "</div>";
					cell.index = i;
					cell.onclick = function(){
						downloadTemperatures(this);
					}
				}
			}
		}
	}

	//生成分页工具条
	var pageBar = page + "/" + totalPage;
	if(page > 1)
	{
		pageBar = "<a href=\"javascript:splitPage(" + (page-1) + "," + pageSize + ");\">&lt </a>" + pageBar;
	}
	else
	{
		pageBar = "&lt " + pageBar;
	}
	if(page < totalPage)
	{
		pageBar += "<a href=\"javascript:splitPage(" + (page+1) + "," + pageSize + ");\"> &gt</a>";
	}
	else
	{
		pageBar += " &gt";
	}
	document.getElementById(table_id+"_bar").innerHTML = pageBar;
}


/*Download*/
function downloadTemperatures(obj)
{
	rowData = tableDataA[obj.index];

	var downloadTimes = [],downloadTemps = [];
	var sTime = rowData.start_time;
	var fileTime = sTime;
	var eTime = rowData.end_time;
	var mmcId = rowData.mac;
	var expNum = rowData.number;
	stopEvent();
	getJsonOfTemperatures(fileTime,sTime,eTime,mmcId,expNum,downloadTimes,downloadTemps);
}

/*阻止冒泡事件*/
function stopEvent()
{
	var e = arguments.callee.caller.arguments[0] || event;
	if (e && e.stopPropagation)
	{
		e.stopPropagation();
	}
	else if(window.event)
	{
		window.event.cancelBubble = true;
	}
}

/*
fileStart = 初始时间
timeStart = 每次取数据的开始时间
timeEnd = 每次取数据的截止时间   */
function getJsonOfTemperatures(fileStart,timeStart,timeEnd,mac,number,downloadTimes,downloadTemps)
{
	var _Error = false;
	var eachEnd = getNextMonth(timeStart);
	var realEnd = eachEnd>timeEnd?timeEnd:eachEnd;
	$.ajax({
        type:"POST",
        contentType:"application/json;charset=utf-8",
        url:"http://" + serverURL + "/iot/temperature/get_compressed/",
        data:JSON.stringify({"start_time":timeStart,"end_time":realEnd,"mac":mac}),
        dataType:"json",
        success: function(messages)
        {
        	if(!messages.temperatures)
        	{
        		return;
        	}
            for(var i=0,leng = messages.temperatures.length;i<leng;i++)
        	{
        		var times = messages.temperatures[i].tm;
            	//times = timeToLocal(times);
            	var temps = messages.temperatures[i].t;
            	temps = parseFloat(temps);

            	downloadTimes.push(times);
            	downloadTemps.push(temps);
        	}
        },
        error:function()
        {
        	_Error = true;
        	return;
        },
        complete:function()
        {
    		if(_Error)
    		{
    			if(isEn)
    			{
    				alert("An error or exception occurred while downloading data.");
    			}
    			else
    			{
    				alert("下载数据出现异常!");
    			}
    			return;
    		}
        	if(eachEnd > timeEnd)
        	{

        		var download_time = getNowFormatTime();
        		
				var filename = "MMC_" + mac + "_" + number + "_" + download_time;
		    	ToExcelConvertor(downloadTimes,downloadTemps, filename, mac,number)
		        return; 
        	}
        	var eachStart = eachEnd;
    		eachStart = getNextSecond(eachStart,1);
			getJsonOfTemperatures(fileStart,eachStart,timeEnd,mac,number,downloadTimes,downloadTemps);
        },
    })
}

/*
dataTimes = 下载的时间数组
dataTemps = 下载的温度数组
FileName = 文件命名
mmcID = 秒秒测ID
expNumber = 快递单号      */
function ToExcelConvertor(dataTimes,dataTemps, FileName, mmcID,expNumber)
{
    var excel = "<table id='toExcel'>";
	//设置表头
    var headRow = "<thead><tr>";
    headRow += "<td>ZenMeasureID:</td><td>" + mmcID + "</td><td>Tracking No.:</td><td>" + expNumber + "</td>";
    headRow += "</tr><tr>";
    headRow += "<td>Date</td><td>Time</td><td>Temperature(°C)</td>";
    headRow += "</tr></thead>";
    excel += headRow + "<tbody>";
	//设置数据
	var valueTemp,valueTime,valueDate,valueHour;
    for (var i = 0,len = dataTimes.length; i < len; i++)
    {
        valueTemp = dataTemps[i];
        valueTime = dataTimes[i];
        valueDate = valueTime.split(" ")[0];
        valueHour = valueTime.split(" ")[1];
        var row = "<tr>";
        row += '<td>' + valueDate + '</td><td>' + valueHour + '</td><td>' + valueTemp + '</td>';
        excel += row + "</tr>";
    }
    excel += "</tbody></table>";
    document.getElementById("displaybox").innerHTML = excel;
	tableExport("toExcel", FileName, "csv");
}
/*End Download*/

function showChart(obj)
{
	rowData = tableDataA[obj.index];
	var _status = rowData.status;
	if(_status == 1)
	{
		if(isEn)
		{
			alert("No record");
		}
		else
		{
			alert("运输途中,暂无温度记录");
		}
	}
	else{
		var expressNumber = rowData.number;
	    var Begin = rowData.start_time;
	    var Finish = rowData.end_time;
	    var lowwarning = rowData.low_temp;
	    var highwarning = rowData.high_temp;

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
		var tickNum = Math.floor(timeLoading/5);//x轴显示个数(5)

	//设置曲线颜色
	    chartOptions.series[0].zones = [{
	            value:lowwarning,
	            color:'#f96969',
	            },{
	            value:highwarning,
	            color:'#3799bf',
	        }]
	    chartOptions.xAxis.tickInterval = tickNum;
	    chart = new Highcharts.Chart(chartOptions);

	    var macId = rowData.mac;

        if(rowData.highest_temp == -200){
                alert("没有温度数据");
                return false;
        }
        else{
            getForm(Begin,Finish,macId,highwarning,lowwarning);
            updateWarningLow(lowwarning);
            updateWarningHigh(highwarning);

            var highest = rowData.highest_temp,
                lowest = rowData.lowest_temp,
                showMax = Math.ceil(highest + 1),
                showMin = Math.ceil(lowest - 1);

            if(lowwarning < lowest){
                showMin = Math.ceil(lowwarning - 1);
            }
            if(highwarning > highest){
                showMax = Math.ceil(highwarning + 1);
            }

            var yAxis = chart.yAxis[0];
            yAxis.options.startOnTick = false;
            yAxis.options.endOnTick = false;
            yAxis.setExtremes(showMin, showMax);

            $(".zhanwei").hide();
            $(".return").show();
            $(obj).siblings().hide();
            $(obj).siblings(".table_head").show();
            $(obj).parents("section").siblings("section").hide();
            $(obj).parents("table").siblings().hide();
            $("#container").show();
        }
	}
}

/*图表展示*/
function getForm(start,end,mac,high,low)
{
	var isError = false;
	var B = getNextMonth(start);
	var realEnd = B>end?end:B;
    $.ajax({
        type:"POST",
        contentType:"application/json;charset=utf-8",
        url:"http://" + serverURL + "/iot/temperature/get_compressed/",
        data:JSON.stringify({"start_time":start,"end_time":realEnd,"mac":mac}),
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
                //time = timeToLocal(time);
                temp = temps[i].t;
                temp = parseFloat(temp);//string To float
                dataT.push(temp);
                rowTime.push(time);
                /*获取超温信息*/
                if(temp < low || temp > high)
                {
                	var lowDif = low - temp;
                	var highDif = temp - high;
                	var tempDif = temp<low?lowDif:highDif;
                	var tempStatus = temp<low?false:true;
                	if(!newWarning.start)
                	{
                		newWarning.start = newWarning.end = time;
                		newWarning.difference = tempDif;
                		newWarning.isHigh = tempStatus;
                	}
                	else
                	{
                		var isNewWarning = false;
                		var nowTime = time.replace(new RegExp(/(-)/g),"/");
                    	var nowEnd = newWarning.end.replace(new RegExp(/(-)/g),"/");
                    	var tx = new Date(nowTime).getTime() - new Date(nowEnd).getTime();
                    	if(tx <= 10*60*1000)
                    	{
                    		if(tempStatus === newWarning.isHigh)
                    		{
	                    		newWarning.end = time;
	                    		newWarning.difference = newWarning.difference>tempDif?newWarning.difference:tempDif;
                    		}
                    		else
                    		{
                    			isNewWarning = true;
                    		}
                    	}
                    	else
                    	{
                    		isNewWarning = true;
                    	}

                    	if(isNewWarning)
                    	{
                    		warnings.push({
	                			'start':newWarning.start,
	                			'end':newWarning.end,
	                			'dif':newWarning.difference,
	                			'is_high':newWarning.isHigh
	                		});
	                		newWarning.start = newWarning.end = time;
	                		newWarning.difference = tempDif;
	                		newWarning.isHigh = tempStatus;
                    	}
                	}
                }
            }
            chart.series[0].setData(dataT);
            chartOptions.xAxis.categories = rowTime;
            chart.redraw();
        },
        error:function()
        {
        	isError = true;
        },
        complete:function()
        {
        	if(isError)
        	{
        		if(isEn)
        		{
        			alert("An error or exception occurred while retrieving data.")
        		}
        		else
        		{
        			alert("获取数据出现异常！");
        		}
        		return;
        	}
        	if(B > end)
        	{
        		warnings.push({
        			'start':newWarning.start,
        			'end':newWarning.end,
        			'dif':newWarning.difference,
        			'is_high':newWarning.isHigh
        		});
        		dataT = [];
				rowTime = [];//数据清空
        		return;
        	}
        	var A = B;
    		A = getNextSecond(A,1);
			getForm(A,end,mac,high,low);
        },
    })
}

function updateWarningLow(newValue)
{
    var series = chart.series[0];
    var yAxis = series.yAxis;
    yAxis.removePlotLine('warning-low');
    yAxis.addPlotLine({
        color:'#f96969',
        dashStyle:'ShortDot',
        value:newValue,
        width:2,
        zIndex:3,
        label:{
            text:newValue,
            align:'right',
            x:30,
            y:5,
            style:{
                fontSize:'12px',
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
        color:'#f96969',
        dashStyle:'ShortDot',
        value:newValue,
        width:2,
        zIndex:3,
        label:{
            text:newValue,
            align:'right',
            x:30,
            y:5,
            style:{
                fontSize:'12px',
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
    var tm = new Date(t.getFullYear(),t.getMonth(),t.getDate()+20);//20天
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

function timeToUTC(value)
{
    var x = new Date().getTimezoneOffset();
    value = getNextSecond(value,x*60);
    return value;
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

function showAll()
{
	window.location.reload();
}





//今日发货
function splitPageB(page,pageSize)
{
	var ptable = document.getElementById(table_id);
	var num = ptable.rows.length;
	//清除tbody
	for(var i=num-1; i>0; i--)
	{
		ptable.deleteRow(i);
	}
	var totalNums = tableDataB.length;//总行数
	var totalPage = Math.ceil(totalNums/pageSize);
	var begin = (page-1)*pageSize;//页起始位置(包括)
	var end = page*pageSize;//页结束位置(不包括)
	end = end>totalNums? totalNums:end;
	//向table中写入数据
	var n = 1;
	for( i=begin;i<end;i++)
	{
		var rowData = tableDataB[i];
		var row = ptable.insertRow(n++);
		row.index = i;
		row.onclick = function(){
			showChartB(this);
		};

		var safehighT = rowData.high_temp;
		safehighT = safehighT.toFixed(1);
		var safelowT = rowData.low_temp;
		safelowT = safelowT.toFixed(1);
		rowData["safe_temp"] = safelowT + " - " + safehighT;
		var highestTemp = rowData.highest_temp;
		var lowestTemp = rowData.lowest_temp;
		var status = rowData.status;
		if(status == 1)
        {
            rowData["status_temp"] = isEn?"in transit":"运输途中";
        }
        else if(rowData.highest_temp == -200){
            rowData["status_temp"] = isEn?"No Data":"无数据";
        }
        else if(lowestTemp < safelowT || highestTemp > safehighT)
        {
            rowData["status_temp"] = isEn?"Anomaly":"异常";
        }
        else
        {
            rowData["status_temp"] = isEn?"Normal":"正常";
        }
        rowData["download_temp"] = isEn?"Download":"下载记录";

		for(var j=0,cell,cellData; j<7; j++)
		{
			cell = row.insertCell(j);
			if(j == 0)
			{
				cell.innerHTML = rowData.number;
			}
			else if(j == 1)
			{
				cell.innerHTML = rowData.mac;
			}
			else if(j == 2 || j == 3)
			{
				cellData = j==2? rowData.start_time:(rowData.end_time==''?'':rowData.end_time);
				cell.innerHTML = cellData;
			}
			else if(j == 4)
			{
				cell.innerHTML = rowData.safe_temp;
			}
			else if(j == 5)
			{
				cellData = rowData.status_temp;
				cell.innerHTML = cellData;
				if(isEn)
				{
					cell.className = cellData == "Normal"?"normal":(cellData == "Anomaly"?"danger":"expressing");
				}
				else
				{
					cell.className = cellData == "正常"?"normal":(cellData == "异常"?"danger":"expressing");
				}
			}
			else
			{
				if(status != 1){
					cell.innerHTML = "<div class='download'>" + rowData.download_temp + "</div>";
					cell.index = i;
					cell.onclick = function(){
						downloadTemperaturesB(this);
					}
				}
			}
		}
	}

	//生成分页工具条
	var pageBar = page + "/" + totalPage;
	if(page > 1)
	{
		pageBar = "<a href=\"javascript:splitPageB(" + (page-1) + "," + pageSize + ");\">&lt </a>" + pageBar;
	}
	else
	{
		pageBar = "&lt " + pageBar;
	}
	if(page < totalPage)
	{
		pageBar += "<a href=\"javascript:splitPageB(" + (page+1) + "," + pageSize + ");\"> &gt</a>";
	}
	else
	{
		pageBar += " &gt";
	}
	document.getElementById(table_id+"_bar").innerHTML = pageBar;
}


/*Download*/
function downloadTemperaturesB(obj)
{
	rowData = tableDataB[obj.index];

	var downloadTimes = [],downloadTemps = [];
	var sTime = rowData.start_time;
	var fileTime = sTime;
	var eTime = rowData.end_time;
	var mmcId = rowData.mac;
	var expNum = rowData.number;
	stopEvent();
	getJsonOfTemperatures(fileTime,sTime,eTime,mmcId,expNum,downloadTimes,downloadTemps);
}

function showChartB(obj)
{
	rowData = tableDataB[obj.index];
    var _status = rowData.status;
	if(_status == 1)
	{
		if(isEn)
		{
			alert("No record");
		}
		else
		{
			alert("运输途中,暂无温度记录");
		}
	}
	else{
		var expressNumber = rowData.number;
	    var Begin = rowData.start_time;
	    var Finish = rowData.end_time;
	    var lowwarning = rowData.low_temp;
	    var highwarning = rowData.high_temp;

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
		var tickNum = Math.floor(timeLoading/5);//x轴显示个数(5)

	//设置曲线颜色
	    chartOptions.series[0].zones = [{
	            value:lowwarning,
	            color:'#f96969',
	            },{
	            value:highwarning,
	            color:'#3799bf',
	        }]
	    chartOptions.xAxis.tickInterval = tickNum;
	    chart = new Highcharts.Chart(chartOptions);

	    var macId = rowData.mac;

        if(rowData.highest_temp == -200){
            alert("没有温度数据");
            return false;
        }
        else{
            getForm(Begin,Finish,macId,highwarning,lowwarning);
            updateWarningLow(lowwarning);
            updateWarningHigh(highwarning);

            var highest = rowData.highest_temp,
                lowest = rowData.lowest_temp,
                showMax = Math.ceil(highest + 1),
                showMin = Math.ceil(lowest - 1);

            if(lowwarning < lowest){
                showMin = Math.ceil(lowwarning - 1);
            }
            if(highwarning > highest){
                showMax = Math.ceil(highwarning + 1);
            }

            var yAxis = chart.yAxis[0];
            yAxis.options.startOnTick = false;
            yAxis.options.endOnTick = false;
            yAxis.setExtremes(showMin, showMax);


            $(".zhanwei").hide();
            $(".return").show();
            $(obj).siblings().hide();
            $(obj).siblings(".table_head").show();
            $(obj).parents("section").siblings("section").hide();
            $(obj).parents("table").siblings().hide();
            $("#container").show();
        }
	}

}






//运输途中
function splitPageC(page,pageSize)
{
	var ptable = document.getElementById(table_id);
	var num = ptable.rows.length;
	//清除tbody
	for(var i=num-1; i>0; i--)
	{
		ptable.deleteRow(i);
	}
	var totalNums = tableDataC.length;//总行数
	var totalPage = Math.ceil(totalNums/pageSize);
	var begin = (page-1)*pageSize;//页起始位置(包括)
	var end = page*pageSize;//页结束位置(不包括)
	end = end>totalNums? totalNums:end;
	//向table中写入数据
	var n = 1;
	for( i=begin;i<end;i++)
	{
		var rowData = tableDataC[i];
		var row = ptable.insertRow(n++);

		var safehighT = rowData.high_temp;
		safehighT = safehighT.toFixed(1);
		var safelowT = rowData.low_temp;
		safelowT = safelowT.toFixed(1);
		rowData["safe_temp"] = safelowT + " - " + safehighT;
		var highestTemp = rowData.highest_temp;
		var lowestTemp = rowData.lowest_temp;
		var status = rowData.status;
		if(status == 1)
		{
			rowData["status_temp"] = "";
		}
		else if(lowestTemp < safelowT || highestTemp > safehighT)
		{
			rowData["status_temp"] = isEn?"Anomaly":"异常";
		}
		else
		{
			rowData["status_temp"] = isEn?"Normal":"正常";
		}

		rowData["download_temp"] = isEn?"Download":"下载记录";

		for(var j=0,cell,cellData; j<7; j++)
		{
			cell = row.insertCell(j);
			if(j == 0)
			{
				cell.innerHTML = rowData.number;
			}
			else if(j == 1)
			{
				cell.innerHTML = rowData.mac;
			}
			else if(j == 2 || j == 3)
			{
				cellData = j==2? rowData.start_time:(rowData.end_time==''?'':rowData.end_time);
				if(status == 1 && j == 3){
					cellData = rowData.safe_temp;
				}
				//cellData = timeToLocal(cellData);
				cell.innerHTML = cellData;
			}
			else if(j == 4)
			{
				if(status != 1){
					cell.innerHTML = rowData.safe_temp;
				}
			}
			else if(j == 5)
			{
				if(status != 1){
					cellData = rowData.status_temp;
					cell.innerHTML = cellData;
					if(isEn)
					{
						cell.className = cellData == "Normal"?"normal":(cellData == "Anomaly"?"danger":"expressing");
					}
					else
					{
						cell.className = cellData == "正常"?"normal":(cellData == "异常"?"danger":"expressing");
					}
				}
			}
			else
			{
				if(status != 1){
					cell.innerHTML = "<div class='download'>" + rowData.download_temp + "</div>";
					cell.index = i;
					cell.onclick = function(){
						downloadTemperaturesC(this);
					}
				}
			}
		}
	}

	//生成分页工具条
	var pageBar = page + "/" + totalPage;
	if(page > 1)
	{
		pageBar = "<a href=\"javascript:splitPageC(" + (page-1) + "," + pageSize + ");\">&lt </a>" + pageBar;
	}
	else
	{
		pageBar = "&lt " + pageBar;
	}
	if(page < totalPage)
	{
		pageBar += "<a href=\"javascript:splitPageC(" + (page+1) + "," + pageSize + ");\"> &gt</a>";
	}
	else
	{
		pageBar += " &gt";
	}
	document.getElementById(table_id+"_bar").innerHTML = pageBar;
}


/*Download*/
function downloadTemperaturesC(obj)
{
	rowData = tableDataC[obj.index];

	var downloadTimes = [],downloadTemps = [];
	var sTime = rowData.start_time;
	var fileTime = sTime;
	var eTime = rowData.end_time;
	var mmcId = rowData.mac;
	var expNum = rowData.number;
	stopEvent();
	getJsonOfTemperatures(fileTime,sTime,eTime,mmcId,expNum,downloadTimes,downloadTemps);
}

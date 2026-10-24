// 自定义函数工具集

// 定义一个检查非空函数
function checkField(fieldName, fieldValue) {  
	if (!fieldValue) {  
		layer.msg(`${fieldName}为必填项！`);  
		return false; // 立即返回false，停止后续检查  
	}  
	return true; // 如果字段值有效，返回true  
}


//根据URL获取当前页面地址,并解析成json
function getUrlParam(){
	let url = location.href;
	// console.log(url);
	//截取参数
	let param = url.substring(url.lastIndexOf("?")+1,url.length);
	let ps = param.split("&");
	//截取参数
	let obj={};
	if(ps && ps.length>0){
		for(let i=0;i<ps.length;i++){
			let psList = ps[i].split("=");
			obj[psList[0].trim()]=psList[1].trim();
		}
	}
	return obj
}

// 标准K线图
function kLineChart(data,titleName){
	const upColor = '#ec0000';
	const upBorderColor = '#8A0000';
	const downColor = '#00da3c';
	const downBorderColor = '#008F28';
	// Each item: open，close，lowest，highest
	const data0 = splitData(data);
	function splitData(rawData) {
	  const categoryData = [];
	  const values = [];
	  for (var i = 0; i < rawData.length; i++) {
	    categoryData.push(rawData[i].splice(0, 1)[0]);
	    values.push(rawData[i]);
	  }
	  return {
	    categoryData: categoryData,
	    values: values
	  };
	}
	function calculateMA(dayCount) {
	  var result = [];
	  for (var i = 0, len = data0.values.length; i < len; i++) {
	    if (i < dayCount) {
	      result.push('-');
	      continue;
	    }
	    var sum = 0;
	    for (var j = 0; j < dayCount; j++) {
	      sum += +data0.values[i - j][1];
	    }
	    result.push(sum / dayCount);
	  }
	  return result;
	}
	option = {
	  title: {
	    text: titleName,
	    left: 0
	  },
	  tooltip: {
	    trigger: 'axis',
	    axisPointer: {
	      type: 'cross'
	    }
	  },
	  legend: {
	    data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30']
	  },
	  grid: {
	    left: '10%',
	    right: '10%',
	    bottom: '15%'
	  },
	  xAxis: {
	    type: 'category',
	    data: data0.categoryData,
	    boundaryGap: false,
	    axisLine: { onZero: false },
	    splitLine: { show: false },
	    min: 'dataMin',
	    max: 'dataMax'
	  },
	  yAxis: {
	    scale: true,
	    splitArea: {
	      show: true
	    }
	  },
	  dataZoom: [
	    {
	      type: 'inside',
	      start: 50,
	      end: 100
	    },
	    {
	      show: true,
	      type: 'slider',
	      top: '90%',
	      start: 50,
	      end: 100
	    }
	  ],
	  series: [
	    {
	      name: '日K',
	      type: 'candlestick',
	      data: data0.values,
	      itemStyle: {
	        color: upColor,
	        color0: downColor,
	        borderColor: upBorderColor,
	        borderColor0: downBorderColor,
			barWidth: '2px', //调整蜡烛柱的宽度
			barMaxWidth: '4px'
	      },
	      markPoint: {
	        label: {
	          formatter: function (param) {
	            return param != null ? Math.round(param.value) + '' : '';
	          }
	        },
	        data: [
	          // {
	          //   name: 'Mark',
	          //   coord: ['2013/5/31', 2300],
	          //   value: 2300,
	          //   itemStyle: {
	          //     color: 'rgb(41,60,85)'
	          //   }
	          // },
	          {
	            name: 'highest value',
	            type: 'max',
	            valueDim: 'highest'
	          },
	          {
	            name: 'lowest value',
	            type: 'min',
	            valueDim: 'lowest'
	          },
	          {
	            name: 'average value on close',
	            type: 'average',
	            valueDim: 'close'
	          }
	        ],
	        tooltip: {
	          formatter: function (param) {
	            return param.name + '<br>' + (param.data.coord || '');
	          }
	        }
	      },
	      markLine: {
	        symbol: ['none', 'none'],
	        data: [
	          [
	            {
	              name: 'from lowest to highest',
	              type: 'min',
	              valueDim: 'lowest',
	              symbol: 'circle',
	              symbolSize: 10,
	              label: {
	                show: false
	              },
	              emphasis: {
	                label: {
	                  show: false
	                }
	              }
	            },
	            {
	              type: 'max',
	              valueDim: 'highest',
	              symbol: 'circle',
	              symbolSize: 10,
	              label: {
	                show: false
	              },
	              emphasis: {
	                label: {
	                  show: false
	                }
	              }
	            }
	          ],
	          {
	            name: 'min line on close',
	            type: 'min',
	            valueDim: 'close'
	          },
	          {
	            name: 'max line on close',
	            type: 'max',
	            valueDim: 'close'
	          }
	        ]
	      }
	    },
	    {
	      name: 'MA5',
	      type: 'line',
	      data: calculateMA(5),
	      smooth: true,
	      lineStyle: {
	        opacity: 0.5
	      }
	    },
	    {
	      name: 'MA10',
	      type: 'line',
	      data: calculateMA(10),
	      smooth: true,
	      lineStyle: {
	        opacity: 0.5
	      }
	    },
	    {
	      name: 'MA20',
	      type: 'line',
	      data: calculateMA(20),
	      smooth: true,
	      lineStyle: {
	        opacity: 0.5
	      }
	    },
	    {
	      name: 'MA30',
	      type: 'line',
	      data: calculateMA(30),
	      smooth: true,
	      lineStyle: {
	        opacity: 0.5
	      }
	    }
	  ]
	};
}

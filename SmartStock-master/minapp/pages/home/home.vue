<template>
	<view class="container">
		<view class="card-menu">
			<!-- 循环渲染四个图标菜单 -->
			<view class="card-icons" v-for="(item, index) in menuList" :key="index" @click="goToDetail(item.url)">
			  <image :src="item.icon" mode="aspectFit"></image>
			  <text>{{ item.text }}</text>
			</view>
		</view>
	</view>
	
    <view class="container">
        <!-- 流式栅格布局 -->
        <uni-row class="demo-uni-row">
            <uni-col :span="12">
				<!-- 使用 v-if 指令，确保在 valueInfo 不为 null 时才渲染相关内容 -->
                <view class="card-left" v-if="valueInfo"> 
                    <view class="value-title">上证指数</view>
                    <view class="value-value1" :style="{ color: valueInfo.sz_color }">{{ valueInfo.sz_zs }}</view>
                    <view class="value-value2" :style="{ color: valueInfo.sz_color }">{{ valueInfo.sz_zdf }}%</view>
                </view>
            </uni-col>
            <uni-col :span="12">
                <view class="card-right" v-if="valueInfo">
                    <view class="value-title">深证成指</view>
                    <view class="value-value1" :style="{ color: valueInfo.sc_color }">{{ valueInfo.sc_zs }}</view>
                    <view class="value-value2" :style="{ color: valueInfo.sc_color }">{{ valueInfo.sc_zdf }}%</view>
                </view>
            </uni-col>
        </uni-row>
    </view>

    <view class="container">
        <!-- 流式栅格布局 -->
        <uni-row class="demo-uni-row">
            <uni-col :span="12">
                <view class="card-left" v-if="valueInfo">
                    <view class="value-title">创业板指</view>
                    <view class="value-value1" :style="{ color: valueInfo.cyb_color }">{{ valueInfo.cyb_zs }}</view>
                    <view class="value-value2" :style="{ color: valueInfo.cyb_color }">{{ valueInfo.cyb_zdf }}%</view>
                </view>
            </uni-col>
            <uni-col :span="12">
                <view class="card-right" v-if="valueInfo">
                    <view class="value-title">恒生指数</view>
                    <view class="value-value1" :style="{ color: valueInfo.hsi_color }">{{ valueInfo.hsi_zs }}</view>
                    <view class="value-value2" :style="{ color: valueInfo.hsi_color }">{{ valueInfo.hsi_zdf }}%</view>
                </view>
            </uni-col>
        </uni-row>
    </view>
	
	
	
	<view class="container">
	  <view class="echartCard">
		  <view class="kLine-title">上证指数</view>
		 <canvas canvas-id="kLineSz" id="kLineSz" class="charts" @touchend="tap"/>
	  </view>
	</view>
	
	<view class="container">
	  <view class="echartCard">
		  <view class="kLine-title">深证成指</view>
		 <canvas canvas-id="kLineSc" id="kLineSc" class="charts" @touchend="tap2"/>
	  </view>
	</view>
	
	<view class="text-container">
		<view class="text-content">
			交易日9:30-15:00数据实时更新
			<view class="sub-text">
				本产品仅作为策略工具，不属于理财产品，本站数据仅供参考，不构成任何投资建议，据此操作风险自担。
			</view>
		</view>
	</view>
	
	
</template>


<script>
// import { ref, onMounted } from 'vue';
import { getValueCard, getKLineSz, getKLineSc } from '@/api/home.js';
import { onLoad, onShow } from '@dcloudio/uni-app';
import uCharts from '@/static/ucharts/u-charts.min.js';
import { drawChartsUtil } from '@/utils/charts/chartsUtil.js'

var uChartsInstances = {}; // 用于存储不同图表实例
var uChartsInstances2 = {};

export default {
    // 响应式数据变量
    data() {
        return {
            valueInfo: null,
            cWidth: 400,
            cHeight: 302,
			uChartsInstances: {},
			uChartsInstances2: {},
			// 定义图标菜单列表
			menuList: [
				{ icon: '/static/images/hangqing.png', text: '行情中心', url: '/pages/market/market' },
				{ icon: '/static/images/celue.png', text: '我的策略', url: '/pages/strategy/strategy' },
				{ icon: '/static/images/jiaoyi.png', text: '交易明细', url: '/pages/trading/trading' },
				{ icon: '/static/images/yuqing.png', text: '舆情分析', url: '/pages/news/news' }
			  ]
        };
    },
    onReady() {
        // 这里的 750 对应 css .charts 的 width
        this.cWidth = uni.upx2px(680);
        // 这里的 500 对应 css .charts 的 height
        this.cHeight = uni.upx2px(350);
        this.getServerData();
		this.getServerData2();
    },
    // 页面加载前执行
    beforeMount() {
        // this.getValue();
    },
	// 页面显示时执行(目的：每次点击tabBar都重载数据)
	onShow() {
		// this.getServerData();
		// this.getServerData2();
		this.getValue();
	},
    methods: {

		// 点击图标菜单跳转到详情页的方法
		goToDetail(url) {
		  uni.navigateTo({
			url: url
		  });
		},
			
        // 异步获取指标卡数据
        async getValue() {
            const res = await getValueCard();
            // console.log(res);
            if (res.status === 0) {
                // 直接更新响应式数据
                this.valueInfo = res.data;
            } else {
                uni.$showMessage(res.msg);
            }
        },
		
        // K线图
        getServerData() {
            // 从服务器获取数据时的延时
            setTimeout(async () => {
                try {
                    // 返回数据 await：待接口返回后才执行下面的渲染
                    const getKLineSzData = await getKLineSz();
                    const KLineSzData = getKLineSzData.data;
					// console.log(KLineSzData)

                    // 初始化两个空数组
                    const categorie = [];
                    const datas = [];

                    // 遍历原始数组
                    KLineSzData.forEach(subarray => {
                        // 第一个元素是日期，添加到 categories
                        categorie.push(subarray[0]);
                        // 其余元素添加到 data
                        datas.push(subarray.slice(1));
                    });
                    // console.log(categorie, datas)

                    let res = {
                        categories: categorie,
                        series: [
                            {
                                name: "上证指数",
                                data: datas
                            }
                        ]
                    };
                    this.uChartsInstances['kLineSz'] = drawChartsUtil('kLineSz', res, this.cWidth, this.cHeight);
                } catch (error) {
                    console.error('获取 K 线数据时出错:', error);
                }
            }, 1000);
        },
        tap(e) {
            if (this.uChartsInstances[e.target.id]) {
                this.uChartsInstances[e.target.id].touchLegend(e);
                this.uChartsInstances[e.target.id].showToolTip(e);
            }
        },
		
		
		// 深成指K线图
		getServerData2() {
		    // 从服务器获取数据时的延时
		    setTimeout(async () => {
		        try {
		            // 返回数据 await：待接口返回后才执行下面的渲染
		            const getKLineScData = await getKLineSc();
		            const KLineScData = getKLineScData.data;
					// console.log(KLineScData)
		
		            // 初始化两个空数组
		            const categorie = [];
		            const datas = [];
		
		            // 遍历原始数组
		            KLineScData.forEach(subarray => {
		                // 第一个元素是日期，添加到 categories
		                categorie.push(subarray[0]);
		                // 其余元素添加到 data
		                datas.push(subarray.slice(1));
		            });
		            // console.log(categorie, datas)
		
		            let res = {
		                categories: categorie,
		                series: [
		                    {
		                        name: "深证成指",
		                        data: datas
		                    }
		                ]
		            };
		            this.uChartsInstances2['kLineSc'] = drawChartsUtil('kLineSc', res, this.cWidth, this.cHeight);
		        } catch (error) {
		            console.error('获取 K 线数据时出错:', error);
		        }
		    }, 1000);
		},
		tap2(e) {
		    if (this.uChartsInstances2[e.target.id]) {
		        this.uChartsInstances2[e.target.id].touchLegend(e);
		        this.uChartsInstances2[e.target.id].showToolTip(e);
		    }
		}
	
    }
};

</script>

<style>
/* 修改 container 类 */
.container {
  height: auto; /* 修改高度为自动 */
  margin-top: 0; /* 去掉顶部外边距 */
  margin-bottom: 0; /* 去掉底部外边距 */
  margin-left: 1px;
  margin-right: 1px;
  box-sizing: border-box;
}

/* 修改 demo-uni-row 类 */
.demo-uni-row {
  padding: 0; /* 去掉内边距 */
  display: block;
}

/* 其他样式保持不变 */
/* 卡片样式 */
.card-left {
  background-color: #fff; /* 背景颜色 */
  margin-top: 10px; /* 外边距 */
  margin-left: 10px;
  padding: 10px; /* 内边距 */
  box-sizing: border-box; /* 确保内边距不会增加卡片宽度 */
  border-radius: 8px; /* 添加圆角，半径为8像素 */
  height: 80px;
}

.card-right {
  background-color: #fff; /* 背景颜色 */
  margin-top: 10px; /* 外边距 */
  margin-left: 10px;
  margin-right: 10px;
  padding: 12px; /* 内边距 */
  box-sizing: border-box; /* 确保内边距不会增加卡片宽度 */
  border-radius: 8px; /* 添加圆角，半径为8像素 */
  height: 80px;
}

/* 指标值名样式 */
.value-title {
  font-size: 12px;
  margin-bottom: 2px;
  font-weight: bold; /* 设置字体加粗 */
  color: #666565;
  text-align: center; /* 内容文本居中 */
}
/* 指标值1 */
.value-value1 {
  font-size: 16px;
  margin-bottom: 2px;
  font-weight: bold; /* 设置字体加粗 */
  /* color: #f01919; */
  text-align: center; /* 内容文本居中 */
}
/* 指标值2 */
.value-value2 {
  font-size: 13px;
  margin-bottom: 2px;
  font-weight: bold; /* 设置字体加粗 */
  /* color: #4e4e4e; */
  text-align: center; /* 内容文本居中 */
}

.card-menu {
  background-color: #fff; /* 背景颜色 */
  height: 60px; /* 修改高度为自动 */
  margin-left: 10px;
  margin-right: 10px;
  margin-top: 10px;
  display: flex;
  justify-content: space-around;
  padding: 20px;
  border-radius: 8px; /* 添加圆角，半径为8像素 */
}

.card-icons {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.card-icons image {
  width: 50px;
  height: 50px;
  margin-bottom: 5px;
}

.card-icons text {
  font-size: 12px;
}


/* Echarts样式：K线图 */
.charts{
/*    width: 680px; */
    height: 250px;
  }
  
.echartCard {
  background-color: #fff; /* 背景颜色 */
  padding: 5px; /* 内边距 */
  box-sizing: border-box; /* 确保内边距不会增加卡片宽度 */
  border-radius: 8px; /* 添加圆角，半径为8像素 */
  height: 250px;
  margin-left: 10px;
  margin-right: 10px;
  margin-top: 10px;
}

.kLine-title{
	font-weight: bold;
	color: #666565;
}

.text-container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center;    /* 垂直居中（如果需要） */
  height: 100%;           /* 根据需要设置高度 */
  padding: 6px;          /* 内边距 */
}

.text-content {
  text-align: center;     /* 文字居中 */
  line-height: 1.5;       /* 行高，根据需要调整 */
  font-size: 5px;
  color: #666565;
}
 
.sub-text {
  margin-top: 3px;       /* 与上方文字的间距 */
  text-align: center;     /* 文字居中 */
  line-height: 1.5;       /* 行高，根据需要调整 */
  white-space: normal;    /* 允许换行 */
  word-wrap: break-word;  /* 长单词换行 */
}
</style>

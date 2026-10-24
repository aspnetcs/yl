<template>
  <view class="con-search">
  	<image class="search-image" src="../../static/images/stock/search.svg" mode=""></image>
  	<input class="search-input" type="text" placeholder="请输入内容">
  </view>
  
  <view class="stock-list">
	<!-- 表头 -->
    <view class="header">
      <view class="header-item">
        <view>股票</view>
      </view>
      <view class="header-item">最新价</view>
      <view class="header-item">涨跌幅</view>
	  <view class="header-item">盈亏</view>
	  <view class="header-item">收益率</view>
    </view>
	
	<!-- 明细 -->
    <view class="stock-item" v-for="(stock, index) in stockList" :key="index" @click="goToDetail(stock)">
		<view class="code-name-container">
			<view class="stock-name">{{stock.name}}</view>
			<view class="stock-code">{{stock.code}}</view>
		  </view>
		  <view class="stock-price">{{stock.zxj}}</view>
		  <view :class="{'stock-change': true, 'positive': stock.zdf > 0, 'negative': stock.zdf < 0, 'zero': stock.zdf === 0}">
			{{stock.zdf}}%
		  </view>
		  <view :class="{'stock-change': true, 'positive': stock.profit > 0, 'negative': stock.profit < 0, 'zero': stock.profit === 0}">
			{{stock.profit}}
		  </view>
		  <view :class="{'stock-change': true, 'positive': stock.profit_rate > 0, 'negative': stock.profit_rate < 0, 'zero': stock.profit_rate === 0}">
			{{stock.profit_rate}}%
		</view>
    </view>
	
	<!-- 合计 -->
	<view class="total-row">
      <view class="total-item">合计</view>
	  <view class="total-item"></view>
	  <view class="total-item"></view>
      <view :class="{'total-item': true, 'positive': total_profit > 0, 'negative': total_profit < 0, 'zero': total_profit === 0}">{{ total_profit }}</view>
      <view :class="{'total-item': true, 'positive': total_profit_rate > 0, 'negative': total_profit_rate < 0, 'zero': total_profit_rate === 0}">{{ total_profit_rate }}%</view>
    </view>	
	
  </view>
  
  <view class="text-container">
  	<view class="text-content">
  		数据更新时间：{{max_update_time}}
  	</view>
  </view>
</template>

<script>
import { getStockList } from '@/api/stock.js';
import { userInfoStore } from '@/stores'

// 获取本地存储库
const userStore = userInfoStore()

export default {
  data() {
    return {
      stockList: [],
	  total_profit: null,
	  total_profit_rate: null,
	  max_update_time: null
    };
  },
  // 页面打开时执行
  onLoad() {
    // this.fetchStockList();
  },
  // 页面显示时执行
  onShow() {
	  // 显示操作，数据更新
      // console.log('Page onShow');
	  this.fetchStockList()
  },
  methods: {
	
	// 点击进入股票详情页
	goToDetail(stock) {
	        uni.navigateTo({
	            url: `/pages/optional/optionalDetail?code=${stock.code}`
	        });
	    },
		
    async fetchStockList() {
      try {
		const userId = userStore.jobNumber
        const res = await getStockList(userId,'');
		console.log(res.data)
        this.stockList = res.data.rows;
		this.total_profit = res.data.total_profit;
		this.total_profit_rate = res.data.total_profit_rate
		this.max_update_time = res.data.max_update_time
      } catch (error) {
        console.error('获取股票数据失败:', error);
      }
    },
	
  }
};
</script>

<style scoped>
.con-search{
	/* width: 100%; */
	height: 90rpx;
	border-radius: 90rpx;
	background-color: #fff;
	margin-left: 10px;
	margin-right: 10px;
	margin-top: 10px;
	padding: 0 24rpx;
	display: flex;
	align-items: center;
}
.search-image{
	width: 36rpx;
	height: 36rpx;
}
.search-input{
	margin-left: 24rpx;
	width: 70%;
	font-size: 28rpx;
	color: #333;
}

.search-input::placeholder {
  color: #C3C3C3;
}

.stock-list {
  background-color: #fff; /* 背景颜色 */
  margin-left: 10px;
  margin-right: 10px;
  margin-top: 10px;
  padding: 5px;
  border-radius: 8px; /* 添加圆角，半径为8像素 */
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 0;
  border-bottom: 1px solid #ccc;
  font-weight: bold;
  color: #888888;
}
.header-item {
  flex: 1;
  text-align: center;
}
.stock-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 0;
  font-size: 14px;
  border-bottom: 1px solid #e7e7e7;
}
.code-name-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}
.stock-code,
.stock-name {
  text-align: center;
}
.stock-price {
  flex: 1;
  text-align: center;
}
.stock-change {
  flex: 1;
  text-align: center;
}
.positive {
  color: red;
}
.negative {
  color: green;
}
.zero {
  color: gray;
}

/* 合计行样式 */
.total-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 3px 0;
  border-top: 2px;
  margin-top: 3px;
  font-weight: bold;
}
.total-item {
  flex: 1;
  text-align: center;
}
.text-container {
  display: flex;
  justify-content: left; /* 水平居中 */
  align-items: center;    /* 垂直居中（如果需要） */
  height: 100%;           /* 根据需要设置高度 */
  margin-top: 5px;
  margin-left: 10px;
}

.text-content {
  text-align: left;     /* 文字居中 */
  line-height: 1.5;       /* 行高，根据需要调整 */
  font-size: 5px;
  color: #666565;
}
</style>
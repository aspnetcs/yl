<template>
    <!-- 搜索区域 -->
    <view class="con-search">
        <image class="search-image" src="../../static/images/stock/search.svg" mode=""></image>
        <input class="search-input" type="text" placeholder="请输入内容" v-model="searchVal">
        <text class="search-button" @tap="search()">搜索</text> <!-- 添加搜索按钮 -->
    </view>
    <view class="container">
        <!-- 卡片列表 -->
        <view class="card" v-for="(item, index) in tradingList" :key="index" @click="goToDetail(item)">
			<view class="title-switch-container">
				<!-- 主标题：股票名称 -->
				<view class="main-title">{{ item.name }}</view>
				<!-- 修改显示逻辑和样式 -->
				<view class="sub-title" v-if="item.is_monitor === 1" :style="{ color: '#ff0000' }">
					监控中
				</view>
			</view>
            <!-- 副标题信息 -->
            <view class="sub-title">
                <view>交易类型：{{ item.trade_type }}</view>
                <view>成交价格：{{ item.cjjg }} </view>
                <view class="title-switch-container">
					<view>成交数量：{{ item.cjsl }}</view>
					<view>{{ item.trade_time }}</view>
				</view>
            </view>
        </view>
    </view>
</template>

<script>
import { getTradingList } from '@/api/stock.js';
import { userInfoStore } from '@/stores'

// 获取本地存储库
const userStore = userInfoStore()

export default {
  data() {
    return {
      // 股票数据列表
      tradingList: [],
	  searchVal: '',
	  isSwitchOn: null
    };
	},
	
	// 页面显示时执行
	onShow() {
		  // 显示操作，数据更新
	    // console.log('Page onShow');
		  this.getData()
	},
	
	
	methods: {
		
		// 点击进入详情页
		goToDetail(item) {
		        uni.navigateTo({
		            url: `/pages/trading/tradingDetail?id=${item.id}`
		        });
		    },
			
		// 搜索
		search() {
			this.getData(this.searchVal)
		},
		
		// 获取数据
		async getData(value = '') {
			try {
				const userId = userStore.jobNumber
				const res = await getTradingList(userId,value,'');
				// console.log(res.data)
				this.tradingList = res.data.rows;
			  }
			  catch (error) {
				console.error('获取数据失败:', error);
			  }
		
		}
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
	width: 80%;
	font-size: 28rpx;
	color: #333;
}
.search-input::placeholder {
  color: #C3C3C3;
}
.search-button{
	color: #00aaff;
}	

.container {
  padding: 20rpx;
}

.card {
  background-color: #fff;
  border-radius: 10rpx;
  box-shadow: 0 0 10rpx rgba(0, 0, 0, 0.1);
  padding: 20rpx;
  margin-bottom: 20rpx;
}

.main-title {
  font-size: 32rpx;
  font-weight: bold;
  margin-bottom: 10rpx;
  color: #222222;
}

.sub-title {
  font-size: 28rpx;
  color: #666;
}

.sub-title view {
  margin-bottom: 5rpx;
}

/* 主标题和开关按钮容器样式 */
.title-switch-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>
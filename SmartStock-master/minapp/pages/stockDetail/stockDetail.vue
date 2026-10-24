<template>
  <view class="container">
    <!-- 股票基本信息 -->
    <view class="stock-info">
      <view class="stock-code-name">
        <text class="stock-code">{{ stock.code }}</text>
        <text class="stock-name">{{ stock.name }}</text>
      </view>
      <view class="stock-price-change">
        <text :style="{ color: getPriceColor(stock.zdf) }" class="stock-latest-price">{{ stock.zxj }}</text>
        <text :style="{ color: getPriceColor(stock.zdf) }" class="stock-change-rate">{{ stock.zdf }}%</text>
      </view>
    </view>

    <!-- 股票其他信息 -->
    <view class="stock-other-info">
      <view class="info-row">
        <view class="info-label">昨收</view>
        <view class="info-value">{{ stock.zs }}</view>
      </view>
      <view class="info-row">
        <view class="info-label">成交量</view>
        <view class="info-value">{{ stock.cjl }}</view>
      </view>
      <view class="info-row">
        <view class="info-label">成交额</view>
        <view class="info-value">{{ stock.cje }}</view>
      </view>
      <view class="info-row">
        <view class="info-label">换手率</view>
        <view class="info-value">{{ stock.hsl }}</view>
      </view>
      <view class="info-row">
        <view class="info-label">市盈率-动态</view>
        <view class="info-value">{{ stock.syl_dt }}</view>
      </view>
      <view class="info-row">
        <view class="info-label">市净率</view>
        <view class="info-value">{{ stock.sjl }}</view>
      </view>
      <view class="info-row">
        <view class="info-label">总市值</view>
        <view class="info-value">{{ stock.zsz }}</view>
      </view>
	  <view class="info-row">
          <view class="info-label">60 日涨跌幅</view>
          <view :style="{ color: getColorFromPercent(stock.zdf_60d) }" class="info-value">{{ stock.zdf_60d }}</view>
      </view>
      <view class="info-row">
          <view class="info-label">年初至今涨跌幅</view>
          <view :style="{ color: getColorFromPercent(stock.zdf_nzj) }" class="info-value">{{ stock.zdf_nzj }}</view>
      </view>
    </view>
  </view>
</template>

<script>
import { getMarketList } from '@/api/stock.js';
import { userInfoStore } from '@/stores'

// 获取本地存储库
const userStore = userInfoStore()


export default {
  data() {
    return {
		pageSize: 10,
		pageNo: 1,
		stock: {},
		code: null
    };
  },
  
  onLoad(options) {
      this.code = options.code;
      // 调用获取股票详情的方法
      this.showStockDetail(this.code);
    },
	
  methods: {
    getPriceColor(changeRate) {
      if (changeRate > 0) {
        return 'red';
      } else if (changeRate < 0) {
        return 'green';
      } else {
        return 'gray';
      }
    },
	
	 getColorFromPercent(percentStr) {
	      const value = parseFloat(percentStr.replace('%', ''));
	      if (value > 0) {
	        return 'red';
	      } else if (value < 0) {
	        return 'green';
	      } else {
	        return 'gray';
	      }
	},
	
	// 获取数据
	async showStockDetail(value) {
		console.log(value);
		try {
			const userId = userStore.jobNumber
			const res = await getMarketList(userId,this.pageNo,this.pageSize,value);
			// console.log(res.data)
			this.stock = res.data.rows[0];
		  }
		  catch (error) {
			  uni.$showMessage('获取股票数据失败:', error)
		  }
	
	},
	
  }
};
</script>

<style scoped>
.container {
  padding: 20rpx;
}

.stock-info {
  background-color: #fff;
  padding: 30rpx;
  border-radius: 10rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
  margin-bottom: 20rpx;
}

.stock-code-name {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10rpx;
}

.stock-code {
  font-size: 28rpx;
  color: #666;
}

.stock-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.stock-price-change {
  display: flex;
  align-items: center;
}

.stock-latest-price {
  font-size: 48rpx;
  font-weight: bold;
  margin-right: 20rpx;
}

.stock-change-rate {
  font-size: 32rpx;
}

.stock-other-info {
  background-color: #fff;
  padding: 30rpx;
  border-radius: 10rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10rpx 0;
  border-bottom: 1px solid #eee;
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 32rpx;
  color: #666;
}

.info-value {
  font-size: 32rpx;
  color: #333;
}
</style>
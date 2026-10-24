<template>
  <view class="container">
    <!-- 自选股票基本信息 -->
    <view class="stock-info">
      <view class="stock-code-name">
        <text class="stock-code">{{ stock.code }}</text>
        <text class="stock-name">{{ stock.name }}</text>
      </view>
      <view class="stock-price-change">
        <text :style="{ color: getPriceColor(stock.zdf) }" class="stock-latest-price">{{ stock.zxj }}</text>
        <text :style="{ color: getPriceColor(stock.zdf) }" class="stock-change-rate">
            {{ stock.zde >= 0 ? '+' : '' }}{{ stock.zde }} ({{ stock.zdf >= 0 ? '+' : '' }}{{ stock.zdf }}%)
        </text>
      </view>
    </view>

    <!-- 股票其他信息 -->
    <view class="stock-other-info">
      <view class="info-row">
        <view class="info-label">是否持仓</view>
        <view class="info-value">{{ stock.is_hold === 1 ? '是' : '否' }}</view>
      </view>
      <view class="info-row">
        <view class="info-label">持仓价</view>
        <view class="info-value">{{ stock.cost_price }}</view>
      </view>
      <view class="info-row">
        <view class="info-label">持仓股数</view>
        <view class="info-value">{{ stock.hold_number }}</view>
      </view>
      <view class="info-row">
        <view class="info-label">成本市值</view>
        <view class="info-value">{{ stock.cost_amt }}</view>
      </view>
      <view class="info-row">
        <view class="info-label">当前市值</view>
        <view class="info-value">{{ stock.now_value }}</view>
      </view>
      <view class="info-row">
        <view class="info-label">持仓盈亏</view>
        <view :style="{ color: getColorFromPercent(stock.profit) }" class="info-value">{{ stock.profit }}</view>
      </view>
      <view class="info-row">
        <view class="info-label">收益率</view>
        <view :style="{ color: getColorFromPercent(stock.cost_amt ? (stock.profit / stock.cost_amt).toFixed(2)  : 0) }" class="info-value">{{ stock.cost_amt ? ((stock.profit / stock.cost_amt).toFixed(2))*100 + '%' : '0%' }}</view>
      </view>
      <view class="info-row">
          <view class="info-label">年初至今涨跌幅</view>
          <view :style="{ color: getColorFromPercent(stock.zdf_nzj) }" class="info-value">{{ stock.zdf_nzj }}%</view>
      </view>
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
	      // const value = parseFloat(percentStr.replace('%', ''));
		  const value = percentStr
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
			const res = await getStockList(userId,value);
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
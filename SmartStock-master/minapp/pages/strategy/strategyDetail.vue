<template>
  <view class="container">
    <view class="card">
      <!-- 股票基本信息 -->
      <view class="section">
        <view class="section-title">基本信息</view>
        <view class="info-item">
          <view class="label">股票编码</view>
          <view class="value">{{ strategy.code }}</view>
        </view>
        <view class="info-item">
          <view class="label">股票名称</view>
          <view class="value">{{ strategy.name }}</view>
        </view>
        <view class="info-item">
          <view class="label">最新价</view>
          <view class="value">{{ strategy.zxj }}</view>
        </view>
      </view>

      <!-- 投资相关信息 -->
      <view class="section">
        <view class="section-title">投资相关信息</view>
        <view class="info-item">
          <view class="label">投资预算</view>
          <view class="value">{{ strategy.total_invest_budget }}</view>
        </view>
        <view class="info-item">
          <view class="label">目标收益率</view>
          <view class="value">{{ strategy.income_rate_target * 100 }}%</view>
        </view>
        <view class="info-item">
          <view class="label">目标收益</view>
          <view class="value">{{ strategy.income_target }}</view>
        </view>
        <view class="info-item">
          <view class="label">已投入</view>
          <view class="value">{{ strategy.total_invested }}</view>
        </view>
      </view>

      <!-- 阈值相关信息 -->
      <view class="section">
        <view class="section-title">阈值相关信息</view>
        <view class="info-item">
          <view class="label">涨跌幅阈值</view>
          <view class="value">{{ strategy.zdf_stg * 100 }}%</view>
        </view>
        <view class="info-item">
          <view class="label">涨跌额阈值</view>
          <view class="value">{{ strategy.zde_stg }}</view>
        </view>
      </view>

      <!-- 买卖点相关信息 -->
      <view class="section">
        <view class="section-title">买卖点相关信息</view>
        <view class="info-item">
          <view class="label">下一买点</view>
          <view class="value">{{ strategy.next_price_buy }}</view>
        </view>
        <view class="info-item">
          <view class="label">建议股数</view>
          <view class="value">{{ strategy.suggest_buy_num }}</view>
        </view>
        <view class="info-item">
          <view class="label">建议金额</view>
          <view class="value">{{ strategy.suggest_buy_amt }}</view>
        </view>
        <view class="info-item">
          <view class="label">下一卖点</view>
          <view class="value">{{ strategy.next_price_sell }}</view>
        </view>
      </view>
	  
	  <!-- 策略实施 -->
	  <view class="section">
	    <view class="section-title">策略实施</view>
	    <view class="info-item">
	      <view class="label">策略名称</view>
	      <view class="value">{{ strategy.strategy_name }}</view>
	    </view>
	  </view>

      <!-- 是否监控 -->
      <view class="section">
        <view class="section-title">监控设置</view>
        <view class="info-item">
          <view class="label">是否监控</view>
          <view class="radio-group">
            <switch :checked="isSwitchOn" @change="switchChange" />
          </view>
        </view>
      </view>

    </view>
  </view>
</template>

<script>
import { getStrategyList, switchStrategy } from '@/api/stock.js';
import { userInfoStore } from '@/stores'

// 获取本地存储库
const userStore = userInfoStore()

export default {
  data() {
    return {
      strategy: {},
	  isSwitchOn: null,
	  strategyId: null
    };
  },
  
  onLoad(options) {
      this.strategyId = options.id;
      // 调用获取策略详情的方法
      this.showStrategyDetail(this.strategyId);
    },
	
  methods: {
    switchChange(e) {
		console.log(e.detail.value);
		try {
			const res = switchStrategy(this.strategyId,e.detail.value);
			uni.$showMessage("修改成功")
		}
		catch (error) {
			// console.error('接口调用失败:', error);
			uni.$showMessage('修改失败:', error)
		}
    },
	
	// 获取数据
	async showStrategyDetail(id) {
		try {
			const userId = userStore.jobNumber
			const res = await getStrategyList(userId,'',id);
			// console.log(res.data)
			const detailData = res.data.rows[0]
			this.strategy = detailData;
			this.isSwitchOn = detailData.is_monitor
		  }
		  catch (error) {
			console.error('获取数据失败:', error);
		  }
	}
	
	
  }
};
</script>

<style scoped>
.container {
  padding: 20rpx;
  background-color: #f5f5f5;
}

.card {
  background-color: #fff;
  border-radius: 10rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
  padding: 20rpx;
}

.section {
  margin-bottom: 20rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
  border-bottom: 1px solid #eee;
  padding-bottom: 10rpx;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 10rpx 0;
}

.label {
  width: 30%;
  font-size: 28rpx;
  color: #666;
}

.value {
  width: 70%;
  font-size: 28rpx;
  color: #333;
}

.radio-group {
  display: flex;
  align-items: center;
}

.radio-group radio {
  margin-right: 20rpx;
}
</style>
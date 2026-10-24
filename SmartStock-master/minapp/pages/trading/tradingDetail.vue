<template>
    <view class="detail-container">
		<view class="card">
			<!-- 标题 -->
			<view class="detail-title">交易详情</view>
			<!-- 详情信息 -->
			<view class="detail-info">
				<view class="info-item">
					<view class="info-label">股票编码</view>
					<view class="info-value">{{ trading.code }}</view>
				</view>
				<view class="info-item">
					<view class="info-label">股票名称</view>
					<view class="info-value">{{ trading.name }}</view>
				</view>
				<view class="info-item">
					<view class="info-label">交易时间</view>
					<view class="info-value">{{ trading.trade_time }}</view>
				</view>
				<view class="info-item">
					<view class="info-label">交易类型</view>
					<view class="info-value">{{ trading.trade_type }}</view>
				</view>
				<view class="info-item">
					<view class="info-label">成交价格</view>
					<view class="info-value">{{ trading.cjjg }}</view>
				</view>
				<view class="info-item">
					<view class="info-label">成交数量</view>
					<view class="info-value">{{ trading.cjsl }}</view>
				</view>
				<view class="info-item">
					<view class="info-label">成交金额</view>
					<view class="info-value">{{ trading.jyje }}</view>
				</view>
				<view class="info-item">
					<view class="info-label">涨跌幅阈值</view>
					<view class="info-value">{{ trading.zdf_tg * 100 }}%</view>
				</view>
				<view class="info-item">
					<view class="info-label">策略名称</view>
					<view class="info-value">{{ trading.strategy_name }}</view>
				</view>
				<view class="info-item">
					<view class="info-label">下一卖点</view>
					<view class="info-value">{{ parseFloat((trading.cjjg * (1 + trading.zdf_tg)).toFixed(2)) }}</view>
				</view>
				<view class="info-item">
					<view class="info-label">是否监控</view>
					<switch :checked="isSwitchOn" @change="switchChange" />
				</view>
			</view>
		</view>
    </view>
</template>

<script>
import { getTradingList, switchTrading } from '@/api/stock.js';
import { userInfoStore } from '@/stores'

// 获取本地存储库
const userStore = userInfoStore()

export default {
    data() {
        return {
            trading: { },
			isSwitchOn: null,
			tradingId: null
        };
    },
    onLoad(options) {
        this.tradingId = options.id;
        // 调用获取策略详情的方法
        this.showTradingDetail(this.tradingId);
      },
    	
    methods: {
      switchChange(e) {
    		console.log(e.detail.value);
    		try {
    			const res = switchTrading(this.tradingId,e.detail.value);
    			uni.$showMessage("修改成功")
    		}
    		catch (error) {
    			// console.error('接口调用失败:', error);
    			uni.$showMessage('修改失败:', error)
    		}
      },
    	
    	// 获取数据
    	async showTradingDetail(id) {
    		try {
    			const userId = userStore.jobNumber
    			const res = await getTradingList(userId,'',id);
    			// console.log(res.data)
    			const detailData = res.data.rows[0]
    			this.trading = detailData;
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
.detail-container {
    padding: 10px;
	background-color: #f5f5f5;
}

.card {
  background-color: #fff;
  border-radius: 10rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
  padding: 20rpx;
}

.detail-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    text-align: center;
	color: #3b3b3b;
}

.detail-info {
    display: flex;
    flex-direction: column;
	color: #424242;
}

.info-item {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
}

.info-label {
    width: 120px;
    font-weight: bold;
}

.info-value {
    flex: 1;
}
</style>
<template>
<view>
	<view class="search_con">
		<view class="search_input">
			<image src="../../static/images/stock/search.svg" mode=""></image>
			<input type="text" placeholder="请输入证券编码或名称" placeholder-class="placeholder" v-model="searchContent">
			<text @tap="search()">搜索</text>
		</view>
		<view class="search_keywords">
			<view class="search_keywords_hd">
				<view class="search_keyword_title">
					搜索历史
				</view>
				<view class="search_keyword_delete" @tap="clearHistory()">
					<image src="../../static/images/stock/delete.svg" mode=""></image>
				</view>
			</view>
			<view class="search_keyword_list">
				<view class="search_keyword_item" v-for="(item,index) in historyList" :key="index" @tap="toShop()">
					{{item.name}}
				</view>
			</view>
		</view>
	</view>
</view>
</template>

<script>
	export default {
		data() {
			return {
				historyList:[
					{
						name:'茅台'
					},
					{
						name:'工商银行'
					},
					{
						name:'中国平安'
					}
				],
				searchContent:''
			};
		},
		methods:{
			backref() {
				uni.navigateBack({
					delta: 1
				})
			},
			// 搜索
			search(){
				uni.navigateTo({
					url:'/pages/stock/stock'
				})
			},
			// 清空历史
			clearHistory(){
				
			},
			// 点击历史记录
			toShop(){
				uni.navigateTo({
					url:'/pages/stock/stock'
				})
			}
		}
	}
</script>

<style lang="scss">
.search_con{
	padding: 0 24rpx;
	.search_input{
		position: relative;
		width: 100%;
		height: 90rpx;
		border-radius: 12rpx;
		margin-top: 6px;
		margin-right: 6px;
		background-color: #F4F4F4;
		display: flex;
		align-items: center;
		padding: 0 24rpx;
		image{
			width: 26rpx;
			height: 26rpx;
		}
		input{
			margin-left: 15rpx;
			width: 70%;
			font-size: 28rpx;
			color: #333;
			&.placeholder{
				color: #C3C3C3;
			}
		}
		text{
			position: absolute;
			right: 35rpx;
			font-size: 26rpx;
			color: #2588FF;
			font-weight: 700;
		}
	}
	.search_keywords{
		margin-top: 24rpx;
		.search_keywords_hd{
			display: flex;
			justify-content: space-between;
			align-items: center;
			.search_keyword_title{
				font-size: 30rpx;
				color: #333;
				font-weight: 700;
			}
			.search_keyword_delete{
				image{
					width: 32rpx;
					height: 32rpx;
				}
			}
		}
		.search_keyword_list{
			display: flex;
			flex-wrap: wrap;
			margin-top: 15rpx;
			.search_keyword_item{
				padding: 0 26rpx;
				height: 50rpx;
				border-radius: 50rpx;
				background-color: #F8F8F8;
				color: #666666;
				font-size: 24rpx;
				display: flex;
				justify-content: center;
				align-items: center;
				margin-right: 24rpx;
			}
		}
	}
}

page {
    background-color: #fff; /* 设置页面根元素背景颜色为白色 */
}
</style>

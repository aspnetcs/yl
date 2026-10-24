<template>
	<view class="information">
		<view class="infor_attr">
			<view class="infor_attr_img">
				<image src="../../static/images/memberCenter/attr.png" mode=""></image>
			</view>
			<view class="infor_add">
				<image src="../../static/images/memberCenter/icon_add.svg" mode=""></image>
			</view>
		</view>
		<view class="infor_content">
			<view class="infor_content_title">
				{{ member.username }}
			</view>
		</view>
		<view class="infor_form">
			<view class="infor_form_item infor_name">
				<view class="infor_form_hd">
					<view class="info_label">
						姓名
					</view>
				</view>
				<view class="infor_form_bd">
					<input type="text" placeholder="姓名" placeholder-class="placeholder" v-model="member.realname">
				</view>
			</view>
			<view class="infor_form_item">
				<view class="infor_form_hd">
					<view class="info_label">
						邮箱
					</view>
				</view>
				<view class="infor_form_bd">
					<input type="text" placeholder="邮箱" placeholder-class="placeholder" v-model="member.email">
				</view>
			</view>
			<view class="infor_form_item">
				<view class="infor_form_hd">
					<view class="info_label">
						邮箱密码
					</view>
				</view>
				<view class="infor_form_bd">
					<input type="text" placeholder="邮箱密码" placeholder-class="placeholder" v-model="member.email_passwd">
				</view>
			</view>
			<view class="infor_form_item">
				<view class="infor_form_hd">
					<view class="info_label">
						描述
					</view>
				</view>
				<view class="infor_form_bd">
					<input type="text" placeholder="描述" placeholder-class="placeholder" v-model="member.remark">
				</view>
			</view>
			<view class="infor_btns">
				<view class="infor_back" @tap="backref()">
					返回
				</view>
				<view class="infor_save">
					<image src="../../static/images/memberCenter/save.svg" mode=""></image>
					保存
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				member:{
					username:'',
					realname:'',
					email:'',
					remark:'',
					email_passwd:''
				}
			};
		},
		methods:{
			backref() {
				uni.navigateBack({
					delta: 1
				})
			},
		}
	}
</script>

<style lang="scss">
	page{
		background: #f4f4f4;
	}
.information{
	padding-top: 80rpx;
	.infor_attr{
		position: relative;
		display: flex;
		justify-content: center;
		align-items: center;
		width: 150rpx;
		height: 150rpx;
		margin-left: 100rpx;
		border-radius: 50%;
		background-color: #FFFFFF;
		.infor_attr_img{
			width: 236rpx;
			height: 236rpx;
			image{
				width: 236rpx;
				height: 236rpx;
				border-radius: 50%;
			}
		}
		.infor_add{
			position: absolute;
			bottom: 10rpx;
			right: 10rpx;
			image{
				width: 30rpx;
				height: 30rpx;
			}
		}
	}
	.infor_content{
		width: 100%;
		height: 150rpx;
		background: url('../../static/image/memberCenter/bk-profil.svg') no-repeat -220rpx -150rpx;
		margin-top: -60rpx;
		padding: 130rpx 50rpx 0;
		.infor_content_title{
			color: #53586E;
			font-size: 40rpx;
		}
	}
	.infor_form{
		background-color: #fff;
		margin-top: -60rpx;
		padding:0 50rpx;
		padding-top: 60rpx;
		height: calc(100vh - 270rpx - 290rpx);
		.infor_form_item{
			padding-top: 30rpx;
			padding-bottom: 24rpx;
			border-bottom: 1rpx solid #ccc;
			.infor_form_hd{
				display: flex;
				justify-content: space-between;
				.info_label{
					color: #868686;
					font-size: 24rpx;
				}
				.info_edit{
					display: flex;
					align-items: center;
					color: #3F4870;
					font-size: 24rpx;
					image{
						width: 20rpx;
						height: 20rpx;
						margin-right: 8rpx;
					}
				}
			}
			&.infor_sex{
				.infor_form_bd{
					padding: 0 20rpx;
					.radio{
						margin-right: 60rpx;
					}
				}
			}
			.infor_form_bd{
				position: relative;
				margin-top: 14rpx;
				input{
					color: #010F07;
					font-size: 24rpx;
					&.placeholder{
						color: #666;
					}
				}
				image{
					position: absolute;
					right: -10rpx;
					top: 50%;
					transform: translateY(-50%);
					width: 160rpx;
					height: 50rpx;
				}
			}
		}
		.infor_btns{
			display: flex;
			justify-content: space-between;
			margin-top: 50rpx;
			.infor_back{
				width: 48%;
				height: 70rpx;
				border-radius: 100rpx;
				border: 1rpx solid #ccc;
				display: flex;
				justify-content: center;
				align-items: center;
				font-size: 28rpx;
				color: #666;
			}
			.infor_save{
				width: 48%;
				height: 70rpx;
				border-radius: 100rpx;
				background-color: #2588FF;
				display: flex;
				justify-content: center;
				align-items: center;
				color: #fff;
				font-size: 28rpx;
				image{
					width: 40rpx;
					height: 40rpx;
					margin-right: 20rpx;
				}
			}
		}
	}
}
</style>
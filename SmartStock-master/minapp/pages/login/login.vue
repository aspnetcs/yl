<template>
	<view class="login">
		<view class="login_title">
			<view class="login_title_first">
				嘿!
			</view>
			<view class="login_title_second">
				赶紧登录吧！
			</view>
			<view class="login_title_content">
				欢迎回来～我们等你好久了!
			</view>
		</view>
		<view class="login_form">
			<view class="login_form_phone">
				<view class="login_form_label">
					账号
				</view>
				<view class="login_form_input">
					<input type="text" placeholder="请输入账号" v-model="username">
				</view>
			</view>
			<view class="login_form_password">
				<view class="login_form_label">
					密码
				</view>
				<view class="login_form_input">
					<input :type="passwordType" placeholder="请输入密码" v-model="password">
				</view>
				<image src="../../static/images/memberCenter/close.svg" mode="" v-show="passwordType == 'password'" @tap="passwordType = 'text'"></image>
				<image src="../../static/images/memberCenter/open.svg" mode="" v-show="passwordType == 'text'" @tap="passwordType = 'password'"></image>
			</view>
		</view>
		
		<view class="login_btn" @click="agreeLogin">
			登录
		</view>
		
		<view class='private'>
		    <checkbox-group @change="changePrivate">
		        <label class="radio">
		            <checkbox class="checkbox" value="agree" />
		        </label>
		    </checkbox-group>
		    <text>已阅读并同意</text>
		    <navigator url="/pages/login/private" class="privateText">《隐私协议》</navigator>
		</view>
	</view>
</template>

<script>
import { ref } from 'vue'
import { userLogin } from '@/api/login.js';
import { userInfoStore } from '@/stores'

const userStore = userInfoStore()

export default {
	data() {
		return {
			passwordType: 'password',
			username: '', 
			password: '',
			privateBool: false,
		}
	},
	methods: {
		changePrivate(e) {
		      this.privateBool = e.detail.value.includes('agree');
		    },
			
		// 前往登录
		async agreeLogin(){
			// 检查账号和密码是否为空
			if (!this.username || !this.password) {
				uni.$showMessage('账号和密码不能为空');
				return;
			}
			
			if (!this.privateBool) {
			        uni.$showMessage('请先同意隐私协议');
			        return;
			      }
						
			try {
				// 调用登录接口并传递账号和密码
				const res = await userLogin({ username: this.username, password: this.password });
				if (res.code === 200) {
					// 本地存储token
					await userStore.setToken(res.data.token)
					
					// 登录成功
					uni.$showMessage('登录成功');

					// 跳转到tabBar首页
					uni.switchTab({
					  url: '/pages/home/home' 
					});
				} else {
					// 登录失败，给出提示
					uni.$showMessage(res.msg || '登录失败');
				}
			} catch (error) {
				// 处理接口调用错误
				console.error('登录接口调用出错:', error);
				uni.$showMessage('登录接口调用出错');
			}
			
		},

	}
}
</script>

<style lang="scss">
page{
	background: #FAFBFF;
}
.login{
	padding: 100rpx 50rpx 80rpx;
	.login_title{
		margin-top: 70rpx;;
		.login_title_first{
			font-size: 60rpx;
			color: #343965;
			font-weight: 700;
		}
		.login_title_second{
			font-size: 60rpx;
			color: #343965;
			font-weight: 700;
			padding-left: 40rpx;
		}
		.login_title_content{
			margin-top: 24rpx;
			font-size: 24rpx;
			color: #343965;
		}
	}
	.login_form{
		margin-top: 98rpx;
		.login_form_phone{
			display: flex;
			align-items: center;
			background-color: #ECF2FF;
			height: 100rpx;
			border-radius: 100rpx;
			padding: 0 40rpx;
			margin-bottom: 30rpx;
		}
		.login_form_password{
			position: relative;
			display: flex;
			align-items: center;
			background-color: #ECF2FF;
			height: 100rpx;
			border-radius: 100rpx;
			padding: 0 40rpx;
			image{
				position: absolute;
				right: 40rpx;
				width: 35rpx;
				height: 35rpx;
			}
		}
		.login_form_label{
			font-size: 28rpx;
			color: #343965;
			width: 120rpx;
		}
		.login_form_input{
			input{
				color: #333;
				font-size: 24rpx;
				width: 400rpx;
				&.placeholder{
					color: #343965;
				}
			}
		}
	}
	.login_btn{
		display: flex;
		justify-content: center;
		align-items: center;
		width: 100%;
		height: 100rpx;
		border-radius: 100rpx;
		background-color: #2588FF;
		color: #fff;
		font-size: 32rpx;
		font-weight: 700;
		margin-top: 120rpx;
		&.disabled-btn {
		    background-color: #cccccc !important;
		    opacity: 0.6;
		    pointer-events: none;
		  }
	}
	.login_tips{
		position: fixed;
		bottom: 40rpx;
		left: 0;
		width: 100%;
		color: #343965;
		font-size: 24rpx;
		text-align: center;
		.privacy-link {
		    color: #2588FF;
		    text-decoration: none; /* 如果有下划线，可以去掉 */
		    margin-left: 8rpx; /* 添加一些间距，使链接和文本不紧贴 */
		    display: inline-block; /* 确保链接不会换行 */
		}
	}
	
	.private {
	    display: flex;
	    align-items: center;
	    margin-top: 40rpx;
		margin-left: 100rpx;
	}
	
	.checkbox {
		color: $uni-primary;
		iconColor: $uni-primary;
	}
	
	.privateText{
		color: $uni-primary;
	}
}
</style>

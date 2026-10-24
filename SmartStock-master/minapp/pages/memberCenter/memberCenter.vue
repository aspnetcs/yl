<template>
    <view class="user">
        <view class="user_hd">
            <view class="user_info">
                <!-- 用户信息，v-if指令判断未登录才显示 -->
                <view class="user_msg" v-if="!loginFlag">
                    <view class="user_msg_attr">
                        <image src="../../static/images/memberCenter/attr.png" mode="aspectFill"></image>
                    </view>
                    <view class="user_msg_title">
                        尊敬的会员
                    </view>
                    <view class="user_msg_login" @tap="toLogin()">
                        去登录
                    </view>
                </view>

                <view class="user_msg" v-if="loginFlag">
                    <view class="user_msg_login" @click="showExit">
                        退出登录
                    </view>

                    <view>
                        <!-- 提示窗示例 -->
                        <uni-popup ref="alertDialogRef" type="dialog">
                            <uni-popup-dialog :type="msgType" cancelText="关闭" confirmText="同意" title="请确认" content="是否退出登录" @confirm="dialogConfirm"
                                @close="dialogClose"></uni-popup-dialog>
                        </uni-popup>
                    </view>

                    <view class="user_msg_attr">
                        <image src="../../static/images/memberCenter/user.png" mode="aspectFill"></image>
                    </view>
                    <view class="user_msg_content">
                        <view class="user_msg_name">
                            {{ realname }}
                        </view>
                        <view class="user_msg_phone">
                            <image src="../../static/images/memberCenter/phone.svg" mode=""></image>
                            <text>{{ email }}</text>
                        </view>
                    </view>
                </view>
                <!-- 用户其他信息 -->
                <view class="user_other" v-if="loginFlag">
                    <view class="user_other_item user_score">
                        <view class="user_other_item_num">
                            {{ user_id }}
                        </view>
                        <view class="user_other_item_name">
                            会员编号
                        </view>
                    </view>
                    <view class="user_ohter_line">

                    </view>
                    <view class="user_other_item user_money">
                        <view class="user_other_item_num">
                            2025-12-31
                        </view>
                        <view class="user_other_item_name">
                            会员到期
                        </view>
                    </view>
                </view>
            </view>
        </view>
        <view class="user_bd">
            <view class="user_functions">
                <view class="user_function" @tap="toInfo()">
                    <view class="user_function_icon">
                        <image src="../../static/images/memberCenter/information.svg" mode=""></image>
                    </view>
                    <view class="user_function_title">
                        个人资料
                    </view>
                    <view class="user_function_more">
                        <uni-icons type="forward" size="16"></uni-icons>
                    </view>
                </view>
            </view>
        </view>
    </view>
</template>

<!-- setup 组合式API -->
<script setup>
import { ref } from 'vue'
import { userInfoStore } from '@/stores'
import { onShow } from '@dcloudio/uni-app'
import { getUserInfo } from '@/api/login.js'

// 获取用户登录信息持久化
const userStore = userInfoStore()
// console.log(userStore.token)

const loginFlag = ref(false)
const realname = ref(null)
const email = ref(null)
const user_id = ref(null)
const msgType  = ref('success')
const messageText = ref('这是一条成功提示')

// 引用 uni-popup 组件
const alertDialogRef = ref(null)

// 页面加载前
onShow(async () => {
    isLogin();
    if (loginFlag.value) {
        await getUserMsg();
    }
})

// 判断是否登录
const isLogin = () => {
    if (userStore.token) {
        loginFlag.value = true;
    } else {
        loginFlag.value = false;
    }
}

// 获取用户信息
const getUserMsg = async () => {
    try {
        const res = await getUserInfo(userStore.jobNumber)
        // console.log(res)
        if (res.code === 200) {
            realname.value = res.data[0].realname
            email.value = res.data[0].email
            user_id.value = res.data[0].user_id
        } else {
            uni.$showMessage? uni.$showMessage(res.msg) : console.error(res.msg);
        }
    } catch (error) {
        console.error('获取用户信息失败:', error);
    }
}

// 跳转至登录页
const toLogin = () => {
    uni.navigateTo({
        url: '/pages/login/login'
    })
}

// 跳转至个人资料页
const toInfo = () => {
    uni.navigateTo({
        url: '/pages/memberCenter/information'
    })
}

// 弹窗确认
const showExit = () => {
    msgType.value = 'warn'
    // 调用 uni-popup 组件的 open 方法
    alertDialogRef.value?.open()
}

// 退出登录
const dialogConfirm = () => {
    // 处理确认事件
	userStore.clearUserInfo()
	uni.$showMessage('已退出登录')
	uni.navigateTo({
	    url: '/pages/login/login'
	})
}

const dialogClose = () => {
    // 处理关闭事件
    console.log('用户点击了关闭')
}

</script>


<style lang="scss">
.user_hd{
	width: 100%;
	height: 640rpx;
	padding: 70rpx 32rpx 0;
	// background: url('../../static/images/memberCenter/bg.png') no-repeat center center;
	background: linear-gradient(to bottom, #0069d9 0%, #0069d9 50%, #FFFFFF 100%);
	background-size: cover;
	
	.user_info{
		.user_msg{
			position: relative;
			display: flex;
			align-items: center;
			margin-top: 26rpx;
			.user_msg_attr{
				width: 124rpx;
				height: 124rpx;
				border-radius: 50%;
				overflow: hidden;
				border: 4rpx solid #fff;
				image{
					width: 100%;
					height: 100%;
				}
			}
			.user_msg_title{
				margin-left: 15rpx;
				font-weight: 500;
				font-size: 36rpx;
				color: #fff;
			}
			.user_msg_login{
				display: flex;
				justify-content: center;
				align-items: center;
				position: absolute;
				right: 0;
				top: 50%;
				transform: translateY(-50%);
				width: 180rpx;
				height: 64rpx;
				border-radius: 64rpx;
				background-color: #fff;
				color: #2588FF;
				font-size: 24rpx;
				font-weight: bolder;
			}
			.user_msg_content{
				margin-left: 15rpx;
				.user_msg_name{
					font-size: 36rpx;
					font-weight: 500;
					color: #fff;
				}
				.user_msg_phone{
					margin-top: 5rpx;
					image{
						width: 22rpx;
						height: 22rpx;
					}
					text{
						color: #fff;
						font-size: 28rpx;
						margin-left: 8rpx;
					}
				}
			}
		}
		.user_other{
			display: flex;
			justify-content: space-around;
			align-items: center;
			margin-top: 40rpx;
			padding: 0 30rpx;
			.user_other_item{
				display: flex;
				flex-direction: column;
				align-items: center;
				.user_other_item_num{
					font-size: 28rpx;
					color: #fff;
					margin-bottom: 10rpx;
				}
				.user_other_item_name{
					font-size: 28rpx;
					color: #fff;
				}
			}
			.user_ohter_line{
				width: 2rpx;
				height: 40rpx;
				background-color: #fff;
			}
		}
	}
}
.user_bd{
	padding: 40rpx 32rpx 180rpx;
	border-radius: 32rpx 32rpx 0 0;
	background-color: #F4F4F4;
	margin-top: -200rpx;
	min-height: calc(100vh - 500rpx);
	.user_banner{
		height: 220rpx;
		image{
			width: 100%;
			height: 100%;
			border-radius: 12rpx;
		}
	}
	.user_functions{
		.user_function{
			position: relative;
			display: flex;
			align-items: center;
			height: 90rpx;
			padding: 0 24rpx;
			border-radius: 12rpx;
			background-color: #fff;
			margin-top: 20rpx;
			.user_function_icon{
				margin-top: 10rpx;
				image{
					width: 42rpx;
					height: 42rpx;
				}
			}
			.user_function_title{
				font-size: 24rpx;
				color: #666;
				margin-left: 15rpx;
			}
			.user_function_more{
				position: absolute;
				right: 24rpx;
			}
		}
	}
}
</style>

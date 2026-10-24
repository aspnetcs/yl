<template>
    <view class="login">
        <view class="box">
            <view class="title">
                <text class="title-text">
                    智投工匠
                </text>
            </view>
            <view class="tip">
                小程序仅供智投工匠授权(特定)人员使用
            </view>
            <button class="btn" type="primary" @click="agreeLogin"
                :disabled="!privateBool">授权登录</button>
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
    </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { registerAndLogin } from '@/services/login.js'
import { userInfoStore } from '@/stores'
// import { onLoad } from '@dcloudio/uni-app'

// const appid = 'wxca13013575c768f2'
// const appSecret = 'e2d88f49eebf6d4928bd147f664da2e9'
// 提示
const userStore = userInfoStore()
const privateBool = ref(false)

const changePrivate = (e) => {
    privateBool.value = e.detail.value.includes('agree');
}

// 授权登录事件
const agreeLogin = async (e) => {
        const res = await wx.login()  // 获取code
        const resgisterRes = await registerAndLogin(res.code)
        if (resgisterRes.code === 200) {
            await userStore.setToken(resgisterRes.data.token)
            // await getListData()
            // uni.$emit('loginSuccess');
			uni.$showMessage('授权成功');
			// 跳转到tabBar首页
			uni.switchTab({
			  url: '/pages/home/home' 
			});
        } else {
			uni.$showMessage(resgisterRes.msg);
        }
}

</script>

<style lang="scss" scoped>
@import "@/uni.scss";

.login {
    margin: 20rpx;

    .box {
        margin-top: 330rpx;
        display: flex;
        flex-direction: column;
        align-items: center;
        // justify-content: center;

        .title {
            display: flex;
            align-items: center;
            justify-content: center;

            .icon-image {
                width: 130rpx;
                height: 130rpx;
            }

            .title-text {
                font-size: 60rpx;
                font-weight: bold;
                margin-left: 20rpx;
            }
        }

        .tip {
            font-size: 32rpx;
            color: #747474;
            margin-top: 40rpx;
        }

        .btn {
            // font-size: 32rpx;
            width: 550rpx;
            height: 100rpx;
            line-height: 100rpx;
            border-radius: 10rpx;
            font-size: 35rpx;
            margin-top: 100rpx;
            background-color: $uni-primary;
        }

        .private {
            display: flex;
            align-items: center;
            margin-top: 40rpx;
        }
		
		.checkbox {
			color: $uni-primary;
			iconColor: $uni-primary;
		}
		
		.privateText{
			color: $uni-primary;
		}
    }
}
</style>
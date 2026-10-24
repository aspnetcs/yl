<template>
	<view class="container">
		
		<view class="intro"></view>

	</view>
</template>

<script setup>
import { ref } from 'vue';
import { userInfoStore } from '@/stores'
import { onLoad, onShow } from '@dcloudio/uni-app'
import { loginCheckReg, getAuth } from '@/api/login.js'

// 定义变量(ref:数据绑定)
const userStore = userInfoStore()
const isLogin = ref(false)

// 判断是否登录状态
onLoad(async () => {
	// console.log(userStore.token);
	if (!userStore.token) {
		isLogin.value = false;
		// 跳转到登录页
		uni.navigateTo({
			url: "/pages/login/login",
			animationType: 'pop-in',
			animationDuration: 200
		});
	} else {
		isLogin.value = true;
		console.log("已登录")
		// 跳转到tabBar首页
		uni.switchTab({
		  url: '/pages/home/home' 
		});
	}
})

</script>

<style>
	.container {
		padding: 20px;
		font-size: 14px;
		line-height: 24px;
	}
</style>

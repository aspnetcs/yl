<template>
  <view class="container">
    <!-- 单选下拉框 -->
	<view class="con-search">
	  <picker :range="dropdownList" :range-key="'label'" :value="selectedIndex" @change="onPickerChange">
		<view class="picker">
		  {{ dropdownList[selectedIndex]? dropdownList[selectedIndex].label : '请选择' }}
		</view>
	  </picker>
	</view>

    <!-- 三个卡片并排 -->
    <view class="card-container">
      <view class="card">
        <text class="card-label">舆情等级</text>
        <!-- 根据舆情等级动态绑定样式 -->
        <text class="card-value" :class="{ 'positive': sentimentLevel === '积极', 'negative': sentimentLevel === '消极' }">{{ sentimentLevel }}</text>
      </view>
      <view class="card">
        <text class="card-label">总记录数</text>
        <text class="card-value">{{ totalRecords }}</text>
      </view>
      <view class="card">
        <text class="card-label">负面率</text>
        <!-- 负面率显示红色 -->
        <text class="card-value negative-rate">{{ negativeRate }}</text>
      </view>
    </view>

    <!-- 正面文章列表 -->
    <view class="article-list">
      <text class="list-title">正面文章列表</text>
      <scroll-view class="article-scroll" scroll-y>
        <view v-for="(article, index) in positive_data" :key="index" @click="openArticle(article.url)">
          <text class="article-ll">{{ article.title }}</text>
        </view>
      </scroll-view>
    </view>

    <!-- 负面文章列表 -->
    <view class="article-list">
      <text class="list-title">负面文章列表</text>
      <scroll-view class="article-scroll" scroll-y>
        <view v-for="(article, index) in negative_data" :key="index" @click="openArticle(article.url)">
          <text class="article-ll">{{ article.title }}</text>
        </view>
      </scroll-view>
    </view>
  </view>
</template>

<script>
import { getNewsList, getDropdownList } from '@/api/stock.js';
import { userInfoStore } from '@/stores'

// 获取本地存储库
const userStore = userInfoStore()

export default {
    data() {
        return {
            dropdownList: [],
            selectedIndex: 0,
            searchVal: '',
            sentimentLevel: '中',
            totalRecords: 100,
            negativeRate: 20,
            positive_data: [],
            negative_data: []
        };
    },
  
    // 页面显示时执行
    async onShow() {
        try {
			// 获取下拉框列表数据
			const dropdownRes = await getDropdownList(userStore.jobNumber);
			console.log(dropdownRes);
			// 直接使用 data.options 作为下拉框列表
			this.dropdownList = dropdownRes.data.options;

			// 显示默认值的详细信息
			if (this.dropdownList.length > 0) {
				await this.getData(this.dropdownList[this.selectedIndex].value);
			}
		} catch (error) {
			console.error('获取下拉框列表数据失败:', error);
		}
},
  
    methods: {
        onPickerChange(e) {
                    this.selectedIndex = e.detail.value;
                    // 获取选中项的 value 并传递给 getData 方法
                    this.getData(this.dropdownList[this.selectedIndex].value);
                },
		openArticle(url) {
			uni.navigateTo({
				url: `/pages/news/webview?url=${encodeURIComponent(url)}`
			});
		},

        // 获取数据
        async getData(value = '') {
            try {
                const userId = userStore.jobNumber
                const res = await getNewsList(userId, value);
                this.positive_data = res.data.positive_data;
                this.negative_data = res.data.negative_data;
                this.sentimentLevel = res.data.sentiment;
                this.totalRecords = res.data.count;
                this.negativeRate = res.data.negative_rate;
            } catch (error) {
                console.error('获取数据失败:', error);
            }
        }
    }
};
</script>

<style scoped>
/* 整体容器样式 */
.container {
  padding: 10px;
  background-color: #f0f0f0; /* 灰色背景 */
}

/* 搜索区域样式 */
.con-search {
  height: 90rpx;
  border-radius: 90rpx;
  background-color: #ffffff;
  margin: 3px 10px;
  padding: 0 24rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 添加阴影 */
}

.picker {
  flex: 1;
  font-size: 28rpx;
  color: #333;
}

/* 卡片容器样式 */
.card-container {
  display: flex;
  justify-content: space-between;
  margin: 10px 0;
}

/* 卡片样式 */
.card {
  flex: 1;
  background-color: #ffffff;
  margin: 0 6px;
  padding: 10px;
  box-sizing: border-box;
  border-radius: 8px;
  height: 80px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 添加阴影 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.card-label {
  font-size: 14px;
  color: #666;
}

.card-value {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-top: 5px;
}

/* 舆情等级积极时的颜色 */
.positive {
  color: red;
}

/* 舆情等级消极时的颜色 */
.negative {
  color: green;
}

/* 负面率的颜色 */
.negative-rate {
  color: red;
}

/* 文章列表样式 */
.article-list {
  margin: 10px 0;
  background-color: #ffffff;
  border-radius: 8px;
  padding: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 添加阴影 */
}

.list-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
}

.article-ll{
  font-size: 10px;
}

.article-scroll {
  height: 200px; /* 固定文章列表高度 */
  overflow-y: auto; /* 超出高度显示滚动条 */
}

.article-scroll view {
  padding: 3px 5px; /* 减少上下内边距 */
  background-color: #f9f9f9;
  border-radius: 5px;
  margin-bottom: 5px; /* 减少底部外边距 */
  transition: background-color 0.3s ease; /* 添加过渡效果 */
}

.article-scroll view:hover {
  background-color: #e9e9e9; /* 鼠标悬停效果 */
}
</style>
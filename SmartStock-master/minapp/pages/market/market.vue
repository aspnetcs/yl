<template>
    <!-- 搜索区域 -->
    <view class="con-search">
        <image class="search-image" src="../../static/images/stock/search.svg" mode=""></image>
        <input class="search-input" type="text" placeholder="请输入内容" v-model="searchVal">
        <text class="search-button" @tap="search()">搜索</text> <!-- 添加搜索按钮 -->
    </view>
  
    <!-- 表格 -->
    <view>
        <view class="container">
            <uni-table ref="table" :loading="loading" stripe type='' emptyText="暂无更多数据">
                <!-- 表头 -->
                <uni-tr>
                    <uni-th width="80" align='center'>股票</uni-th>
                    <uni-th width="80" align='center'>最新价</uni-th>
                    <uni-th width="80" align='center'>涨跌幅</uni-th>
					<!-- <uni-th width="80" align='center'>操作</uni-th> -->
                </uni-tr>
                <!-- 数据 -->
                <uni-tr v-for="(item, index) in tableData" :key="index" @click="goToDetail(item)">
                    <uni-td align="center">
                        <!-- 新增一个view用于垂直布局 -->
                        <view class="stock-info">
                            <view>{{ item.code }} {{ item.name }}</view>
                        </view>
                    </uni-td>
                    <uni-td align="center">
                        <view class="stock-info">{{ item.zxj }}</view>
                    </uni-td>
                    <uni-td align="center">
                        <view :class="{'stock-info': true, 'positive': item.zdf > 0, 'negative': item.zdf < 0, 'zero': item.zdf === 0}">
                            {{ item.zdf }}%
                        </view>
                    </uni-td>
					
					<!-- <uni-td>
						<view class="uni-group">
							<button class="uni-button" size="mini" type="primary">查看</button>
						</view>
					</uni-td> -->
					
                </uni-tr>
            </uni-table>
            <view class="uni-pagination-box"><uni-pagination show-icon :page-size="pageSize" :current="pageNo" :total="total" @change="change" /></view>
        </view>
    </view>
</template>

<script>
import { getMarketList } from '@/api/stock.js';
import { userInfoStore } from '@/stores'

// 获取本地存储库
const userStore = userInfoStore()

export default {
    data() {
        return {
            searchVal: '',
            tableData: [],
            // 每页数据量
            pageSize: 10,
            // 当前页
            pageNo: 1,
            // 数据总量
            total: 0,
            loading: false
        };
    },
    // 页面打开时执行
    onLoad() {
        // this.fetchStockList();
    },
    // 页面显示时执行
    onShow() {
        // 显示操作，数据更新
        // console.log('Page onShow');
        this.getData(1)
    },
    methods: {
        // 点击进入股票详情页
        goToDetail(item) {
            uni.navigateTo({
                url: `/pages/stockDetail/stockDetail?code=${item.code}`
            });
        },
    
        // 分页触发
        change(e) {
            this.getData(e.current)
        },
        // 搜索
        search() {
            this.getData(1, this.searchVal)
        },
        // 获取数据
        async getData(pageNo, value = '') {
            this.loading = true
            this.pageNo = pageNo
            
            try {
                const userId = userStore.jobNumber
                const res = await getMarketList(userId,pageNo,this.pageSize,value);
                // console.log(res.data)
                this.tableData = res.data.rows;
                this.total = res.data.count;
                this.loading = false
            }
            catch (error) {
                console.error('获取股票数据失败:', error);
            }
        }
    }
};
</script>

<style scoped>
.container {
    width: 100%; /* 设置容器宽度为 100% */
    height: auto; /* 修改高度为自动 */
    margin-top: 10px; /* 去掉顶部外边距 */
    margin-left: 0; /* 去掉左边距 */
    margin-right: 0; /* 去掉右边距 */
    box-sizing: border-box;
    padding: 0 10px; /* 添加左右内边距 */
}

.con-search{
    /* width: 100%; */
    height: 90rpx;
    border-radius: 90rpx;
    background-color: #fff;
    margin-left: 10px;
    margin-right: 10px;
    margin-top: 10px;
    padding: 0 24rpx;
    display: flex;
    align-items: center;
}
.search-image{
    width: 36rpx;
    height: 36rpx;
}
.search-input{
    margin-left: 24rpx;
    width: 80%;
    font-size: 28rpx;
    color: #333;
}
.search-input::placeholder {
    color: #C3C3C3;
}
.search-button{
    color: #00aaff;
}

.stock-info {
    flex: 1;
    text-align: center;
    font-size: 12px;
    width: auto; /* 去掉固定宽度 */
}
.positive {
    color: red;
}
.negative {
    color: green;
}
.zero {
    color: gray;
}


</style>
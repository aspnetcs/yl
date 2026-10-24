import { defineStore } from "pinia";
import { ref } from "vue";

// 定义 Store
export const userInfoStore = defineStore(
  "userInfo",
  () => {
    // 用户凭证
    const mobile = ref(null);
    const token = ref(null);
    const jobNumber = ref(null);

    // 保存用户凭证，登录时使用
    const setMobile = (val) => {
      mobile.value = val;
    };
    const setToken = async (val) => {
      token.value = val;
      jobNumber.value = await getString(val);
    };

    // 清理用户信息，退出时使用
    const clearUserInfo = () => {
      mobile.value = null;
      token.value = null;
      jobNumber.value = null;
    };

    const getUserInfo = () => {
      return new Promise((resolve, reject) => {});
    };

    function getString(str) {
		if (str){
			const match = str.match(/#(.+)/);
			return match ? match[1] : "";
		}else{
			console.log("未登录")
		}
    }
    // 记得 return
    return {
      mobile,
      token,
      jobNumber,
      setMobile,
      setToken,
      clearUserInfo,
      getUserInfo,
    };
  },
  // TODO: 持久化
  {
    // persist: true,
    // 小程序端配置
    persist: {
      storage: {
        getItem(key) {
          return uni.getStorageSync(key);
        },
        setItem(key, value) {
          uni.setStorageSync(key, value);
        },
      },
    },
  }
);

/*
封装登录页接口函数
*/

import { http } from "@/utils/request/http";
import baseUrl from "../config";

// 登录接口V2.0
export const userLogin = (data) => {
  return http({
    url: baseUrl + `/api/login/login`,
    method: "POST",
    data: data,
  });
};


// 校验登录状态接口
export const loginCheckReg = (code) => {
  return http({
    url: baseUrl + `/api/member/check_reg`,
    method: "POST",
    data: {
      code,
    },
  });
};

// 登录注册接口
export const registerAndLogin = (code, mobile) => {
  return http({
    url: baseUrl + `/api/member/login`,
    method: "POST",
    data: {
      code,
      mobile,
    },
  });
};

// 权限清单接口
export const getAuth = (mobile) => {
  return http({
    url: baseUrl + `/api/rights/menu?mobile=${mobile}`,
    method: "GET",
  });
};

// 获取手机号接口
export const getMobile = (code) => {
  return http({
    url: baseUrl + `/api/member/get_wechat_phone`,
    method: "GET",
    data: {
      code,
    },
  });
};

// 获取个人信息接口
export const getUserInfo = (user_id) => {
  return http({
    url: baseUrl + `/api/member/list`,
    method: "GET",
    data: {
      user_id,
    },
  });
};


/*
封装主页接口函数
*/
import { http } from "@/utils/request/http";
import baseUrl from "../config";

// 指标卡接口
export const getValueCard = (code) => {
  return http({
    url: baseUrl + `/home/target`,
    method: "GET",
    data: {
		
    },
  });
};

// 上证指数K线图接口
export const getKLineSz = () => {
  return http({
    url: baseUrl + `/home/szZs`,
    method: "GET",
    data: {
		
    },
  });
};

// 深证成指K线图接口
export const getKLineSc = () => {
  return http({
    url: baseUrl + `/home/szCz`,
    method: "GET",
    data: {
		
    },
  });
};
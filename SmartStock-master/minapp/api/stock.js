/*
封装股票接口函数
*/
import { http } from "@/utils/request/http";
import baseUrl from "../config";


// 获取自选股
export const getStockList = (user_id,code) => {
  return http({
    url: baseUrl + `/api/stock/selectedList`,
    method: "GET",
    data: {
      user_id,
	  code
    },
  });
};


// 获取行情中心
export const getMarketList = (userId,pageNo,pageSize,searchVal) => {
  return http({
    url: baseUrl + `/api/stock/marketList`,
    method: "GET",
    data: {
      userId,
	  pageNo,
	  pageSize,
	  searchVal
    },
  });
};


// 获取策略明细
export const getStrategyList = (userId,searchVal,id) => {
  return http({
    url: baseUrl + `/api/stock/strategyList`,
    method: "GET",
    data: {
      userId,
	  searchVal,
	  id
    },
  });
};

// 策略监控修改
export const switchStrategy = (id,is_monitor) => {
  return http({
    url: baseUrl + `/strategy/details/switch`,
    method: "GET",
    data: {
      id,
	  is_monitor
    },
  });
};

// 获取交易明细
export const getTradingList = (userId,searchVal,id) => {
  return http({
    url: baseUrl + `/api/stock/tradingList`,
    method: "GET",
    data: {
      userId,
	  searchVal,
	  id
    },
  });
};

// 交易监控修改
export const switchTrading = (id,is_monitor) => {
  return http({
    url: baseUrl + `/trading/detail/switch`,
    method: "GET",
    data: {
      id,
	  is_monitor
    },
  });
};

// 获取新闻明细
export const getNewsList = (userId,searchVal) => {
  return http({
    url: baseUrl + `/api/stock/newsList`,
    method: "GET",
    data: {
      userId,
	  searchVal
    },
  });
};

// 筛选
export const getDropdownList = (userId) => {
  return http({
    url: baseUrl + `/api/stock/selection`,
    method: "GET",
    data: {
      userId
    },
  });
};
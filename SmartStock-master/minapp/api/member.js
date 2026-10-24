/*
封装个人中心接口函数
*/
import { http } from "@/utils/request/http";
import baseUrl from "../config";


// 获取sys个人信息接口
export const getSysUserInfo = (user_id) => {
  return http({
    url: baseUrl + `/system/user/list`,
    method: "GET",
    data: {
      user_id,
    },
  });
};

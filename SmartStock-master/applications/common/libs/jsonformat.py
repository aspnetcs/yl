# -*- coding: UTF-8 -*-
'''
@Author  ：leven

@Date    ：2024/1/2 16:09 

@mark    : 接口格式处理：按amis接口标准
'''
import json
import decimal
from flask import make_response, Response


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


# 公共接口返回
def r(data, status=0, msg='', errors={}):
    if status == 0 and msg == '':
        msg = '请求成功'
    elif status == 1 and msg == '':
        msg = '请求失败'
    t = {}
    t['status'] = status
    t['msg'] = msg
    t['data'] = data
    if errors:
        # 表单验证
        t['errors'] = errors
        t['status'] = 422
        t['msg'] = '验证错误'
        pass

    jt = json.dumps(t, ensure_ascii=False, cls=DecimalEncoder, default=str)
    response = make_response(jt)
    response.headers['Content-Type'] = 'application/json'

    return response


# 构建json树
def tree_dict(source, parent):
    # 输出列表名
    tree = []
    # 对每项进行循环
    for item in source:
        # 判断上级
        if item['parentid'] == parent:
            # 加上子项
            tree.append(item)
            # 递归
            item['children'] = tree_dict(source, item['label'])
    return tree


def build_tree(items):
    id_map = {item['id']: {'id': item['id'], 'title': item['title'], 'checkArr': item['checkArr'], 'parentId': item['parentId'], 'children': []} for
              item in items}
    roots = []

    for item in items:
        parent_id = item['parentId']
        if parent_id in id_map:
            id_map[parent_id]['children'].append(id_map[item['id']])
        else:
            # 如果parent_id不在id_map中，我们可能想要添加一个占位符或忽略它
            # 这里我们选择忽略它，因为它可能是一个外部引用或错误
            pass
        if item['parentId'] == 0:
            roots.append(id_map[item['id']])

    # tree_json = json.dumps(roots, indent=4)

    return roots

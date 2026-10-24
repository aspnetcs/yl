import copy
from collections import OrderedDict
from flask import jsonify, Blueprint, request
from applications.models import MemberUser
from applications.schemas import PowerOutSchema

route_rights = Blueprint('rights', __name__, url_prefix='/rights')


# 菜单
@route_rights.get('/menu')
def menu():
    # 获取到用户信息
    mobile = request.values.get('mobile')

    member_info = MemberUser.query.filter_by(mobile=mobile).first()

    if member_info is None:
        result = {"code": 400, "msg": "查无此用户"}
        return jsonify(result)

    try:
        roles = member_info.role
        powers = []
        for i in roles:
            # print(i)
            # 如果角色没有被启用就直接跳过
            if i.enable == 0:
                continue
            # 变量角色用户的权限
            for p in i.power:
                # 如果权限关闭了就直接跳过
                if p.enable == 0:
                    continue
                # 一二级菜单
                if int(p.type) in [0, 1] and p not in powers:
                    powers.append(p)

        power_schema = PowerOutSchema(many=True)  # 用已继承 ma.ModelSchema 类的自定制类生成序列化类
        power_dict = power_schema.dump(powers)  # 生成可序列化对象
        # print(power_dict)

        if not power_dict:
            result = {"code": 300, "msg": "该用户无角色权限"}
            return jsonify(result)

        power_dict.sort(key=lambda x: (x['parent_id'], x['id']), reverse=True)

        menu_dict = OrderedDict()
        for _dict in power_dict:
            if _dict['id'] in menu_dict:
                # 当前节点添加子节点
                _dict['children'] = copy.deepcopy(menu_dict[_dict['id']])
                _dict['children'].sort(key=lambda item: item['sort'])
                # 删除子节点
                del menu_dict[_dict['id']]

            if _dict['parent_id'] not in menu_dict:

                menu_dict[_dict['parent_id']] = [_dict]
            else:
                menu_dict[_dict['parent_id']].append(_dict)

        result = {"code": 200, "msg": "获取成功", "data": sorted(menu_dict.get(0), key=lambda item: item['sort'])}

        return jsonify(result)

    except Exception as e:
        result = {"code": 500, "msg": "获取失败", "data": str(e)}
        return jsonify(result)

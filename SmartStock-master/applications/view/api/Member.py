from flask import Blueprint, request, jsonify, g, json
from applications.common.libs.Helper import getCurrentDate
from applications.common.libs.member.MemberService import MemberService
from applications.models.member.MemberUser import MemberUser
from applications.models.member.Oauth_member_bind import OauthMemberBind
from applications.models.system.admin_user import User
from applications.extensions import db

route_api_member = Blueprint('member', __name__, url_prefix='/member')


@route_api_member.route('/login', methods=['POST'])
def member_login():
    """
    # 注册用户
    :return:
    """
    reqs = {'code': 200, 'msg': '登录成功', 'data': {}}

    # 获取到用户信息
    data = request.get_data()
    req = json.loads(data)
    # print(req)

    code = req['code'] if 'code' in req else ''
    # print("code:" + code)
    if not code or len(code) < 1:
        reqs['code'] = 500
        reqs['msg'] = '需要code'
        return jsonify(reqs)

    # 生成openid，生成openid需要code，code从req里拿
    openid = MemberService.getWeChatOpenid(code)
    # print("openid:" + openid)
    if openid is None:
        reqs['code'] = -1
        reqs['msg'] = '需要openid'
        return jsonify(reqs)

    nickname = req['nickName'] if 'nickName' in req else '微信用户'
    sex = req['gender'] if 'gender' in req else 0
    avatar = req[
        'avatarUrl'] if 'avatarUrl' in req else 'https://thirdwx.qlogo.cn/mmopen/vi_32/POgEwh4mIHO4nibH0KlMECNjjGxQUq24ZEaGT4poC6icRiccVGKSyXwibcPq4BWmiaIGuG1icwxaQX6grC9VemZoJ8rg/132'
    mobile = req['mobile'] if 'mobile' in req else ''
    reg_ip = req['reg_ip'] if 'reg_ip' in req else ''

    # # 校验是否公司用户
    # member_info = MemberUser.query.filter_by(mobile=mobile, status=1).first()
    #
    # if not member_info:
    #     reqs['code'] = -1
    #     reqs['msg'] = '非授权用户，禁止访问'
    #     return jsonify(reqs)

    """
    判断是否已经测试过，注册了直接返回一些信息
    """
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()

    # 注册
    if not bind_info:
        # 把数据写进Member表
        member_info = MemberUser()

        member_info.nickname = nickname
        member_info.sex = sex
        member_info.avatar = avatar
        member_info.reg_ip = reg_ip
        # salt用方法自动生成
        member_info.salt = MemberService.geneSalt()
        db.session.add(member_info)
        db.session.commit()

        # 把数据写进OauthMemberBind表
        model_bind = OauthMemberBind()
        model_bind.member_id = member_info.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = ''
        model_bind.updated_time = model_bind.created_time = getCurrentDate()
        db.session.add(model_bind)
        db.session.commit()

        bind_info = model_bind

    member_info = MemberUser.query.filter_by(id=bind_info.member_id).first()

    # token是Cookie
    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)

    reqs['data'] = {"token": token}
    return jsonify(reqs)


@route_api_member.route('/check_reg', methods=['POST'])
def member_check_reg():
    """
    # 判断是否是注册过的用户
    :return:
    """
    reqs = {'code': 200, 'msg': '登录成功', 'data': {}}

    # 获取用户信息
    data = request.get_data()
    req = json.loads(data)
    # print(req)

    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        reqs['code'] = 500
        reqs['msg'] = '需要code'
        return jsonify(reqs)

    # 获取openid
    openid = MemberService.getWeChatOpenid(code)
    if openid is None:
        reqs['code'] = -1
        reqs['msg'] = '需要openid'
        return jsonify(reqs)

    # 根据openid校验是否绑定
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        reqs['code'] = -1
        reqs['msg'] = '未绑定'
        return jsonify(reqs)

    # 校验是否公司用户
    member_info = MemberUser.query.filter_by(id=bind_info.member_id, status=1).first()

    if not member_info:
        reqs['code'] = -1
        reqs['msg'] = '非公司内部用户，禁止访问'
        return jsonify(reqs)

    # token是Cookie
    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)

    reqs['data'] = {"token": token}
    return jsonify(reqs)


@route_api_member.route('/get_wechat_phone', methods=['GET'])
def get_wechat_phone():
    """
    # 获取微信手机号
    :return:
    """
    reqs = {'code': 200, 'msg': '获取成功', 'data': {}}

    code = request.values.get('code')

    if not code or len(code) < 1:
        reqs['code'] = 500
        reqs['msg'] = '需要code'
        return jsonify(reqs)

    get_data = MemberService.getWeChatPhoneNumber(code)

    if get_data["phone"]:
        reqs['data'] = {"phone": get_data["phone"]}
    else:
        reqs['code'] = 300
        reqs['msg'] = get_data["msg"]
        reqs['data'] = {"phone": get_data["phone"]}

    return jsonify(reqs)


@route_api_member.route('/list', methods=['GET'])
def member_list():
    """
    # 获取用户信息
    :return:
    """
    reqs = {'code': 200, 'msg': '获取成功', 'data': {}}

    user_id = request.values.get('user_id')

    try:
        tc = db.session.query(User).filter_by(id=user_id).all()
        temp = []
        for t in tc:
            temp.append({
                'user_id': t.id,
                'username': t.username,
                'realname': t.realname,
                'avatar': t.avatar,
                'email': t.email
            })
    except Exception as e:
        return jsonify({'code': 500, 'msg': '获取失败', 'data': str(e)})

    reqs["data"] = temp
    return jsonify(reqs)

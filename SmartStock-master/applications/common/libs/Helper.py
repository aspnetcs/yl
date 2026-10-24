from flask import g, render_template
import datetime
import json

'''
自定义分页类
'''


def iPagination(params):
    import math

    ret = {
        "is_prev": 1,
        "is_next": 1,
        "from": 0,
        "end": 0,
        "current": 0,
        "total_pages": 0,
        "page_size": 0,
        "total": 0,
        "url": params['url'].replace("&p=", "")
    }

    total = int(params['total'])
    page_size = int(params['page_size'])
    page = int(params['page'])
    display = int(params['display'])
    total_pages = int(math.ceil(total / page_size))
    total_pages = total_pages if total_pages > 0 else 1
    if page <= 1:
        ret['is_prev'] = 0

    if page >= total_pages:
        ret['is_next'] = 0

    semi = int(math.ceil(display / 2))

    if page - semi > 0:
        ret['from'] = page - semi
    else:
        ret['from'] = 1

    if page + semi <= total_pages:
        ret['end'] = page + semi
    else:
        ret['end'] = total_pages

    ret['current'] = page
    ret['total_pages'] = total_pages
    ret['page_size'] = page_size
    ret['total'] = total
    ret['range'] = range(ret['from'], ret['end'] + 1)
    return ret


"""
统一渲染方法
"""


def ops_render(template, context={}):
    if 'current_user' in g:
        context['current_user'] = g.current_user
    return render_template(template, **context)


"""
获取当前时间
"""


def getCurrentDate(format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(format)
    # return datetime.datetime.now()


'''
根据某个字段获取一个dic出来
'''


def getDictFilterField(db_model, select_filed, key_field, id_list):
    ret = {}
    query = db_model.query
    if id_list and len(id_list) > 0:
        query = query.filter(select_filed.in_(id_list))

    list = query.all()
    if not list:
        return ret

    for item in list:
        if not hasattr(item, key_field):
            break

        ret[getattr(item, key_field)] = item
    return ret


"""
从对象取出某字段
"""


def selectFilterObj(obj, field):
    ret = []
    for item in obj:
        if not hasattr(item, field):
            continue
        if getattr(item, field) in ret:
            continue

        ret.append(getattr(item, field))
    return ret


def getDictListFilterField(db_model, select_filed, key_field, id_list):
    ret = {}
    query = db_model.query
    if id_list and len(id_list) > 0:
        query = query.filter(select_filed.in_(id_list))

    list = query.all()
    if not list:
        return ret
    for item in list:
        if not hasattr(item, key_field):
            break
        if getattr(item, key_field) not in ret:
            ret[getattr(item, key_field)] = []

        ret[getattr(item, key_field)].append(item)
    return ret


'''
获取格式化的时间
'''


def getFormatDate(date=None, format="%Y-%m-%d %H:%M:%S"):
    if date is None:
        date = datetime.datetime.now()

    return date.strftime(format)


# 拼接商品信息
def format_goods(goods_list):
    return ';'.join(f"{item['name']}*{item['quantity']}" for item in goods_list)


def aggregate_orders(orders):
    aggregated = {}
    for order in orders:
        order_id = order['id']
        if order_id not in aggregated:
            # 如果这是第一个具有此ID的订单，则直接添加并格式化goodss
            aggregated[order_id] = order.copy()
            aggregated[order_id]['goodss'] = format_goods(aggregated[order_id]['goodss'])
        else:
            # 如果已经有一个具有此ID的订单，则检查是否需要合并（在这个例子中，我们假设它们总是相同的）
            # 在实际情况中，您可能需要实现更复杂的合并逻辑
            # 但由于您的示例数据是相同的，我们在这里不做任何额外的合并
            pass  # 实际上，由于数据重复，这个else分支在您的示例中不会被执行

    # 将聚合后的字典转换回列表
    return list(aggregated.values())


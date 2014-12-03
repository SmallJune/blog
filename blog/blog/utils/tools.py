# coding=utf-8
import urllib
import hashlib
from itertools import chain
import time

# decode url
import datetime


def validate_kwargs_to_object(obj, **kwargs):
    keys = []
    for k in obj._meta.fields:
        keys.append(k.name)
    for i in kwargs.keys():
        if not i in keys:
            return False
    return True


def validate_dict_to_object(obj, parse_dict):
    keys = []
    for k in obj._meta.fields:
        keys.append(k.name)
    for i in parse_dict.keys():
        if not i in keys:
            return False
    return True


def urldecode(query):
    d = {}
    a = query.split('&')
    for s in a:
        if s.find('='):
            k, v = map(urllib.unquote, s.split('='))
            try:
                d[k].append(v)
            except KeyError:
                d[k] = [v]
    return d


# 判断是否是数字
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata

        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


# 迭代器，大数据不使用查询缓存
def my_iterator(queryset):
    the_iterator = queryset.iterator()

    try:
        first_result = next(the_iterator)
    except StopIteration:
        # No rows were found, so do nothing.
        return []
    else:
        return chain([first_result], the_iterator)


def log(content="debug", path='/tmp/test.log', ):
    # logging.basicConfig(level=logging.DEBUG,
    # format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    #                     datefmt='%a, %d %b %Y %H:%M:%S',
    #                     filename=path,
    #                     filemode='w')
    # logging.info(content)
    fsock = open(path, 'a')
    now = time.strftime("%Y-%m-%d %H %M %S", time.localtime())
    result = '%s--%s\n' % (now, content)
    fsock.write(result)
    fsock.close()
    return result


# 随即字符串
def rand_str(**kwargs):
    str_key = str(time.time())
    for key in kwargs:
        str_key = str_key + '_' + str(kwargs[key])
    return hashlib.md5(str_key).hexdigest()


from django.db import models


def shift_paths(exclude, name):
    return tuple(item.split('.', 1)[1] for item in exclude
                 if item.startswith(('{0}.'.format(name), '*.')))


# 深度遍歷模型
def deep_dump_instance(instance,
                       depth=1,
                       exclude=(),
                       include=(),
                       order_by=(),
                       seen=None):
    if not seen:
        seen = set()
    if (instance.__class__, instance.pk) in seen:
        return '<recursive>'
    seen.add((instance.__class__, instance.pk))
    field_names = sorted(
        [field.name for field in instance._meta.fields] +
        [f.get_accessor_name() for f in instance._meta.get_all_related_objects()])

    dump = []
    exclude_all = '*' in exclude
    for name in field_names:
        if name in include or (not exclude_all and name not in exclude):
            try:
                value = getattr(instance, name)
            except models.ObjectDoesNotExist:
                value = None
            if value.__class__.__name__ == 'RelatedManager':
                if depth >= 1:
                    related_objects = value.all()
                    for ordering in order_by:
                        parts = ordering.split('.')
                        if len(parts) == 2 and parts[0] == name:
                            related_objects = related_objects.order_by(parts[1])
                    value = [deep_dump_instance(related,
                                                depth=depth - 1,
                                                exclude=shift_paths(exclude, name),
                                                include=shift_paths(include, name),
                                                order_by=shift_paths(order_by, name),
                                                seen=seen)
                             for related in related_objects]
                else:
                    continue
            elif isinstance(value, models.Model):
                if depth >= 1:
                    value = deep_dump_instance(value,
                                               depth=depth - 1,
                                               exclude=shift_paths(exclude, name),
                                               include=shift_paths(include, name),
                                               order_by=shift_paths(order_by, name),
                                               seen=seen)
                else:
                    continue
            dump.append((name, value))
    return dump


# 2.0 返回django models對象或對象集的列表
def dump_models_simple(instance):
    result = []
    if instance:
        for i in instance:
            result.append(dump_single_model(i))
    return result


# 返回單個model的dict對象
def dump_single_model(instance):
    global tmp
    result = {}
    if isinstance(instance, models.Model):
        for i in instance._meta.fields:
            try:
                tmp = getattr(instance, i.name + '_id')
            except:
                tmp = getattr(instance, i.name)
            finally:
                if isinstance(tmp, datetime.datetime):
                    tmp = str(tmp)
                result[i.name] = tmp
    return result


# 2.0根据微信名获取微信头像 @zhangfeng
def get_wx_avatar(username):
    avatar_path = False
    if username:
        avatar_api = 'http://open.weixin.qq.com/qr/code/?username=%s' % username
        avatar_path = Qiniu('mt-temp').save_remote(avatar_api, 'mt-temp')
    return avatar_path


def get_range(page_no):
    page = int(page_no)
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    return start, end
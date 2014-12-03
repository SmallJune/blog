# coding=utf-8
import hashlib

from django.core.cache import cache



__author__ = 'garfield'


class NewCache:
    config = {
        # 首页轮播图，缓存在接口中
        'home_cycle_new': {
            'time': 3600,  # 缓存时间
            'key': 'new_cache_promote_home_cycle_new',  #key前缀
            'sub_key': [],
            'dynamic_key': [],
        },
        # 首页精选，缓存在接口中
        'home_choice': {
            'time': 3600,
            'key': 'new_cache_promote_home_choice',
            'sub_key': ['home'],
            'dynamic_key': ['end'],
        },
        # 首页推荐灵感板，缓存在接口中
        'home_album': {
            'time': 3600,  #缓存时间
            'key': 'new_cache_promote_home_album',  #key前缀
            'sub_key': [],
            'dynamic_key': [],
        },
        #首页推荐商品，缓存在接口中
        # 'home_goods': {
        #     'time': 3600,  #缓存时间
        #     'key': 'new_cache_promote_home_goods',  #key前缀
        #     'sub_key': [],
        #     'dynamic_key': [],
        # },
        # 帖子详情页
        'detail_page': {
            'time': 3600,
            'key': 'new_cache_detail_page',
            'sub_key': ['mobile', 'web', 'supplier'],
            'dynamic_key': ['share_id'],
        },
        # 图片页及相关ajax
        'item_data': {
            'time': 3600,
            'key': 'new_cache_item_data',
            'sub_key': ['page', 'ext'],
            'dynamic_key': ['image_id'],
        },
        # # 商品图片页及相关ajax
        # 'goods_page_data': {
        #     'time': 3600,
        #     'key': 'new_cache_goods_page_data',
        #     'sub_key': [],
        #     'dynamic_key': [],
        # },
        #网站seo信息
        'site': {
            'time': 3600,
            'key': 'new_cache_website',
            'sub_key': [],
            'dynamic_key': [],
        },
        'category': {
            'time': 3600,
            'key': 'new_cache_category',
            'sub_key': ['card_theme', 'recommed_tag'],
            'dynamic_key': [],
        },
        'category_hot_tag': {
            'time': 3600,
            'key': 'new_cache_category_hot_tag',
            'sub_key': [],
            'dynamic_key': [],
        },
        # 不需要清理，缓存在接口中
        'color': {
            'time': 3600,
            'key': 'new_cache_color',
            'sub_key': [],
            'dynamic_key': [],
        },
        #友情链接 不需要清理，缓存在接口中
        'link': {
            'time': 3600,
            'key': 'new_cache_link',
            'sub_key': [],
            'dynamic_key': [],
        },
        #商家角色 不需要清理，缓存在接口中
        'role': {
            'time': 3600,
            'key': 'new_cache_role',
            'sub_key': [],
            'dynamic_key': [],
        },
        #灵感总数 不需要清理，缓存在接口中
        'site_post_total': {
            'time': 3600,
            'key': 'new_cache_site_post_total',
            'sub_key': [],
            'dynamic_key': [],
        },
        # TODO 似乎已经失效
        'cate_share': {
            'time': 3600,
            'key': 'new_cache_cate_share',
            'sub_key': ['selected', 'new'],
            'dynamic_key': ['cate_id'],
        },
        #用户分享的灵感
        'user_post': {
            'time': 3600,
            'key': 'new_cache_user_post',
            'sub_key': ['style', 'new'],
            'dynamic_key': ['user_id', 'year', 'month', 'city_id', 'service_id', 'name'],
        },
        #用户喜欢的图片
        'user_like': {
            'time': 15 * 60,
            'key': 'new_cache_user_like',
            'sub_key': ['user'],
            'dynamic_key': ['user_id'],
        },
        # 根据tag搜索的share数据
        'search_tag': {
            'time': 3600,
            'key': 'new_cache_search_tag',
            'sub_key': [],
            'dynamic_key': ['tag'],
        },
        #根据keyword搜索的share数据
        'search_keyword': {
            'time': 3600,
            'key': 'new_cache_search_keyword',
            'sub_key': [],
            'dynamic_key': ['keyword'],
        },
        #根据color搜索的share数据
        'search_color': {
            'time': 3600,
            'key': 'new_cache_search_color',
            'sub_key': [],
            'dynamic_key': ['color'],
        },
        #根据tag搜索的所有商品数据
        # 似乎已经失效
        'goods_tag': {
            'time': 3600,
            'key': 'new_cache_goods_tag',
            'sub_key': [],
            'dynamic_key': ['tag'],
        },
        #根据cate搜索的所有商品数据
        'goods_cate': {
            'time': 60 * 60,
            'key': 'cache_goods_cate',
            'sub_key': [],
            'dynamic_key': ['cate_id'],
        },
        #热门标签
        'hot_tag': {
            'time': 3600,
            'key': 'new_cache_hot_tag',
            'sub_key': [],
            'dynamic_key': ['cate_id'],
        },
        #商品页推荐标签
        # 似乎已经失效
        'command_goods_tag': {
            'time': 3600,
            'key': 'new_cache_hot_tag',
            'sub_key': [],
            'dynamic_key': [],
        },
        #类目推荐标签
        # 似乎已经失效
        'cate_command_tag': {
            'time': 1800,
            'key': 'new_cache_cate_command_tag',
            'sub_key': [],
            'dynamic_key': ['cate_id'],
        },
        #推荐订阅
        'command_subscribe_keyword': {
            'time': 1800,
            'key': 'new_cache_command_subscribe_keyword',
            'sub_key': [],
            'dynamic_key': [],
        },
        #用户订阅的内容
        'subscribe_share': {
            'time': 600,
            'key': 'new_cache_user_subscribe_share',
            'sub_key': [],
            'dynamic_key': ['user_id'],
        },
        #灵感板
        'user_album_share': {
            'time': 600,
            'key': 'new_cache_user_album_share',
            'sub_key': [],
            'dynamic_key': ['album_id'],
        },
        'province_city': {
            'time': 60000,
            'key': 'new_cache_province_city',
            'sub_key': [],
            'dynamic_key': [],
        },
        #商品总数
        'site_tk_total': {
            'time': 3600,
            'key': 'new_cache_site_tk_total',
            'sub_key': [],
            'dynamic_key': [],
        },
        #灵感板总数
        'site_album_total': {
            'time': 3600,
            'key': 'new_cache_site_album_total',
            'sub_key': [],
            'dynamic_key': [],
        },
        #图片总数
        # 首页相关数据，缓存在接口中
        'site_attach_total': {
            'time': 3600,
            'key': 'new_cache_site_attach_total',
            'sub_key': [],
            'dynamic_key': [],
        },
        #商家服务类目
        # TODO 这个缓存全部加在了接口里
        'supplier_service_cate': {
            'time': 3600,
            'key': 'new_cache_supplier_service_cate',
            'sub_key': ['service_cate', 'best_supplier'],
            'dynamic_key': ['service_id', 'post_id', 'service', 'style', 'city_id', 'number'],
        },
        #商家列表
        'supplier_list': {
            'time': 4 * 60 * 60,
            'key': 'new_cache_supplier_list',
            'sub_key': ['posts', 'recomends'],
            'dynamic_key': ['city_id', 'supplier_id', 'num'],
        },
        # 图片附加数据
        # 失效
        # 'image_ext_data': {
        #     'time': 10 * 60,
        #     'key': 'new_cache_image_ext_data',
        #     'sub_key': [],
        #     'dynamic_key': ['image_id'],
        # },
        #2.0 用户故事时间轴
        # 时间轴缓存在页面中 本缓存失效
        # 'time_line': {
        #     'time': 60 * 60,
        #     'key': 'new_cache_time_line',
        #     'sub_key': [],
        #     'dynamic_key': ['user_id'],
        # },
        #2.0 专题页
        'special_page': {
            'time': 60 * 60,
            'key': 'new_cache_special_page',
            'sub_key': [],
            'dynamic_key': ['site_id'],
        },
        'public_banner': {
            'time': 60 * 60,
            'key': 'new_cache_public_banner',
            'sub_key': [],
            'dynamic_key': ['city_id', 'site_type'],
        },
        #2.0 猜你喜欢
        'guess_data': {
            'time': 60 * 15,
            'key': 'new_cache_guess_data',
            'sub_key': ['post', 'service', 'goods'],
            'dynamic_key': ['tag'],
        },
        'search_origin': {
            'time': 60 * 15,
            'key': 'new_cache_search_data',
            'sub_key': [],
            'dynamic_key': ['origin'],
        },

        'search_goods': {
            'time': 60 * 15,
            'key': 'new_cache_search_data',
            'sub_key': [],
            'dynamic_key': ['goods'],
        },
        'search_supplier': {
            'time': 60 * 15,
            'key': 'new_cache_search_data',
            'sub_key': [],
            'dynamic_key': ['city_id', 'supplier'],
        },

        #2.0 获取service和city_id
        'get_commonservice': {
            'time': 60 * 60,
            'key': 'new_cache_get_commonservice',
            'sub_key': [],
            'dynamic_key': ['service_id', 'city_id'],
        },
        # 用户个人空间
        'user_home': {
            'time': 60 * 60,
            'key': 'new_cache_user_home',
            'sub_key': ['album', 'weddstory', 'like'],
            'dynamic_key': ['user_id', 'year', 'month'],
        },
        # 服务商首页
        'supplier_home': {
            'time': 60 * 60,
            'key': 'new_cache_supplier_home',
            'sub_key': ['home', 'post', 'service_list'],
            'dynamic_key': ['user_id'],
        },
        'shop_item': {
            'time': 60 * 60,
            'key': 'new_cache_shop_item',
            'sub_key': [],
            'dynamic_key': ['item_id'],
        },
        'user_shop': {
            'time': 3600,
            'key': 'new_cache_user_shop',
            'sub_key': [],
            'dynamic_key': ['user_id'],
        },
        'special_item': {
            'time': 3600,
            'key': 'cache_special_item',
            'sub_key': ['banner', 'content'],
            'dynamic_key': ['special_id'],
        },
        'user_info': {
            'time': 3600,
            'key': 'new_cache_user_info',
            'sub_key': ['step'],
            'dynamic_key': ['user_id'],
        }
    }
    page = [0, 1, 2, 3, 4]
    '''
        NewCache('detail_page').set(data,sub_key,**kwargs)
        sub_key sub_key的值为列表里的一个值
        **kwargs 型参为dynamic_key列表里的值，dynamic_key的值都是必填的
        example: NewCache('detail_page').set(data,sub_key='mobile',share_id=xxx)
                 NewCache('detail_page').get(sub_key='mobile',share_id=xxx)
                 NewCache('detail_page').delete(sub_key='mobile',share_id=xxx) #mode默认等于False
                 NewCache('detail_page').delete(mode=True,share_id=xxx)
    '''

    def __init__(self, key):
        self.cache_config = NewCache.config.get(key) or None

    def get(self, **kwargs):
        cache_config = self.cache_config
        if not cache_config:
            return None
        else:
            cache_key = cache_config.get('key')

            # try:
            if kwargs.get('sub_key'):
                if kwargs['sub_key'] in cache_config['sub_key']:
                    cache_key += '_' + str(kwargs['sub_key'])
                    kwargs.pop('sub_key')
                # else:
                #     raise KeyError
            for i in cache_config['dynamic_key']:
                try:
                    value = kwargs.pop(i)
                    cache_key += '_' + i + '_' + str(value)
                except:
                    pass
            if 'page' in kwargs.keys():
                cache_key += '_page_' + str(kwargs.pop('page'))
            # if len(kwargs) > 0:
            #     raise KeyError
            # except:
            # return None
            data = cache.get(hashlib.md5(cache_key).hexdigest())
            return data

    def set(self, data, **kwargs):
        cache_config = self.cache_config
        cache_time = cache_config.get('time')
        cache_key = cache_config.get('key')
        # try:
        if kwargs.get('sub_key'):
            if kwargs['sub_key'] in cache_config['sub_key']:
                cache_key += '_' + str(kwargs['sub_key'])
                kwargs.pop('sub_key')
            # else:
            #     raise KeyError

        for i in cache_config['dynamic_key']:
            try:
                value = kwargs.pop(i)
                cache_key += '_' + i + '_' + str(value)
            except:
                pass
        # for k, v in kwargs.items():
        #     if k == 'page':
        #         continue
        #     if k in cache_config['dynamic_key']:
        #         cache_key += '_' + k + '_' + str(v)
        #     else:
        #         raise KeyError
        if 'page' in kwargs.keys():
            cache_key += '_page_' + str(kwargs.pop('page'))
        # if len(kwargs) > 0:
        #     raise KeyError
        # except:
        # return None
        cache.set(hashlib.md5(cache_key).hexdigest(), data, cache_time)

    # paging 表示数据是分页到，paging=True 将清空分页数据
    def delete(self, paging=False, **kwargs):
        cache_config = self.cache_config
        cache_key = cache_config.get('key')
        tail_key = ''
        # try:
        for i in cache_config['dynamic_key']:
            if kwargs.get(i):
                tail_key += '_' + i + '_' + str(kwargs[i])
        # except:
        # return None

        if not 'sub_key' in kwargs.keys():
            if cache_config['sub_key']:
                for i in cache_config['sub_key']:
                    temp = cache_key + '_' + i + tail_key
                    if paging:
                        for x in NewCache.page:
                            cache.delete(hashlib.md5(temp + '_page_' + str(x)).hexdigest())
                    else:
                        cache.delete(hashlib.md5(temp).hexdigest())
            temp = cache_key + tail_key
            if paging:
                for i in NewCache.page:
                    cache.delete(hashlib.md5(temp + '_page_' + str(i)).hexdigest())
            cache.delete(hashlib.md5(temp).hexdigest())
        # 定向删除
        else:
            if kwargs['sub_key'] in cache_config['sub_key']:
                cache_key += '_' + str(kwargs['sub_key'])
            temp = cache_key + tail_key
            if paging:
                for i in NewCache.page:
                    cache.delete(hashlib.md5(temp + '_page_' + str(i)).hexdigest())
            cache.delete(hashlib.md5(temp).hexdigest())

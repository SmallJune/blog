# coding:utf-8
import hashlib
import sys

from django.core.cache import cache


reload(sys)
sys.setdefaultencoding('utf8')

# 缓存

class MtCache:
    def __init__(self, key):
        config = {
            'home_cycle_new': {
                'time': 60 * 60,  #缓存时间
                'key': 'cache_promote_home_cycle_new'  #key前缀
            },
            'home_choice': {
                'time': 60 * 60,
                'key': 'cache_promote_home_choice'
            },
            #首页推荐灵感板
            'home_album': {
                'time': 60 * 60,  #缓存时间
                'key': 'cache_promote_home_album'  #key前缀
            },
            #首页推荐商品
            'home_goods': {
                'time': 60 * 60,  #缓存时间
                'key': 'cache_promote_home_goods'  #key前缀
            },
            # 帖子详情页
            'detail_page': {
                'time': 3600,
                'key': 'cache_detail_page'
            },
            # 图片页及相关ajax
            'item_data': {
                'time': 3600,
                'key': 'cache_item_data'
            },
            # 商品图片页及相关ajax
            'goods_page_data': {
                'time': 3600,
                'key': 'cache_goods_page_data'
            },
            #网站seo信息
            'site': {
                'time': 60 * 60,
                'key': 'cache_website'
            },
            'category': {
                'time': 60 * 60,
                'key': 'cache_category'
            },
            'category_hot_tag': {
                'time': 60 * 60,
                'key': 'cache_category_hot_tag'
            },
            'color': {
                'time': 60 * 60,
                'key': 'cache_color'
            },
            #友情链接
            'link': {
                'time': 60 * 60,
                'key': 'cache_link'
            },
            #商家角色
            'role': {
                'time': 60 * 60,
                'key': 'cache_role'
            },
            #灵感总数
            'site_post_total': {
                'time': 60 * 60,
                'key': 'cache_site_post_total'
            },
            'cate_share': {
                'time': 60 * 60,
                'key': 'cache_cate_share'
            },
            #用户分享的灵感
            'user_post': {
                'time': 60 * 60,
                'key': 'cache_user_post'
            },
            #用户喜欢的图片
            'user_like': {
                'time': 15 * 60,
                'key': 'cache_user_like'
            },
            #根据tag搜索的share数据
            'search_tag': {
                'time': 60 * 60,
                'key': 'cache_search_tag'
            },
            #根据keyword搜索的share数据
            'search_keyword': {
                'time': 60 * 60,
                'key': 'cache_search_keyword'
            },
            #根据color搜索的share数据
            'search_color': {
                'time': 60 * 60,
                'key': 'cache_search_color'
            },
            #根据tag搜索的所有商品数据
            'goods_tag': {
                'time': 60 * 60,
                'key': 'cache_goods_tag'
            },
            #根据cate搜索的所有商品数据
            'goods_cate': {
                'time': 60 * 60,
                'key': 'cache_goods_cate'
            },
            #热门标签
            'hot_tag': {
                'time': 60 * 60,
                'key': 'cache_hot_tag'
            },
            #商品页推荐标签
            'command_goods_tag': {
                'time': 10 * 60,
                'key': 'cache_hot_tag'
            },
            #类目推荐标签
            'cate_command_tag': {
                'time': 30 * 60,
                'key': 'cache_cate_command_tag'
            },
            #推荐订阅
            'command_subscribe_keyword': {
                'time': 30 * 60,
                'key': 'cache_command_subscribe_keyword'
            },
            #用户订阅的内容
            'subscribe_share': {
                'time': 10 * 60,
                'key': 'cache_user_subscribe_share'
            },
            #灵感板
            'user_album_share': {
                'time': 10 * 60,
                'key': 'cache_user_album_share'
            },
            'province_city': {
                'time': 1000 * 60,
                'key': 'cache_province_city'
            },
            #商品总数
            'site_tk_total': {
                'time': 60 * 60,
                'key': 'cache_site_tk_total'
            },
            #灵感板总数
            'site_album_total': {
                'time': 60 * 60,
                'key': 'cache_site_album_total'
            },
            #图片总数
            'site_attach_total': {
                'time': 60 * 60,
                'key': 'cache_site_attach_total'
            },
            #商家服务类目
            'supplier_service_cate': {
                'time': 60 * 60,
                'key': 'cache_supplier_service_cate'
            },
            #商家列表
            'supplier_list': {
                'time': 4 * 60 * 60,
                'key': 'cache_supplier_list'
            },
            #图片附加数据
            'image_ext_data': {
                'time': 10 * 60,
                'key': 'cache_image_ext_data'
            },
            #2.0 用户故事时间轴
            'time_line': {
                'time': 60 * 60,
                'key': 'cache_time_line'
            },
            #2.0 专题页
            'special_page': {
                'time': 60 * 60,
                'key': 'cache_special_page'
            },
            'public_banner': {
                'time': 60 * 60,
                'key': 'cache_public_banner'
            },
            #2.0 猜你喜欢
            'guess_data': {
                'time': 60 * 15,
                'key': 'cache_wedding_data'
            },
            'search_origin': {
                'time': 60 * 15,
                'key': 'cache_search_data'
            },
            'search_goods': {
                'time': 60 * 15,
                'key': 'cache_search_data'
            },
            'search_supplier': {
                'time': 60 * 15,
                'key': 'cache_search_data'
            },
            #2.0 获取service和city_id
            'get_commonservice': {
                'time': 60 * 60,
                'key': 'cache_get_commonservice'
            },
            # 用户个人空间
            'user_home': {
                'time': 60 * 60,
                'key': 'cache_user_home',
            },
            # 服务商首页
            'supplier_home': {
                'time': 60 * 60,
                'key': 'cache_supplier_home'
            },
            'shop_item': {
                'time': 60 * 60,
                'key': 'cache_shop_item',
            },
            'user_shop': {
                'time': 3600,
                'key': 'cache_user_shop',
            },
            'special_item': {
                'time': 3600,
                'key': 'cache_special_item',
            }
        }

        self.cache_config = config.get(key) or None


    #取
    def get(self, **kwargs):
        cache_config = self.cache_config
        if not cache_config:
            return None
        else:
            cache_key = cache_config.get('key')
            for key in kwargs:
                cache_key = cache_key + '_' + str(kwargs[key])
            data = cache.get(hashlib.md5(cache_key).hexdigest())
            return data

    #存
    def set(self, data, **kwargs):
        cache_config = self.cache_config
        cache_time = cache_config.get('time')
        cache_key = cache_config.get('key')

        for key in kwargs:
            cache_key = cache_key + '_' + str(kwargs[key])
        cache.set(hashlib.md5(cache_key).hexdigest(), data, cache_time)

    #删除
    def delete(self, **kwargs):
        cache_config = self.cache_config
        cache_key = cache_config.get('key')

        for key in kwargs:
            cache_key = cache_key + '_' + str(kwargs[key])
        cache.delete(hashlib.md5(cache_key).hexdigest())

    # def log(self,content):
    #     path = '/tmp/goods.log'
    #     fsock = open(path, 'a')
    #     fsock.write(content+'\n')
    #     fsock.close()
    #     return None
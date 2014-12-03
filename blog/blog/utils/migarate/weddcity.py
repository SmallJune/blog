#coding:utf-8
import logging
import threading
import time

from django.conf import settings


settings.configure(
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'new_lovewith',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': '19881988',
        'HOST': '127.0.0.1',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',                      # Set to empty string for default.
        }
    }
)

from django.db import models


class MtUserWeddingData(models.Model):
    step_type = ((1, u'我的信息完成'), (2, u'另一半'), (3, u'时间'), (4, u'地点'))
    bride = models.CharField(max_length=30, blank=True, null=True, verbose_name=u'新娘')
    bridegroom = models.CharField(max_length=30, blank=True, null=True, verbose_name=u'新郎')
    wedding_date = models.CharField(max_length=30, blank=True, null=True, verbose_name=u'日期')
    wedding_time = models.CharField(max_length=30, blank=True, null=True, verbose_name=u'时间')
    city = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'城市')
    wedd_city_id = models.IntegerField()
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'地点')
    #新郎：1 新娘: 2
    user_role = models.SmallIntegerField(max_length=1, default=1, verbose_name=u'用户身份')
    user_id = models.IntegerField()
    # 2.0 new filed
    love_id = models.IntegerField()
    love_avatar = models.CharField(max_length=255, verbose_name=u'路径')
    is_active = models.BooleanField(default=False, verbose_name=u'激活帐号')
    is_wedding_date = models.BooleanField(default=False, verbose_name=u'日期确定')
    is_wedding_time = models.BooleanField(default=False, verbose_name=u'具体时间')
    is_address = models.BooleanField(default=False, verbose_name=u'地址')
    is_map = models.BooleanField(default=False, verbose_name=u'百度地图')
    step = models.SmallIntegerField(choices=step_type, max_length=1, default=0, verbose_name=u'信息填写状态')

    def __unicode__(self):
        return self.bride

    class Meta:
        app_label='weddcity'
        verbose_name_plural = u'婚礼信息'
        db_table = 'mt_user_wedding_data'

class City(models.Model):
    province_id = models.IntegerField()
    name = models.CharField(max_length=45, verbose_name=u'市')

    def __unicode__(self):
        return self.name

    class Meta:
        app_label='weddcity'
        verbose_name_plural = u'市'
        db_table = 'mt_province_city'


class RunThread(threading.Thread):
    length=0
    offset=100
    def run(self):
        start=0
        end=start+self.offset
        while(self.length>0):
            if(end>self.length):
                end=self.length
            result = MtUserWeddingData.objects.all()[start:end]
            for list in result:
                try:
                    tmp=City.objects.get(name=list.city)
                    if tmp:
                        list.wedd_city_id=tmp.id
                        list.save()
                        print list.id,":",list.city,":",tmp.id
                    else :
                        print list.id,'no matched row!'
                except Exception,e:
                    print e
                    logging.basicConfig(filename='error.log',level = logging.DEBUG)
                    if list.city:
                        message = 'mt_user_wedding_data:row '+str(list.id)+" not affected,city:"+list.city.encode('utf-8')
                        logging.debug(message)
                        print list.city," goes error!"
                    continue
                finally:
                     pass
            start=end+1
            end=end+self.offset
            time.sleep(1)
    def __init__(self):
        threading.Thread.__init__(self)
        self.length = MtUserWeddingData.objects.count()
        print "thread start!"

if __name__ == "__main__":
    a = RunThread()
    a.daemon=True
    a.start()
    while True:
        time.sleep(100)

__author__ = 'garfield'
import threading
import time
import os.path
import sys

from django.core.management import setup_environ


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'lovewith.settings'
from lovewith import settings

setup_environ(settings)
from lovewith.share.models import Attachment


def update_title():
    tt = RunThread()
    tt.daemon = True
    tt.start()
    while True:
        time.sleep(100)


class RunThread(threading.Thread):
    length = 0
    offset = 500

    def __init__(self):
        threading.Thread.__init__(self)
        from lovewith.share.models import AttachGoods
        #self.length=20
        self.length = AttachGoods.objects.count()
        # self.length = 30
        print 'start!'

    def run(self):
        from lovewith.share.models import AttachGoods
        from lovewith.share.models import MtGoodsPost
        start = 0
        end = start + self.offset
        while self.length > start:
            end = self.length if end > self.length else end
            to_be_created = AttachGoods.objects.filter(post_image__is_delete=0)[start:end]
            create_list = []
            for single in to_be_created:
                try:
                    temp_goods_post = MtGoodsPost(
                        title=single.product_name,
                        user=single.user,
                        price=single.product_price,
                        link=single.product_url,
                    )
                    temp_goods_post.save()
                    image = single.post_image
                    create_list.append(Attachment(
                        path=image.path,
                        tag=image.tag,
                        content=image.content,
                        is_cover=1,
                        like=image.like,
                        share_post=temp_goods_post.id,
                        is_delete=0,
                        is_top=image.is_top,
                        cate=image.cate,
                        click_num=image.click_num,
                        sort=1,
                        attr_type=1,
                        title=image.title
                    ))
                    print(str(single.id) + ' add complete!')
                except Exception, e:
                    print e
                    log(str(single.id))
            Attachment.objects.bulk_create(create_list)
            print(str(start) + ' -- ' + str(end) + 'created!')
            start = end + 1
            end += self.offset
            time.sleep(1)


def log(content):
    print content
    path = '/tmp/goods.log'
    fsock = open(path, 'a')
    fsock.write(content)
    fsock.close()
    return None
if __name__ == '__main__':
    update_title()
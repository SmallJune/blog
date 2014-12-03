import Queue

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
from lovewith.share.models import AttachTag


class WorkManager(object):
    def __init__(self, thread_num=5):
        self.work_queue = Queue.Queue(300)
        self.threads = []
        self.__init_producer_queue()
        self.__init_consumer_thread_pool(thread_num)

    def __init_consumer_thread_pool(self, thread_num):
        for i in range(thread_num):
            consumer = Consumer(self.work_queue)
            consumer.daemon =True
            self.threads.append(consumer)
            consumer.start()

    def __init_producer_queue(self):
        producer = Producer(queue=self.work_queue)
        producer.daemon=True
        producer.start()

    def wait_all_complete(self):
        for item in self.threads:
            if item.isAlive():
                item.join()


class Producer(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.work_queue = queue
        self.length = Attachment.objects.count()
        self.offset = 200
        print "Producer start!"

    def run(self):
        split_start = 0
        split_end = split_start + self.offset
        while self.length >= split_start:
            if split_end > self.length:
                split_end = self.length
            result = Attachment.objects.all()[split_start:split_end]
            self.work_queue.put(result)
            split_start = split_end
            split_end += self.offset


class Consumer(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue

    def run(self):
        while True:
            queryset = self.work_queue.get()
            for single_att in queryset:
                try:
                    s = single_att
                    tmp = AttachTag.objects.filter(post_image_id=single_att.id)
                    if tmp:
                        cate_id = tmp[0].cate_id
                        click_num = 0
                        tagnames = []
                        for element in tmp:
                            click_num += int(element.click_num)
                            tagnames.append(element.tagname)
                        s.cate_id = cate_id
                        s.click_num = click_num
                        s.tag = ','.join(tagnames)
                        s.save()
                        print s.id, "  cate_id:", s.cate_id, " click_num:", s.click_num
                        print "cate_id:", s.cate_id, "  click_num:", s.click_num
                    else:
                        s.tag = ''
                        s.cate_id = 1
                        s.save()
                        print '%s\'s cate_id been has setted to 1' % (s.id)
                except Exception, e:
                    print e
                    e_message = 'mt_attachment:row ' + str(single_att.id) + ' not affected.'
                    log(str(single_att.id))
                    print single_att.id, " goes error!"
                    continue
                finally:
                    pass
            self.work_queue.task_done()


def log(content):
    print content
    path = '/tmp/attach.log'
    fsock = open(path, 'a')
    fsock.write(content+'\n')
    fsock.close()
    return None


if __name__ == "__main__":
    work_manager = WorkManager(10)
    time.sleep(5)
    work_manager.wait_all_complete()

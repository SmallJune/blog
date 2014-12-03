import time

__author__ = 'garfield'
import Queue
import threading
import os.path
import sys
from django.core.management import setup_environ

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'lovewith.settings'
from lovewith import settings

setup_environ(settings)
from lovewith.share.models import Attachment,  Post


class WorkManager(object):
    def __init__(self, thread_num=5):
        self.work_queue = Queue.Queue(maxsize=300)
        self.threads = []
        self.__init_producer_queue()
        self.__init_consumer_thread_pool(thread_num)

    def __init_consumer_thread_pool(self, thread_num):
        for i in range(thread_num):
            consumer = Consumer(self.work_queue)
            self.threads.append(consumer)
            consumer.start()

    def __init_producer_queue(self):
        producer = Producer(self.work_queue)
        producer.daemon = True
        producer.start()

    def wait_all_complete(self):
        for item in self.threads:
            if item.isAlive():
                item.join()


class Producer(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.length = Post.objects.count()
        self.offset = 5

    def run(self):
        split_start = 0
        split_end = split_start + self.offset
        while True:
            split_end = self.length if split_end > self.length else split_end
            to_be_update = Post.objects.all()[split_start:split_end]
            self.work_queue.put(to_be_update)
            split_start = split_end
            split_end += self.offset
            if split_end == self.length:
                break


class Consumer(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue

    def run(self):
        while True:
            queryset = self.work_queue.get()
            for post in queryset:
                try:
                    print 'doing job with ', str(post.id)
                    Attachment.objects.filter(share_post_id=post.id).update(title=post.title)
                except Exception, e:
                    print e
                    log(str(post.id))
            self.work_queue.task_done()
def log(content):
    print content
    path = '/tmp/title.log'
    fsock = open(path, 'a')
    fsock.write(content+'\n')
    fsock.close()
    return None

if __name__ == "__main__":
    work_manager = WorkManager(2)
    time.sleep(5)
    work_manager.wait_all_complete()






















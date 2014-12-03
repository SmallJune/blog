import os
import requests
import sys

from django.core.management import setup_environ


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'lovewith.settings'
from lovewith import settings
setup_environ(settings)
import Queue
import threading
import time
from lovewith.share.models import Attachment

__author__ = 'garfield'

import ConfigParser


class Recorder:
    def __init__(self):
        pass

    def save_last(self, value):
        with open('size.config', 'r') as cfgfile:
            config.readfp(cfgfile)
            old_last = config.get('size', 'last')
        print 'my value: '+ str(value)
        if value > int(old_last):
            print 'old: '+str(old_last)+' new: '+str(value)
            log('i write ' + str(value))
            config.set('size', 'last', value=value)
            config.write(open('size.config','w'))


class WorkManager(object):
    def __init__(self, _start=0, _offset=200, thread_num=5):
        self.work_queue = Queue.Queue(maxsize=150)
        self.threads = []
        self.__init_producer_queue(_start, _offset)
        self.__init_consumer_thread_pool(thread_num)
        print 'workmanager init !!'

    def __init_consumer_thread_pool(self, thread_num):
        for i in range(thread_num):
            consumer = Consumer(self.work_queue)
            consumer.daemon = True
            self.threads.append(consumer)
            consumer.start()

    def __init_producer_queue(self, _start, _offset):
        producer = Producer(self.work_queue, _start, _offset)
        producer.daemon = True
        producer.start()

    def wait_all_complete(self):
        for item in self.threads:
            if item.isAlive():
                item.join()


class Producer(threading.Thread):
    def __init__(self, work_queue, _start, _offset):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.length = Attachment.objects.count()
        self._start = _start
        self._offset = _offset
        print 'Producer init success!'

    def run(self):
        split_start = self._start
        split_end = split_start + self._offset
        while True:
            split_end = self.length if split_end > self.length else split_end
            to_be_update = Attachment.objects.all()[split_start:split_end]
            self.work_queue.put((to_be_update, split_end))
            split_start = split_end
            split_end += self._offset
            if split_end == self.length:
                break


class Consumer(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.lock = threading.Lock()
        print 'consumer init !'

    def run(self):
        while True:
            queryset, end = self.work_queue.get()
            for attachment in queryset:
                try:
                    print 'doing job with ', str(attachment.id)
                    info = requests.get(attachment.path + '?imageInfo')
                    image_info = info.json() if int(info.status_code)==200 else None
                    if image_info:
                        size = str(image_info['width']) + 'x' + str(image_info['height']) if image_info else '280x280'
                        attachment.size = size
                        attachment.save()
                    log(str(attachment.id)+' done')
                except Exception, e:
                    log(str(attachment.id)+' : '+str(e)+'\n'+'='*20, '/tmp/size_error.log')
            hour = time.strftime('%H', time.localtime(time.time()))
            if int(hour) >= 5:
                self.lock.acquire()
                Recorder().save_last(value=end)
                self.lock.release()
                print 'i quit!'
                break
            else:
                self.work_queue.task_done()


def log(content, path='/tmp/size.log'):
    print content
    path = path
    fsock = open(path, 'a')
    fsock.write(content + '\n')
    fsock.close()
    return None


if __name__ == "__main__":
    path = str(os.path.split(os.path.realpath(__file__))[0]) + '/size.config'
    config = ConfigParser.ConfigParser()
    with open(path, 'r') as cfgfile:
        config.readfp(cfgfile)
        offset = config.get('size', 'offset')
        start = config.get('size', 'last')
    work = WorkManager(_start=int(start), _offset=int(offset), thread_num=5)
    work.wait_all_complete()

#!/usr/bin/python
#coding=utf-8
import io
import os
import time
import hashlib
from PIL import Image
from urllib2 import urlopen
from lovewith.api.qiniu import Qiniu
from lovewith.api.upyun_tools import Upyun
from lovewith.share.models import Post, Attachment
from lovewith.settings import FILE_UPLOAD_PATH


class MtImage:
    def __init__(self):
        self.base_path = FILE_UPLOAD_PATH

    #获取文件保存路径
    def get_save_path(self):
        save_path = time.strftime('%Y/%m/%d/', time.localtime(time.time()))

        try:
            os.makedirs('%stemp/%s' % (self.base_path, save_path))
        except StandardError, api_error:
            pass

        return save_path

    #缩略图
    def create_thumb(self, original, width, height, crop_x=0, crop_y=0):
        original = '%s%s' % (self.base_path, original)

        file_path, file_ext = os.path.splitext(original)
        img = Image.open(original)
        o_width, o_height = img.size

        o_width = int(o_width)
        o_height = int(o_height)

        #按width缩放,裁剪高度
        new_width = width
        new_height = int((o_height * new_width) / o_width)

        if new_height > height:
            #生成比较高的缩略图
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
            #裁剪多余的高度
            img = img.crop((0, crop_y, new_width, height + crop_y))
        else:
            new_height = height
            new_width = int((o_width * new_height) / o_height)
            #生成比较宽的缩略图
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
            if not crop_x:
                #计算裁剪的x偏移
                x = int((new_width - width) / 2)
            else:
                x = crop_x
            #裁剪多余的宽度
            img = img.crop((x, crop_y, x + width, new_height))

        new_file_name = '%s_%sx%s%s' % (file_path, width, height, file_ext)
        #保存图片
        img = img.convert('RGB')
        img.save(new_file_name, quality=90)

        #返回完整图片路径
        return new_file_name

    #读取远程图片
    @staticmethod
    def read_remote_image(image_path):
        image_bytes = urlopen('%s!650' % image_path).read()
        data_stream = io.BytesIO(image_bytes)

        return Image.open(data_stream)

    #合并图片
    def combo_images_by_share(self, share_id):
        share_filter_data = Post.objects.filter(id=int(share_id))
        if not share_filter_data.exists():
            #帖子不存在
            return False
        else:
            share_data = share_filter_data[0]
            #获取全部帖子图片
            images_data = Attachment.objects.filter(share_post=share_data)
            if not images_data.exists():
                #没有图片
                return False
            else:
                image_handle = []
                #合并后的图片宽度
                target_width = 440
                #合并后图片总高度
                total_height = 0
                #合并后的文件名
                combo_file_name = None

                #遍历图片取最小宽度
                for i, img in enumerate(images_data.iterator()):
                    if i < 20:
                        the_img = None
                        try:
                            if img.path.find('http') < 0:
                                the_img = Image.open('%stemp/%s' % (self.base_path, img.path))
                            else:
                                the_img = self.read_remote_image(img.path)
                        except StandardError, api_error:
                            pass
                        if the_img:
                            if not combo_file_name:
                                combo_file_name = '%s.jpg' % hashlib.new('md5', img.path + str(time.time())).hexdigest()

                            o_width, o_height = the_img.size

                            #取20张图片中宽度最小的
                            if o_width < target_width:
                                target_width = o_width

                            #遍历一次后保存结果
                            image_handle.append({
                                'handle': the_img,
                                'width': o_width,
                                'height': o_height
                            })

                #计算合并后图片的高度
                for i, img in enumerate(image_handle):
                    target_height = int((img.get('height') * target_width) / img.get('width'))
                    total_height += target_height

                #新建合并后的图片
                combo_img = Image.new('RGBA', (target_width, total_height))
                #粘贴开始位置
                target_top = 0

                #遍历图片合并
                for img in image_handle:
                    o_width = img.get('width')
                    o_height = img.get('height')
                    the_img = img.get('handle')

                    #计算缩放后的图片高度
                    target_height = int((o_height * target_width) / o_width)
                    #缩放图片
                    scale_img = the_img.resize((target_width, target_height), Image.ANTIALIAS)
                    #合并图片
                    combo_img.paste(scale_img, (0, target_top))

                    target_top += target_height

                if total_height == 0:
                    return False
                else:
                    save_path = '%s%s' % (self.get_save_path(), combo_file_name)
                    combo_path = '%stemp/%s' % (self.base_path, save_path)
                    combo_img.save(combo_path, quality=100)

                    #上传到upyun
                    combo_url = Qiniu('mt-share').upload(combo_path)
                    #更新数据库
                    share_data.combo_path = combo_url['path'].replace(' ', '')
                    share_data.save()

                    return combo_url['path']

    #放大并根据坐标裁剪指定区域
    def scale_and_crop(self, original, target_width, target_height, crop_x, crop_y, crop_width, crop_height):
        original_path = '%s%s' % (self.base_path, original)

        img = Image.open(original_path)
        #缩放到指定大小
        img = img.resize((target_width, target_height), Image.ANTIALIAS)
        #裁剪
        img = img.crop((crop_x, crop_y, crop_x + crop_width, crop_y + crop_height))
        #覆盖原图
        img = img.convert('RGB')
        img.save(original_path, quality=95)

        #返回完整图片路径
        return original_path
# -*- coding: utf-8 -*-
import time

from Database.models import get_db
from Database.tables import UserImage, Image, AppointmentImage, \
    ActivityImage, CompanionImg, WApCompanionImage,CommuQuesImg,\
    TrendImage

'''
 创建者：兰威 黄鑫晨
 创建时间：2016-08-30 18:05
'''


class ImageHandler(object):
    # def __init__(self):
    # @staticmethod
    def insert(self, list):
        '''
        向数据库插入图片链接
        :param list: 图片名的列表
        :table: 应该插入的表名
        :return:
        '''
        new_imids = []
        for img_name in list:  # 第一步，向Image里表里插入
            image = Image(
                IMvalid=True,
                IMT=time.strftime('%Y-%m-%d %H:%M:%S'),
                IMname=img_name
            )
            try:
                db = get_db()
                db.merge(image)
                db.commit()
                new_img = get_db().query(Image).filter(Image.IMname == img_name).one()
                imid = new_img.IMid
                new_imids.append(imid)
            except Exception,e:
                print "数据库操作：图片插入失败"+str(e)
        return new_imids

    # @staticmethod
    def insert_user_image(self, list, uid):
        '''
        Args:
            list:图片名字的数组
            uid: 用户的ID
        Returns:
        '''
        imids = self.insert(list)
        for i in range(len(imids)):
            image = UserImage(
                UIuid=uid,
                UIimid=imids[i],
                UIurl=list[i]
            )
            try:
                db = get_db()
                db.merge(image)
                db.commit()
            except Exception,e:
                print "数据库操作：用户图片插入失败" + str(e)

    # @staticmethod
    def insert_activity_image(self, list, ac_id):
        '''
        Args:
            list: 图片的名字的数组
            ac_id: 活动的ID
        Returns:
        '''
        imids = self.insert(list)
        for i in range(len(imids)):
            image = ActivityImage(
                ACIacid=ac_id,
                ACIimid=imids[i],
                ACIurl=list[i]
            )
            try:
                db = get_db()
                db.merge(image)
                db.commit()
            except Exception,e:
                print "数据库操作：活动图片插入失败" + str(e)

    # @staticmethod
    def insert_appointment_image(self, list, ap_id):
        '''
        Args:
            list: 图片名字的数组
            ap_id: 约拍的ID
        Returns:
        '''
        imids = self.insert(list)
        for i in range(len(imids)):
            image = AppointmentImage(
                APIapid=ap_id,
                APIimid=imids[i],
                APIurl=list[i]
            )
            try:
                db = get_db()
                db.merge(image)
                db.commit()
            except Exception,e:
                print "数据库操作：约拍图片插入失败" + str(e)

    def change_user_headimage(self, newimage, uid):
        db = get_db()
        images = db.query(UserImage).filter(UserImage.UIuid == uid).all()
        for image in images:
            image_id = image.UIimid
            im = db.query(Image).filter(Image.IMid == image_id).one()
            if im.IMvalid == 1:
                im.IMvalid = 0
        db.commit()
        self.insert_user_image(newimage, uid)

    # print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # timen = time.strftime('%Y-%m-%dT%H:%M:%S')
    # timeStamp = int(time.mktime(timen))
    # print timeStamp

    def insert_companion_image(self, list, Companion_id):  # 插入约拍伴侣图片
        '''
        Args:
            list: 图片的名字的数组
            ac_id: 约拍伴侣的id
        Returns:
        '''
        imagehandler = ImageHandler()
        imids = imagehandler.insert(list)
        for i in range(len(imids)):
            image = WApCompanionImage(
                WAPCid=Companion_id,
                WAPCimid=imids[i],
                WAPCurl=list[i],
            )
            try:
                db = get_db()
                db.merge(image)
                db.commit()
            except Exception,e:
                print "数据库操作：约拍图片插入失败" + str(e)

    def insert_commuques_image(self, list, question_id):  # 插入社区问题图片
        '''
        Args:
            list: 图片的名字的数组
            question_id: 社区问题的id
        Returns:
        '''
        imagehandler = ImageHandler()
        imids = imagehandler.insert(list)
        for i in range(len(imids)):
            image = CommuQuesImg(
                CQquesid=question_id,
                CQimid=imids[i],
                CQimurl=list[i],
            )
            try:
                db = get_db()
                db.merge(image)
                db.commit()
            except Exception,e:
                print "数据库操作：社区问题图片插入失败" + str(e)

    def insert_trend_image(self, list, trend_id):  # 插入社区问题图片
        '''
        Args:
            list: 图片的名字的数组
            trend_id: 动态的id
        Returns:
        '''
        imagehandler = ImageHandler()
        imids = imagehandler.insert(list)
        for i in range(len(imids)):
            image = TrendImage(
                TItid=trend_id,
                TIimid=imids[i],
                TIimgurl=list[i],
            )
            try:
                db = get_db()
                db.merge(image)
                db.commit()
            except Exception,e:
                print "数据库操作：动态图片插入失败" + str(e)
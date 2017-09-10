# -*- coding:utf-8 -*-
import json


from Appointment.APmodel import APmodelHandler
from BaseHandler import BaseHandler

# 约拍伴侣
from Database.tables import WApCompanions, WAcAuth
from FileHandler.ImageHandler import ImageHandler


class ApCompanionHandler(BaseHandler):
    retjson = {'code': '', 'contents': ''}

    def post(self):
        type = self.get_argument('type')
        
        if type == '80005':    # 发布约拍伴侣
            apc_title = self.get_argument('title')
            ap_org = self.get_argument('organization')
            apc_content = self.get_argument('content')
            apc_url = self.get_argument('url')
            apc_img = self.get_arguments('imgs[]')

            new_companion = WApCompanions(
                            WAPCname=apc_title,
                            WAPCServeintro=apc_content,  # 服务内容介绍
                            WAPCOrganintro=ap_org,      # 组织/个人介绍
                            WAPCvalid=1,
                            WAPCContact=apc_url,
            )  
            try:
                self.db.merge(new_companion)
                self.db.commit()
                add = self.db.query(WApCompanions).filter(WApCompanions.WAPCname == apc_title,
                                                          WApCompanions.WAPCServeintro == apc_content,
                                                          WApCompanions.WAPCContact == apc_url,
                                                          WApCompanions.WAPCvalid == 1).one()
                image = ImageHandler()
                image.insert_companion_image(apc_img, add.WAPCid)
                self.db.commit()
                self.retjson['code'] = '800050'
                self.retjson['contents'] = '约拍伴侣创建成功'
                    
            except Exception, e:
                    print e
                    self.retjson['code'] = '800051'
                    self.retjson['contents'] = '创建失败'

        elif type == '80006':    # 返回约拍伴侣
    
            retdata = []
            companions = self.db.query(WApCompanions).filter(WApCompanions.WAPCvalid == 1).all()
            model_handler = APmodelHandler()
            for item in companions:
                model_handler.ApCompanion(item, retdata)

            self.retjson['code'] = '800060'
            self.retjson['contents'] = retdata
            
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))







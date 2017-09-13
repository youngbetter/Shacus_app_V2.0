# -*- coding: utf-8 -*-
'''
@author:杨兴才
@模块功能：创建全局变量
'''

##所有const常量在此定义##
'''
#请求码为五位80000-89999状态码为六位#
#状态码为相应请求码后面再加一位      #
#请求码最后一位为奇数,状态码偶数     #
85001   创建动态，第一步，生成凭证
850010  生成凭证
850012  生成凭证成功
85002   创建动态，第二步，存储图片
850020  动态发表成功
850022  动态图片插入失败
850024  动态发表失败
850026  用户头像或昵称获取失败
85003   删除动态
850030  删除动态成功
850032  动态已经删除过
850034  此动态不存在
850000  用户验证失败

85011   请求刷新所有动态,上拉
850110  请求加载动态成功
850112  动态加载失败
85013   请求刷新所有动态，下拉
850130  请求刷新动态成功
850132  动态刷新失败
850150  动态，用户认证失败

85021   发布动态评论
850210  评论发表成功
850212  评论发表失败
850214  要评论的动态不存在或已删除
850216  要评论的动态不存在或已删除
85023   删除动态评论
850230  评论已删除过
850232  评论删除成功
850234  评论删除失败
850250  用户认证失败

85031   动态点赞
850310  点赞成功
850312  点赞新增失败
850314  已经点过赞
850316  点赞数据插入失败
85033   取消点赞
850330  没有点赞过
850332  取消点赞失败
850334  已经取消过点赞
850336  取消点赞成功
850300  用户验证失败

85041   发布问题，第一步，生成凭证
850410  生成凭证
850412  生成凭证失败
85042   发布问题，第二步，存储图片
850420  发布问题成功
850422  社区问题图片插入失败
850424  社区问题发表失败
850426  用户头像图片获取失败
85043   删除动态
850430  删除问题成功
850432  问题已经删除过
850434  此问题不存在
850400  用户验证失败

85051   问题刷新，下拉
850510  刷新成功
850512  问题刷新失败
85053   问题刷新，上拉
850530  加载成功
850532  问题加载失败
85055   请求刷新所收藏问题，下拉
850550  成功
850552  收藏问题刷新失败
85057   请求刷新所收藏问题，上拉
850570  成功
850572  收藏问题加载失败
85059   请求问题详情模型，包括问题和评论
850590  请求成功
850592  没评论时返回成功
850594  问题查找失败
850596  没评论时返回成功
850500  用户认证失败

85061   发布问题评论
850610  评论发表成功
850612  评论发表失败
850614  要评论的动态不存在或已删除
850616  要评论的动态不存在或已删除
85063   删除动态评论
850630  评论已删除过
850632  评论删除成功
850634  评论删除失败
850600  用户认证失败

85071   收藏问题
850710  创建收藏成功
850712  收藏失败
850714  要收藏的问题不存在或已删除
850716  要收藏的问题不存在或已删除
850718  曾收藏过
850720  重新收藏成功
85073   取消收藏
850730  取消收藏成功
850734  取消收藏失败
850700  用户认证失败

85081   创建作品集，第一步，，生产凭证
850810  生成凭证
850812  生成凭证失败
85082   创建作品集，第一步，，存储图片
850820  作品集发表成功
850822  作品集内容插入失败
850824  用户头像或昵称获取失败
850826  作品集图片插入失败
85083   删除作品集
850830  删除作品集成功
850832  作品集已经删除过
850834  此作品不存在
850800  用户验证失败

85091   点赞作品集
850910  点赞成功
850912  点赞新增失败
850914  已经点过赞
850916  点赞数据插入失败
85093   取消点赞
850930  取消点赞成功
850932  取消点赞失败
850934  已经取消过点赞
850936  没有点赞过
850900  用户验证失败

85101   请求刷新所有作品，下拉
851010  请求成功
851012  作品集刷新失败
85103   请求刷新所有作品集，上拉
851030  请求成功
851032  作品集加载失败
85105   请求个人照片
851050  请求成功
851052  个人照片加载失败
851000  用户认证失败
'''
class Const(object):
    FAVORITE_TYPE_TREND = 3
    FAVORITE_TYPE_QUESTION = 4
    FAVORITE_TYPE_COLLECT = 5
    COLLECT_TYPE_COLLECTION = 1
    COLLECT_TYPE_PRIVATEIMG = 0
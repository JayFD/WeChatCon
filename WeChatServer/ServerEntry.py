# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import receive
import reply
from UserHandler import UserHandler
from FileHandler import FileHandler
import traceback
from Operator import *

class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            #wechat authoticaiton
            signature = data.signature
            timestamp = data.timestamp

            nonce = data.nonce
            echostr = data.echostr
            token = "helloworld"
            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            #print "handle/GET func: hashcode {0}, signature : {1} ".format(hashcode, signature))
            print("handle/GET func: hashcode: {0}, signature: {1}".format(hashcode, signature))
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as Argument:
            return Argument

    def POST(self):
        try:
            webData = web.data()
            print("Handle Post webdata is {0}".format(webData))
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                cnstr = recMsg.Content.decode()

                #print(cnstr)
                action_str = cnstr[0:2]
                msg_str = cnstr[3:]

                func = OperationType.get_operate_function(OperationType.get_operate_type(action_str))
                if (func == OperationType.UnDefined):
                    content = "不能识别你的操作"
                else:
                    content = func(msg_str, recMsg.FromUserName)
            else:
                content = "暂且不处理"
                #return "success

            replyMsg = reply.TextMsg(toUser, fromUser, content)
            return replyMsg.send()

        except Exception as Argment:
            traceback.print_exc()
            return Argment

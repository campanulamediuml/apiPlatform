#coding=utf-8
import sys
sys.path.append('../')
import requests
from urllib.parse import quote
from wish import wish_common

class Ticket:

    def __init__(self):
        pass


    #ticket_id : 票证对象中的ID
    #检索票据
    def retrieve_ticket(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        ticket_id = quote(execute_command['ticket_id'])
        url = "https://merchant.wish.com/api/v2/ticket?access_token=%s&id=%s",(access_token,ticket_id)
        r = requests.post(url)
        result = r.text
        return result


    #列出所有等待你处理的票剧
    def retrieve_all_ticket_waiting(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        start = quote(execute_command['start'])
        limit = quote(execute_command['limit'])
        url = "https://merchant.wish.com/api/v2/ticket/get-action-required?access_token=%s&limit=%s&start=%s"%(access_token,limit,start)
        r = requests.post(url)
        result = r.text
        return result

    #票据回复
    def replay_to_ticket(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        reply = quote(execute_command['reply'])
        ticket_id = quote(execute_command['ticket_id'])
        url = "https://merchant.wish.com/api/v2/ticket/reply?access_token=%s&reply=%s&id=%s"%(access_token,reply,ticket_id)
        r = requests.post(url)
        result = r.text
        return result


    def close_ticket(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        ticket_id = quote(execute_command['ticket_id'])
        url = "https://merchant.wish.com/api/v2/ticket/close?access_token=%s&id=%s"%(access_token,ticket_id)
        r = requests.post(url)
        result = r.text
        return result


    def appeal_to_wish_support(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        ticket_id = quote(execute_command['ticket_id'])
        url = "https://merchant.wish.com/api/v2/ticket/appeal-to-wish-support?access_token=%s&id=%s"%(access_token,ticket_id)
        r = requests.post(url)
        result = r.text
        return result


    def reopen_ticket(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        ticket_id = quote(execute_command['ticket_id'])
        reply = quote(execute_command['reply'])
        url = "https://merchant.wish.com/api/v2/ticket/re-open?access_token=%s&id=%s&message=%s"%(access_token,ticket_id,reply)
        r = requests.post(url)
        result = r.text
        return result

        
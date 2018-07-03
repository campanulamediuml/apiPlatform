#coding=utf-8
import sys
sys.path.append('../')
import requests
from urllib.parse import quote
from wish import wish_common


class Notifications:

    def __init__(self):
        pass


    def fetch_notifications(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        limit = quote(execute_command['limit'])
        start = quote(execute_command['start'])
        url = "https://merchant.wish.com/api/v2/noti/fetch-unviewed?access_token=%s&limit=%s&start=%s"%(access_token,limit,start)
        r = requests.post(url)
        result = r.text
        return result


    def mark_as_viewed(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        noti_id = quote(execute_command['noti_id'])
        url = "https://merchant.wish.com/api/v2/noti/mark-as-viewed?access_token=%s&id=%s"%(access_token,noti_id)
        r = requests.post(url)
        result = r.text
        return result


    def count_unview_notifications(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        url = "https://merchant.wish.com/api/v2/noti/get-unviewed-count?access_token=%s&id=%s" % (access_token)
        r = requests.post(url)
        result = r.text
        return result



    def fetch_announcements(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        url = "https://merchant.wish.com/api/v2/fetch-bd-announcement?access_token=%s&id=%s" % (access_token)
        r = requests.post(url)
        result = r.text
        return result


    def fetch_system_update_notifications(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        url = "https://merchant.wish.com/api/v2/fetch-sys-updates-noti?access_token=%s&id=%s" % (access_token)
        r = requests.post(url)
        result = r.text
        return result


    def get_infractions_count(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        url = "https://merchant.wish.com/api/v2/count/infractions?access_token=%s&id=%s" % (access_token)
        r = requests.post(url)
        result = r.text
        return result


    def fetch_infractions(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        url = "https://merchant.wish.com/api/v2/get/infractions?access_token=%s&id=%s" % (access_token)
        r = requests.post(url)
        result = r.text
        return result
import requests
	def main():
        while 1:
            r = requests.get('http://localhost:9527/wish/refresh_token')
            if r.text = "refreshing"

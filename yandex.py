import requests



class YaDisk:
	base_url = 'https://cloud-api.yandex.net/'

	def __init__(self, token):
		self.token = token
		self.headers = {
			'Authorization': f'OAuth {self.token}'
		}

	def create_folder(self, folder):
		url = 'v1/disk/resources'
		full_url = self.base_url + url
		params = {
			'path': folder
		}
		response = requests.put(url=full_url, params=params, headers=self.headers).status_code
		return response

	def delete_folder(self, folder):
		url = 'v1/disk/resources'
		full_url = self.base_url + url
		params = {
			'path': folder
		}
		response = requests.delete(url=full_url, params=params, headers=self.headers).status_code
		return response

	def check_folder(self, folder):
		url = 'v1/disk/resources'
		full_url = self.base_url + url
		params = {
			'path': folder
		}
		response = requests.get(url=full_url, params=params, headers=self.headers).status_code
		return response


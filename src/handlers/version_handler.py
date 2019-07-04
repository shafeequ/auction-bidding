from base_handler import BaseRequestHandler


class AppVersionHandler(BaseRequestHandler):
	def get(self):
		self.write({"message": "success","code":20001, "version":"v1"})
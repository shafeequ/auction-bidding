import tornado.ioloop
import tornado.web
import json 
from app_constants import AppConstants, ResponseMessages
import simplejson
from datetime import date
import datetime 
from decimal import Decimal


class BaseRequestHandler(tornado.web.RequestHandler):

	def set_default_headers(self):
		"""Set the default response header to be JSON."""
		self.set_header("Content-Type", 'application/json; charset="utf-8"')

	def prepare(self):
		try:
			if self.request.body:
				self.request_context = json.loads(self.request.body)
		except:
			self.send_error_response(ResponseMessages.INVALID_JSON)

	def send_json_response(self, data, status=200):
		self.set_status(status)
		self.write(json.dumps(data, default=self.default_handler))
		self.finish()

	def send_error_response(self, data):
		response_http_code = data.get("code") // 100
		self.set_status(response_http_code)
		self.write(json.dumps(data, default=self.default_handler))
		self.finish()

	@classmethod
	def json_serial(cls, obj):

	    if isinstance(obj, decimal.Decimal):
	        return float(obj)

	    if isinstance(obj, (datetime, date)):
        	return obj.isoformat()

	    raise TypeError


	def default_handler(cls, o):

	    if type(o) is datetime.date or type(o) is datetime.datetime:
	        return o.isoformat()
	    if isinstance(o, Decimal) or type(o) is decimal.Decimal:
	        return float(o)




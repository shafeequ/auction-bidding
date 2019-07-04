from base_handler import BaseRequestHandler
from services.auctioner_items_service  import AuctionerItemsService
from app_constants import AppConstants, ResponseMessages
import time
from utils.helper import allowedRole

class AuctionerItemsHandler(BaseRequestHandler):
	""" This handler is all for the auctioner related operations CRUD of ITEMS """
	SUPPORTED_METHODS = ["GET", "POST"]

	@allowedRole('auctioner')
	def get(self):
		""" fetch all the items and display to the Auctioner"""
		items_list = AuctionerItemsService.get_all_items()
		self.send_json_response(items_list)

	@allowedRole('auctioner')
	def post(self):
		""" create the biddable item for the auctioner"""

		now = time.strftime('%Y-%m-%d %H-%M-%S')

		# validate the required fields 
		if not self.request_context.get("item_name") or not self.request_context.setdefault("item_bid_start_date",now) \
		or not self.request_context.get("item_desc") or not self.request_context.setdefault("item_bid_end_date",now) or not self.request_context.get("item_base_price"):
			self.send_error_response(ResponseMessages.INVALID_INPUT)

		# call the service to create it 
		item_code = AuctionerItemsService.create_item(self.request_context)
		self.send_json_response({"item_code_created":item_code}, status=AppConstants.HTTP_RESOURCE_CREATED)



from base_handler import BaseRequestHandler
from services.bidder_item_service  import BidderItemsService
from services.auctioner_items_service import AuctionerItemsService
from app_constants import AppConstants, ResponseMessages
import copy
from utils.helper import allowedRole


class BidderItemsHandler(BaseRequestHandler):
	""" This handler is all for the auctioner related operations CRUD of ITEMS """
	SUPPORTED_METHODS = ["GET", "POST"]

	@allowedRole('bidder')
	def get(self, own=None):
		""" fetch all the items and display to the Bidder """
		if own:
			own = self.user_id

		items_list = BidderItemsService.get_all_items(own=own)
		self.send_json_response(items_list)

	@allowedRole('bidder')
	def post(self, item_id=None):
		""" bidder bidding the price for the item"""

		# validate the required fields  

		# item code should be present 
		if not item_id:
			self.send_error_response(ResponseMessages.ITEM_CODE_MISSING)

			# item price should be there 
		if not self.request_context.get("item_bid_price"):
			self.send_error_response(ResponseMessages.ITEM_BID_PRICE_MISSING)

		if isinstance(self.request_context.get("item_bid_price"), basestring):
			self.send_error_response(ResponseMessages.ITEM_BID_PRICE_INVALID)


		if AuctionerItemsService.is_item_alreay_awarded(item_id):
			self.send_error_response(ResponseMessages.ITEM_ALREADY_AWARDED)

		# call the service to create it 
		# item_code = BidderItemsService.bid_item(self.request_context)

		# item bid price should be greater then the starting price  
		item_base_price = BidderItemsService.get_item_price(item_id)

		if float(self.request_context.get("item_bid_price")) <= float(item_base_price.get("bid_start_price")):
			response = ResponseMessages.ITEM_BID_PRICE_LESS_THAN_START_PRICE.copy()
			response.setdefault("bid_start_price", float(item_base_price.get("bid_start_price")))
			self.send_error_response(response)

		item_bid_from_user = {}

		item_bid_from_user.setdefault("user_id", self.user_id)
		item_bid_from_user.setdefault("item_id", item_id)
		item_bid_from_user.setdefault("item_bidder_price", float(self.request_context.get("item_bid_price")))

		item_code = BidderItemsService.bidder_item_add(item_bid_from_user)

		self.send_json_response({"message":" item_base_price = {} and your bid_price = {} recorded sucessfully".format(item_base_price.get("bid_start_price"),self.request_context.get("item_bid_price"))}, status=AppConstants.HTTP_RESOURCE_CREATED)



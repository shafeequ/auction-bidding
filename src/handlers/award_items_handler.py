from base_handler import BaseRequestHandler
from services.auctioner_items_service  import AuctionerItemsService
from app_constants import AppConstants, ResponseMessages
from utils.helper import allowedRole


class AuctionerItemsAwardHandler(BaseRequestHandler):
	"""this class is used to to provide the functios to Award the items to the bidder and list teh items awarded to the bidders """
	SUPPORTED_METHODS = ["GET", "PUT"]


	@allowedRole('auctioner')
	def get(self, item_id=None):
		users_bid_items = AuctionerItemsService.award_item_list(item_id=item_id)
		self.send_json_response(users_bid_items)

	@allowedRole('auctioner')
	def put(self, item_id=None):
		""" Award the Item to the closet bidder"""

		# validate the required fields  

		# item code should be present 
		if not item_id:
			self.send_error_response(ResponseMessages.ITEM_CODE_MISSING)

		item_code = AuctionerItemsService.award_item(item_id)

		self.send_json_response({"item_code": item_code})

class AppConstants:
	LOG_CONFIG_FILE = "auction_bidding.conf"
	DEBUG = True
	HTTP_RESOURCE_CREATED = 201
	USERS_LIST = {}
	ROLES = {  "auctioner" : 1, "bidder" : 2 }




class ResponseMessages:
	# all response message from the application , we can even use for localization 

	# 2XX Messages 
	SUCCESS_MESSAGE = {"message":"success", "code": 20001}
	NO_DATA = {"message":"No Data", "code": 20002}


	 # 400 Messages
	INVALID_INPUT = {"message":"some of the required Input Parameter Missing/Empty", "code": 40001}
	ITEM_BID_PRICE_MISSING = {"message":"item_base_price is not provided", "code": 40002}
	ITEM_BID_PRICE_INVALID = {"reason": "item_base_price is not valid", "code": 40003}
	ITEM_CODE_MISSING = {"message":"item code in the URL is not provided", "code": 40004}
	ITEM_BID_PRICE_LESS_THAN_START_PRICE = {"reason": "item_base_price should be greater than the starting price", "code": 40003}
	ITEM_ALREADY_AWARDED = {"message":"Iteam already Sold/Awarded", "code": 40004}

	# Auth Related Erroes

	AUTH_HEADER_NOT_FOUND = {"message":" Auth Header Not Found", "code": 40101}
	INVALID_USER = {"message":" User Unknown", "code": 40102}
	USER_OPR_NOT_PERMITTED = {"message":" You are not authorized to perform this operation", "code": 40102}

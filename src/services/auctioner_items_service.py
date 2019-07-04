from models.base_model import SimpleMysql, MyTables
from app_constants import ResponseMessages


class AuctionerItemsService:

	db = SimpleMysql() 

	@classmethod
	def get_all_items(cls):
		items_list = cls.db.getAll(MyTables.TBL_ITEMS,
		["item_id", "item_name","item_desc","item_base_price"]
		)

		return items_list


	@classmethod
	def create_item(cls, data):
		items_list = cls.db.insert(MyTables.TBL_ITEMS,
		data
		) 
		cls.db.commit()
		item_code  = cls.db.lastId()
		return item_code


	@classmethod
	def award_item(cls, item_id):
		""" Award the item to the closest bidder
		if only one bidder assign it to him
		if two bidder with the same price assign it to the first bidder
		if no bidder just return the info tot he auctioner  
		"""

		if cls.is_item_alreay_awarded(item_id):
			return ResponseMessages.ITEM_ALREADY_AWARDED

		sql = "SELECT p1.user_id, p1.item_id, item_bidder_price FROM {} p1 WHERE item_bid_date = (SELECT MAX(p2.item_bid_date) FROM items_bidded p2 WHERE p1.user_id = p2.user_id and p2.item_id={}) ORDER BY item_bidder_price asc, item_bid_date asc  limit 1; ".format(MyTables.TBL_ITEMS_BIDDED, item_id) 
		awarded_bidder = cls.db.query(sql) 
		winner =  awarded_bidder.fetchone()
		if winner:
			winner_details = cls.get_user(winner[0])
			awardee ={}
			awardee ["user_id"] = winner[0]
			awardee ["item_id"] = winner[1]
			awardee ["item_sold_price"] = winner[2]

			items_list = cls.db.insert(MyTables.TBL_ITEMS_AWARDED,awardee)
			cls.db.commit()

			awardee["user_name"] = winner_details["user_name"]
			awardee["user_email"] = winner_details["user_email"]
			return awardee

		else:
			return {"message":"No Bidder Available for awarding the item"}
		


	@classmethod
	def get_user(cls, user_id):
		user_info  = cls.db.getOne(MyTables.TBL_USERS,
		["user_name", "user_email"], ["id = {}".format(user_id)]
		)
		if user_info:
			return user_info
		else:
			return {}




	@classmethod
	def get_item(cls, item_id):
		item_info  = cls.db.getOne(MyTables.TBL_ITEMS,
		["item_name", "item_desc", "item_base_price"], ["item_id = {}".format(item_id)]
		)
		if item_info:
			return item_info
		else:
			return {}

#
	@classmethod
	def is_item_alreay_awarded(cls, item_id):
		rec_exists  = cls.db.getOne(MyTables.TBL_ITEMS_AWARDED,
		["user_id"], ["item_id = {}".format(item_id)]
		)
		if rec_exists:
			return True
		return False


	@classmethod
	def award_item_list(cls, item_id=None):
		if item_id:
			rec_list  = cls.db.getAll(MyTables.TBL_ITEMS_AWARDED,["user_id","item_sold_price","item_id"], ["item_id = {}".format(item_id)])
		else:
			rec_list  = cls.db.getAll(MyTables.TBL_ITEMS_AWARDED, ["user_id","item_sold_price","item_id"])

		winners_list = []
		for rec in rec_list:
			user_info = cls.get_user(rec["user_id"])
			item_info = cls.get_item(rec["item_id"])
			user_info.update(item_info)
			user_info.update(rec)
			# user_info.update({"item_sold_price": rec_list["item_sold_price"]})
			winners_list.append(user_info)

		return winners_list







				
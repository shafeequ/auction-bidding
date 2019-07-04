from models.base_model import SimpleMysql, MyTables
import tornado
from app_constants import ResponseMessages
import time

class BidderItemsService:

	db = SimpleMysql() 

	@classmethod
	def get_all_items(cls, own=None):
		exclude_list = cls.awarded_item_list_ids(own=own)
		exclude_list = ', '.join(str(x) for x in exclude_list)

		# if not exclude_list:
		# 	return ResponseMessages.NO_DATA

		if exclude_list:
			if own:
				cond = ("item_id in ({})".format(exclude_list),[])
			else:
				cond=("item_id not in ({})".format(exclude_list),[])
		else:
			cond = ()

		items_list = cls.db.getAll(MyTables.TBL_ITEMS,
		["item_id as item_code ", "item_name","item_desc","item_base_price as bid_start_price"], cond
		)

		return items_list


	@classmethod
	def bidder_item_add(cls, data):
		items_list = cls.db.insert(MyTables.TBL_ITEMS_BIDDED,
		data
		) 
		cls.db.commit()

		item_code  = cls.db.lastId()
		return item_code

		
	@classmethod
	def get_item_price(cls, item_id):
		items_price = cls.db.getOne(MyTables.TBL_ITEMS,["item_base_price as bid_start_price"], ("item_id=%s",[item_id])) 
		return items_price

	@classmethod
	def awarded_item_list_ids(cls, own=None):
		cond =()
		if own:
			cond = ("user_id = {}".format(own), [])
		rec_list  = cls.db.getAll(MyTables.TBL_ITEMS_AWARDED, ["item_id"], cond)

		item_id_list = []
		for rec in rec_list:
			item_id_list.append(rec["item_id"])
		return item_id_list
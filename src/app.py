import os
SRC_PATH =  os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sys
sys.path.insert(0,SRC_PATH)
import logging
import tornado
import tornado.ioloop
import tornado.web
from app_constants import AppConstants
from handlers.version_handler import AppVersionHandler
import logging.config
from tornado.httpclient import AsyncHTTPClient
import time, signal
from tornado import web, ioloop, options, httpserver
from tornado.options import parse_command_line, define, options
from handlers.auctioner_handler import AuctionerItemsHandler
from handlers.award_items_handler import AuctionerItemsAwardHandler
from handlers.bidder_handler import BidderItemsHandler
from models.base_model import SimpleMysql, MyTables

application = tornado.web.Application([
        (r'/auction-bidding/v1/?', AppVersionHandler),   # this is just to see what cloud version of the application is running ( as we keep going we need to be backward compatible)
        (r'/auctioner/v1/items/?', AuctionerItemsHandler),    # Auctioner will CRUD the list of  items
        (r'/bidder/v1/items/available/?(?P<own>\w+)?', BidderItemsHandler),      # list  all the of the biddable items to the bidders
        (r'/bidder/v1/items/(?P<item_id>\w+)', BidderItemsHandler),     # bid the item
        (r'/auctioner/v1/items/award/?(?P<item_id>\w+)?', AuctionerItemsAwardHandler), # Auctioner award one item at a time
    ], debug=AppConstants.DEBUG)

import signal
def sig_exit(signum, frame):
    tornado.ioloop.IOLoop.instance().add_callback_from_signal(do_stop)

def do_stop(signum, frame):
    tornado.ioloop.IOLoop.instance().stop()

if __name__ == "__main__":
    define("port", default=8082)
    parse_command_line()
    # Overwrite the options logging level with the log config file
    logging.config.fileConfig(AppConstants.LOG_CONFIG_FILE)

    application.listen(options.port)
    # this should not be done in production, this is used for only demoing KI connect the validate  bidder-auctioner can do the transation on this system
    db = SimpleMysql() 
    users = db.leftJoin(tables=(MyTables.TBL_USERS, MyTables.TBL_USER_ROLES), fields=(["id","user_email"], ["user_id","user_role"]), join_fields=("id","user_id"))
    for user in users:
        AppConstants.USERS_LIST.setdefault(user.user_email, {"role":user.user_role, "id": user.id})

    tornado.ioloop.IOLoop.instance().start()
    signal.signal(signal.SIGINT, sig_exit)



from models.base_model import SimpleMysql, MyTables
db = SimpleMysql()  

print db , db1

print db.getAll(MyTables.TBL_ITEMS,
        ["item_id", "item_name"]
    )
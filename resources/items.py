from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import request
from models.item import ItemModel
from models.store import StoreModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field cannot blank")
    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="This field cannot blank")

    @jwt_required()
    def get(self, name):
        item = ItemModel.get_item_by_name(name.lower())
        if item:
            return {"item":item.json()}, 200
        return {"item": "Item {} not found".format(name)}, 404

    @jwt_required()
    def post(self, name):
        result = ItemModel.get_item_by_name(name.lower())
        if result:
            return {"message": "'{}' is present in DB".format(name)}, 400
        data = request.get_json()
        store_obj = StoreModel.get_store_by_name(data['store'].lower())
        if not store_obj:
            return {"message": "'{}' Store not  present in DB, Please create a new store".format(data['store'])}, 400
        item_obj = ItemModel(name.lower(), data["price"], store_obj.id)
        try:
            item_obj.save_to_db()
        except:
            return {"Message": "Error is occurred during insertion time"}, 500
        return {"message": "'{}' is inserted in DB".format(name)}, 201

    @jwt_required()
    def delete(self, name):
        result = ItemModel.get_item_by_name(name.lower())
        if not result:
            return {"message": "'{}' is not present in DB".format(name)}, 400
        result.delete_from_db()
        return {"message": "{} is deleted from DB".format(name)}

    @jwt_required()
    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()
        item = ItemModel.get_item_by_name(name.lower())
        if not item:
            item = ItemModel(name.lower(), **data)
        else:
            item.price = data["price"]
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        item_li = []
        items = ItemModel.get_all_items()
        if not items:
            return {"message": "Items List is not available in DB"}
        for rec in items:
            item_li.append(rec.json())
        return {"items": item_li}
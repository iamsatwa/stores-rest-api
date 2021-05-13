from flask_restful import Resource
from models.store import StoreModel
from flask_jwt import jwt_required


class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.get_store_by_name(name)
        if store:
            return store.json()
        return {"message": "store {} is not found in db".format(name)}, 404

    @jwt_required()
    def post(self, name):
        store = StoreModel.get_store_by_name(name)
        if store:
            return {"message": "store {} is found in db".format(name)}, 400
        store_obj = StoreModel(name)
        try:
            store_obj.save_to_db()
        except:
            return {"message": "Error occurred, while creating a store"}, 500
        return {"message": "store {} has been  created".format(name)}, 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.get_store_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": "{} is deleted from DB".format(name)}, 201
        return {"message": "'{}' is not present in DB".format(name)}, 400


class StoreList(Resource):
    @jwt_required()
    def get(self):
        """
        store.json() method call json() method in models/store.py
        Example:
            (Pdb) stores
            [<StoreModel 1>, <StoreModel 1>]
            (Pdb) stores[0]
            <StoreModel 1>
            (Pdb) stores[0].name
            'bike'
            (Pdb) stores[0].item
            [<ItemModel 1>, <ItemModel 2>, <ItemModel 3>, <ItemModel 7>]
            (Pdb) stores[0].item[0].name
            'Bajaj'
            (Pdb) stores[0].item[0].price
            1555.5
        """
        stores = StoreModel.get_all_stores()
        return {"stores": [store.json() for store in stores]}

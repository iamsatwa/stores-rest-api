from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))
    item = db.relationship("ItemModel")

    def __init__(self, name):
        self.name = name

    def json(self):
        """
        item.json() call json() method in models/item.py
        Example:
            (Pdb) store.name
            'bike'
            (Pdb) store.item
            [<ItemModel 1>, <ItemModel 2>, <ItemModel 3>, <ItemModel 7>]
            (Pdb) store.item[0].name
            'Bajaj'
            (Pdb) store.item[0].price
            1555.5
        """
        return {"name": self.name,
                "items": [item.json() for item in self.item]}  # self.name==storeObj.name and self.item==storeObj.item

    @classmethod
    def get_store_by_name(cls, name):

        return StoreModel.query.filter_by(name=name).first()  # select * from items where name=name limit 1;

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_stores(cls):
        return StoreModel.query.all()

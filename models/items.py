from api_v4.db import db


class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Integer)

    def json(self):
        return {"name": self.name, "price": self.price}

    @staticmethod
    def find_by_name(name):
        return ItemModel.query.filter_by(name=name).first()

    def add_item(self):
        db.session.add(self)
        db.session.commit()

    def delete_item(self):
        db.session.delete(self)
        db.commit()

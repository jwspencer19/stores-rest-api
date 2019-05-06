from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# Notes:
# parameter to get_json()
# force=True - will allow posts that do not have the content-type header set to application/json.
#  This is a bit dangerous
# silent=True - will not return an error just None if no json payload or incorrect json format


# class Item inherits from class Resource
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                       )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every items needs a store id"
                       )

    # we will have to authenticate before being able to call get
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])
        # item = ItemModel(**data)
        # item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500    # 500, Internal Server Errot

        return item.json(), 201

    def delete(self, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "DELETE from items WHERE name=?"
        # cursor.execute(query, (name,))
        #
        # connection.commit()
        # connection.close()
        # return {'message': 'Item deleted'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    # put is idempotent. can be used to create or update items
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data['price'])

        if item is None:
            # item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        #
        # items = []
        # for row in result:
        #     items.append({'name': row[1], 'price': row[2]})
        #
        # connection.close()
        #
        # return {'items': items}

        # using lambda function
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        # -or- using list comprehension
        return {'items': [item.json() for item in ItemModel.query.all()]}

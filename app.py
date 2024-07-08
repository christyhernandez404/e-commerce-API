from flask import Flask,jsonify, request
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_marshmallow import Marshmallow
from datetime import date
from typing import List
from marshmallow import ValidationError, fields
from sqlalchemy import select, delete

app = Flask(__name__) # creating an instance of the Flask class for our app to use


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Tomatillo4!@127.0.0.1/ecom'


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app, model_class=Base)
ma = Marshmallow(app)

#these are the models to create tables in my db
class Customer(Base):
    __tablename__ = "customer" 

    #mapping our class attributes to our table column
    id:Mapped[int] = mapped_column(primary_key=True)
    customer_name:Mapped[str] = mapped_column(db.String(75),nullable=False)
    email:Mapped[str] = mapped_column(db.String(150))
    phone: Mapped[str] = mapped_column(db.String(15))

    orders: Mapped[List["Orders"]] = db.relationship(back_populates='customer')

order_products = db.Table(
    "order_products",
    Base.metadata, # allow this table to locate the foreign keys from the Base class
    db.Column('order_id', db.ForeignKey('orders.id'), primary_key= True),
    db.Column('product_id', db.ForeignKey('products.id'), primary_key= True)
)

class Orders(Base):
    __tablename__ = "orders" 

    id:Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[date] = mapped_column(db.Date, nullable= False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customer.id'))

    # create our many-one relationship to the customer table
    customer: Mapped['Customer'] = db.relationship(back_populates='orders')
    # create a many-many relationship to Products through our association table order_products
    products: Mapped[List['Products']] = db.relationship(secondary=order_products)

class Products(Base):
    __tablename__ = 'products'
    id:Mapped[int] = mapped_column(primary_key=True)
    product_name:Mapped[str] = mapped_column(db.String(255),nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)


class CustomerAccount(Base):
    __tablename__ = 'customer_account'
    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(db.String(250),nullable=False)
    password:Mapped[str] = mapped_column(db.String(250),nullable=False)

# with app.app_context():
#     db.drop_all()
#     db.create_all()

#================= Marshmallow Data Validation Schema =========================#
# Define schema to validate customer data
class CustomerSchema(ma.Schema):
    id = fields.Integer(required= False)
    customer_name = fields.String(required= True)
    email = fields.String()
    phone = fields.String()

    class Meta:
        fields = ('id', 'customer_name', 'email', 'phone')


class CustomerAccountSchema(ma.Schema):
    id = fields.Integer(required= False)
    username = fields.String(required= True)
    password = fields.String(required= True)

    class Meta:
        fields = ('id', 'username','password')

class OrderSchema(ma.Schema):
    id = fields.Integer(required= False)
    order_date = fields.Date(required= False)
    customer_id = fields.Integer(required= True)

    class Meta:
        fields = ('id', 'order_date', 'customer_id', 'items') # items will be a list of product id's associated with an order

class ProductSchema(ma.Schema):
    id = fields.Integer(required= False)
    product_name = fields.String(required= True)
    price = fields.Float(required= True)

    class Meta:
        fields = ('id', 'product_name', 'price')

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many= True)

customer_account_schema = CustomerAccountSchema()
customer_accounts_schema = CustomerAccountSchema(many= True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many= True)

product_schema = ProductSchema()
products_schema = ProductSchema(many= True)

#=================CRUD for Customer=================================#

@app.route("/customers/<int:id>", methods=["GET"])
def get_customer(id):
    query = select(Customer).where(Customer.id ==id)
    result = db.session.execute(query).scalars().first()

    if result is None:
        return jsonify({'Error':'Customer not found!'}),404
    
    return customer_schema.jsonify(result)

# create customers with a POST request
@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify({e.messages}), 400

    new_customer = Customer(customer_name= customer_data['customer_name'], email= customer_data['email'], phone= customer_data['phone'])
    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"Message": "New customer added successfully!"}), 201

# Update a user with a PUT request
@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):

    query = select(Customer).where(Customer.id == id)
    result = db.session.execute(query).scalar()
    if result is None:
        return jsonify({"Error": "Customer not found"}), 404
    
    customer = result
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in customer_data.items():
        setattr(customer, field, value)

    db.session.commit()
    return jsonify({"Message": "Customer details have been updated!"})

@app.route('/customers/<int:id>',methods=['DELETE'])
def delete_customer(id):
    query = delete(Customer).where(Customer.id == id)
    result = db.session.execute(query)

    if result.rowcount == 0:
        return jsonify({'Error': "Customer not found"})
    
    db.session.commit()
    return jsonify({"Message":"Customer successfully deleted!"})

#===============CRUD for Customer Account==========#

@app.route('/customeraccount/<int:id>', methods=['GET'])
def get_customer_account(id):
    query = select(CustomerAccount).where(CustomerAccount.id == id)
    result = db.session.execute(query).scalars().first()

    if result is None:
        return jsonify({'Error': "Customer Account not found!"}), 404
    
    return customer_account_schema.jsonify(result)


@app.route('/customeraccount', methods=['POST'])
def add_customer_account():
    try:
        customer_account_data = customer_account_schema.load(request.json)
    except ValidationError as e:
        return jsonify({e.messages}), 400

    new_customer_account = CustomerAccount(username= customer_account_data['username'], password= customer_account_data['password'])
    db.session.add(new_customer_account)
    db.session.commit()

    return jsonify({"Message": "New customer account added successfully!"}), 201

@app.route('/customeraccount/<int:id>', methods=['PUT'])
def update_customer_account(id):

    query = select(CustomerAccount).where(CustomerAccount.id == id)
    result = db.session.execute(query).scalar()
    if result is None:
        return jsonify({"Error": "Customer Account not found"}), 404
    
    customer_account = result
    try:
        customer_account_data = customer_account_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in customer_account_data.items():
        setattr(customer_account, field, value)

    db.session.commit()
    return jsonify({"Message": "Customer account details have been updated!"})

@app.route('/customeraccount/<int:id>', methods=['DELETE'])
def delete_customer_account(id):
    query = delete(CustomerAccount).where(CustomerAccount.id == id) 

    result = db.session.execute(query)

    if result.rowcount == 0:
        return jsonify({"Error": "Customer not found"})
    
    db.session.commit()
    return jsonify({"Message": "Customer Account successfully deleted!"}), 200

#===============CRUD for Product==========#

# get all products
@app.route("/products", methods= ['GET'])
def get_all_products():
    query = select(Products) 
    result = db.session.execute(query).scalars() 
    products = result.all() 

    return products_schema.jsonify(products)

# get a single product
@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    query = select(Products).where(Products.id == id)
    result = db.session.execute(query).scalar()

    if result is None:
        return jsonify({'Error': "Product not found!"}), 404
    
    return product_schema.jsonify(result)

# add a product
@app.route('/products', methods=['POST'])
def add_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_product = Products(product_name= product_data['product_name'], price= product_data['price'])
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"Message": "New product successfully added!"}), 201

#update a product
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):

    query = select(Products).where(Products.id == id)
    result = db.session.execute(query).scalar()
    if result is None:
        return jsonify({"Error": "Product not found"}), 404
    
    product = result
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in product_data.items():
        setattr(product, field, value)

    db.session.commit()
    return jsonify({"Message": "Product details have been updated!"})

#delete a product
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    query = delete(Products).where(Products.id == id) 

    result = db.session.execute(query)

    if result.rowcount == 0:
        return jsonify({"Error": "Product not found"})
    
    db.session.commit()
    return jsonify({"Message": "Product successfully deleted!"}), 200

#===============CRUD for Order Interactions==========#
# place a new order
@app.route('/orders', methods=['POST'])
def add_order():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_order = Orders(order_date= date.today(), customer_id= order_data['customer_id'])

    for item_id in order_data['items']:
        query = select(Products).where(Products.id == item_id)
        item = db.session.execute(query).scalar()
        new_order.products.append(item) 

    db.session.add(new_order)
    db.session.commit()
    return jsonify({"Message": "New order placed!"}), 201

# Get items in an order by order id with GET
@app.route("/order_items/<int:id>", methods=['GET'])
def order_items(id):
    query = select(Orders).filter(Orders.id == id)
    order = db.session.execute(query).scalar()

    return products_schema.jsonify(order.products)


if __name__ == "__main__":
    app.run(debug=True)


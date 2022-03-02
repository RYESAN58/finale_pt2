from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Car:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.model = db_data['model']
        self.make = db_data['make']
        self.price = db_data['price']
        self.description = db_data['description']
        self.User_id = db_data['User_id']
        self.year = db_data['year']



    #Create instance of data
    @classmethod
    def create(cls, data):
        query = "INSERT INTO `drive`.`cars` (`model`, `make`, `price`, `description`, `User_id`, `year`) VALUES (%(model)s, %(make)s, %(price)s, %(description)s, %(User_id)s, %(year)s);"
        return connectToMySQL("drive").query_db(query,data)


    #retrieve all the data
    @classmethod
    def retrieve(cls):
        query = 'SELECT * FROM cars'
        which = connectToMySQL('drive').query_db(query)
        descriptions = []
        for i in which:
            descriptions.append(cls(i))
        return descriptions


    #retriever all specific data
    @classmethod
    def retrieve_by(cls, data):
        query = "SELECT * FROM cars WHERE id = %(id)s"
        return connectToMySQL('drive').query_db(query, data)


    #update data
    @classmethod
    def update(cls, data):
        query = "UPDATE `drive`.`cars` SET `model` = %(model)s, `make` = %(make)s, `price` = %(make)s, `description` = %(description)s, `year` = %(year)s WHERE (`id` = %(id)s);"
        return connectToMySQL('drive').query_db(query, data)


    #delete row 
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM `drive`.`cars` WHERE (`id` = %(id)s);"
        return connectToMySQL('drive').query_db(query, data)


    @staticmethod
    def validate(user):
        is_valid = True
        if len(user['model']) < 1:
            flash("model requiered")
            is_valid = False
        if len(user['make']) < 1:
            flash("Must have a make")
            is_valid = False
        if len(user['price']) < 1:
            flash("Must have a price")
            is_valid = False
        if len(user['description']) < 1 :
            flash("Must type something in description")
            is_valid = False
        return is_valid


    @classmethod
    def get_all_cars( cls):
        query = "select a.model, a.year,a.id as carnum,b.id as user, concat(b.firstname, ' ', b.lastname) as seller from cars a join user b on a.user_id = b.id"
        print(query)
        return connectToMySQL('drive').query_db(query)
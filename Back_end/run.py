import sqlite3
import flask
from flask import request
import pandas as pd
import datetime
import random
from flask_restplus import Resource, Api
from flask_restplus import reqparse
from pandas.io import sql
import numpy as np
import re
import os
import ast
import collections

my_db = 'ISSE.db'
# initialization
app = flask.Flask(__name__)
api = Api(app, default='general_user', version='3.7', title='ISSE APIs',
          description='Final version of ISSE API',
          default_label='APIs for general users')

c_api = api.namespace('category', description='APIs for categories')
i_api = api.namespace('ingredient', description='APIs for ingredient')
u_api = api.namespace('update', description='APIs for updating items in database')
r_api = api.namespace('recipe', description='APIs for recipes')

parser = reqparse.RequestParser()
parser.add_argument('email', type=str, location='args')
parser.add_argument('password', type=str, location='args')
parser.add_argument('username', type=str, location='args')
parser.add_argument('id', type=str, location='args')
parser.add_argument('meal_Type', type=str, location='args')
parser.add_argument('Ingredients', type=str, location='args')

parser.add_argument('i_name', type=str, location='args')
parser.add_argument('c_name', type=str, location='args')


# used to modify or create database
def database_controller(db_name, cmd):
    # Connect to db
    connection = sqlite3.connect(db_name)
    cur = connection.cursor()

    # execute command
    cur.execute(cmd)
    result = cur.fetchall()

    # close connection and cursor
    connection.commit()
    cur.close()
    connection.close()

    return result


# read sql and convert it in the format of dictionary
def read_sql(db_name, cmd):
    conn = sqlite3.connect(db_name)
    results = sql.read_sql(cmd, conn)
    results = results.to_dict("records")
    return results


# initial database when DB not exist
def initial_db(db):
    database_controller(db,
                        'CREATE TABLE "Users" ('
                        '"id"	INTEGER NOT NULL UNIQUE,'
                        '"username"	TEXT NOT NULL,'
                        '"password"	TEXT NOT NULL,'
                        '"list_id"	INTEGER NOT NULL UNIQUE,'
                        '"email"	INTEGER NOT NULL UNIQUE,'
                        'PRIMARY KEY("id")'
                        ');'
                        )
    database_controller(db,
                        'CREATE TABLE "Recipes" ('
                        '"id"	INTEGER NOT NULL UNIQUE,'
                        '"name"	TEXT NOT NULL,'
                        '"img"	TEXT,'
                        '"description"	TEXT,'
                        '"time"	INTEGER,'
                        '"serves"	INTEGER,'
                        '"author"	TEXT NOT NULL,'
                        '"list_id"	INTEGER NOT NULL UNIQUE,'
                        '"steps"	TEXT NOT NULL,'
                        '"tags"	TEXT,'
                        '"type"	TEXT NOT NULL,'
                        '"rating"	INTEGER,'
                        'PRIMARY KEY("id")'
                        ');'
                        )

    database_controller(db,
                        'CREATE TABLE "Recipe_list" ('
                        '"u_id"	INTEGER NOT NULL,'
                        '"recipe_id"	INTEGER NOT NULL UNIQUE'
                        ');'
                        )

    database_controller(db,
                        'CREATE TABLE "Ingredient_list" ('
                        '"recipe_id"	INTEGER NOT NULL,'
                        '"ingredient_id"	INTEGER NOT NULL'
                        ');'
                        )

    database_controller(db,
                        'CREATE TABLE "Ingredients" ('
                        '"id"	INTEGER NOT NULL UNIQUE,'
                        '"name"	TEXT NOT NULL,'
                        '"c_id"	INTEGER NOT NULL,'
                        '"Img_address"	TEXT,'
                        'PRIMARY KEY("id")'
                        ');'
                        )

    database_controller(db,
                        'CREATE TABLE "Categories" ('
                        '"category_name"	TEXT NOT NULL UNIQUE,'
                        '"id"	INTEGER NOT NULL UNIQUE,'
                        'PRIMARY KEY("id")'
                        ');'
                        )


def get_current_id(name):
    cmd = "SELECT max(id) FROM {}".format(name)
    id = read_sql(my_db, cmd)
    if id[0]['max(id)'] is None:
        id = 1
    else:
        id = id[0]['max(id)'] + 1
    return id


# the function allows developer to obtain argument from front end and API page
def get_argu(argu):
    parser.add_argument(argu, type=str, location='args')
    temp = request.form.get(argu)
    if not temp:
        temp = parser.parse_args()[argu]
    return temp


if os.path.exists(my_db):
    # os.remove(my_db)
    print(my_db, "already exists")
else:
    print("Creating Database")
    initial_db(my_db)


@api.route("/login")
@api.response(200, 'OK')
@api.response(201, 'Created')
@api.response(400, 'Validation Error')
@api.response(404, 'Not Found')
class Login(Resource):
    @api.doc(params={"email": 'Email_address', 'password': 'Password'})
    def get(self):
        """
        Login
        """

        email = parser.parse_args()['email']
        password_input = parser.parse_args()['password']

        # validate email address
        cmd = "SELECT * FROM Users WHERE email='{}'".format(email)
        users = read_sql(my_db, cmd)
        if not users:
            return {
                       "message": "User not exist"
                   }, 404

        password = users[0]['password']
        id = users[0]['id']
        if password_input == password:
            return {
                       "message": "Login successful",
                       "id": id
                   }, 200
        else:
            return {
                       "message": "invalid user"
                   }, 400


@api.route("/save_changes")
@api.response(200, 'OK')
@api.response(201, 'Created')
@api.response(400, 'Validation Error')
@api.response(404, 'Not Found')
class Save_changes(Resource):
    @api.doc(params={"id": 'user_id', 'password': 'Password', 'email': "email address", 'username': "username"})
    def post(self):
        """
        For updating information of users
        """
        id = get_argu('id')
        email = get_argu('email')
        username = get_argu('username')
        password = get_argu('password')
        if not email or not username or not password:
            return {
                       "message": "invalid input"
                   }, 500
        cmd = "DELETE FROM Users WHERE id = '{}'".format(id)
        database_controller(my_db, cmd)
        database_controller(my_db,
                            "INSERT INTO Users(id, username, password, list_id, email) Values ('{}', "
                            "'{}', '{}', '{}', '{}')".format(id, username, password, id, email))

        cmd = "Select p.id FROM Recipes p Join Recipe_list r on p.id = r.recipe_id Join Users u on " \
              "r.u_id = u.list_id Where u.id = '{}'".format(id)
        temp = read_sql(my_db, cmd)
        id_list = [i['id'] for i in temp]
        for id in id_list:
            cmd = "UPDATE Recipes SET author = '{}'  WHERE id = {}".format(username, id)
            database_controller(my_db, cmd)

        return {
                   "message": "updated"
               }, 201


@api.route("/recommend_friend")
@api.response(200, 'OK')
@api.response(201, 'Created')
@api.response(400, 'Validation Error')
@api.response(404, 'Not Found')
class Friend(Resource):
    @api.doc(params={"id": 'user_id'})
    def get(self):
        """
        Recommend friend to user according to the recipes they created
        """
        """
        Select current user's recipes and count many ingredients they've used
        """
        u_id_ = int(get_argu('id'))
        cmd = 'Select name from Recipe_list r Join Ingredient_list i On i.recipe_id = r.recipe_id Join ' \
              'Ingredients s on s.id = i.ingredient_id Where r.u_id = {}'.format(u_id_)
        temp = read_sql(my_db, cmd)
        temp = [i['name'] for i in temp]
        temp = {x: temp.count(x) for x in temp}
        temp = sorted(temp.items(), key=lambda kv: kv[1], reverse=True)
        # user_ingredient.key()---> the ingredient name; user_ingredient.value()---> The number of times each
        # ingredient is used
        user_ingredient = {}
        for i in range(len(temp)):
            user_ingredient[str(temp[i][0])] = temp[i][1]

        ingre_list = [i for i in user_ingredient]

        """
        Go through all users who created recipes before, do the same thing as above
        """
        cmd = "Select Distinct u_id From Recipe_list"
        result = read_sql(my_db, cmd)
        scores = {}
        user_id = [i['u_id'] for i in result]
        if u_id_ in user_id:
            user_id.remove(u_id_)
            # random choose 4 users with recipes, the number can be increased when we have more users
            if len(user_id) > 3:
                user_id = random.sample(user_id, 4)

            for id in user_id:
                scores[id] = 0
            for id in user_id:
                cmd = 'Select name from Recipe_list r Join Ingredient_list i On i.recipe_id = r.recipe_id Join ' \
                      'Ingredients s on s.id = i.ingredient_id Where r.u_id = {}'.format(id)
                temp = read_sql(my_db, cmd)
                temp = [i['name'] for i in temp]
                temp = {x: temp.count(x) for x in temp}
                temp = sorted(temp.items(), key=lambda kv: kv[1], reverse=True)
                friend = {}
                for i in range(len(temp)):
                    friend[str(temp[i][0])] = temp[i][1]

                for i in friend.keys():
                    if i in ingre_list:
                        scores[id] = user_ingredient[i] + friend[i] + scores[id]

            """
            scores are the evidence we used to test whether users have similar flavor
            """
            scores = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
            scores = scores[:3]
            id = []
            for i in range(0, 3):
                id.append(scores[i][0])

            final_result = []
            for i in id:
                cmd = "SELECT username, email From Users where id = {}".format(i)
                result = read_sql(my_db, cmd)
                result[0]['user_id'] = i
                final_result.append(result[0])

            return final_result, 200
        else:
            # if user has not created any recipes, recommend friend randomly.
            cmd = "Select Distinct u_id From Recipe_list"
            result = read_sql(my_db, cmd)
            user_id = [i['u_id'] for i in result]
            user_id = random.sample(user_id, 3)
            final_result = []
            for i in user_id:
                cmd = "SELECT username, email From Users where id = {}".format(i)
                result = read_sql(my_db, cmd)
                result[0]['user_id'] = i
                final_result.append(result[0])

            return final_result, 200


@api.route("/get_user_name")
@api.response(200, 'OK')
@api.response(201, 'Created')
@api.response(400, 'Validation Error')
@api.response(404, 'Not Found')
class User_name(Resource):
    @api.doc(params={"id": 'user_id'})
    def get(self):
        id = parser.parse_args()['id']
        cmd = "Select username from Users where id = '{}'".format(id)
        result = read_sql(my_db, cmd)
        if len(result) == 0:
            pass
        return result[0]['username'], 200


@api.route("/get_user_info")
@api.response(200, 'OK')
@api.response(201, 'Created')
@api.response(400, 'Validation Error')
@api.response(404, 'Not Found')
class User_information(Resource):
    @api.doc(params={"id": 'user_id'})
    def get(self):
        id = parser.parse_args()['id']
        cmd = "Select username, password, email from Users where id = '{}'".format(id)
        result = read_sql(my_db, cmd)
        if len(result) == 0:
            return "", 404
        return {
                   "username": result[0]['username'],
                   "email": result[0]['email'],
                   "password": result[0]['password']
               }, 200


@api.route("/random_recipe")
@api.response(200, 'OK')
@api.response(201, 'Created')
@api.response(400, 'Validation Error')
@api.response(404, 'Not Found')
class Random_recipe(Resource):
    @api.doc(params={})
    def get(self):
        """
       Random choose recipes for main page
        """
        cmd = "SELECT id from Recipes"
        id_list = read_sql(my_db, cmd)
        id = [i['id'] for i in id_list]
        id_list = random.sample(id, k=6)
        result = []
        for id in id_list:
            cmd = "Select name, img, rating, serves, author, id FROM Recipes where id = '{}'".format(id)
            temp = read_sql(my_db, cmd)
            # print(temp)

            temp_dic = {}
            temp_dic['name'] = temp[0]['name']
            temp_dic['img'] = temp[0]['img']
            temp_dic['rating'] = temp[0]['rating']
            temp_dic['number_people'] = temp[0]['serves']
            temp_dic['author'] = temp[0]['author']
            temp_dic['id'] = temp[0]['id']
            result.append(temp_dic)

        return result, 200


@api.route("/get_user_recipes")
@api.response(200, 'OK')
@api.response(201, 'Created')
@api.response(400, 'Validation Error')
@api.response(404, 'Not Found')
class User_recipes(Resource):
    @api.doc(params={"id": 'user_id'})
    def get(self):
        """
        get user's recipes with their user id
        """
        id = parser.parse_args()['id']
        cmd = "Select r.name, r.img, r.rating, r.serves, r.author, r.id FROM Recipes r Join Recipe_list l on r.id = " \
              "l.recipe_id WHERE l.u_id = '{}'".format(id)
        temp = read_sql(my_db, cmd)
        if len(temp) == 0:
            return "NOT FOUND", 404
        # print(temp)
        result = []

        for i in temp:
            temp_dic = {}
            temp_dic['name'] = i['name']
            temp_dic['img'] = i['img']
            temp_dic['rating'] = i['rating']
            temp_dic['number_people'] = i['serves']
            temp_dic['author'] = i['author']
            temp_dic['id'] = i['id']
            result.append(temp_dic)

        return result, 200


@api.route("/signup")
@api.response(200, 'OK')
@api.response(201, 'Created')
@api.response(400, 'Validation Error')
@api.response(404, 'Not Found')
class Signup(Resource):
    @api.doc(params={"username": 'Username', 'password': 'Password', 'email': 'Email address'})
    def post(self):
        """
        Sign_up
        """
        email = get_argu('email')
        username = get_argu('username')
        password = get_argu('password')

        if not email or not password or not username:
            return {
                       "message": "Please provide valid information"
                   }, 400
        # Check if the email has benn enrolled before
        cmd = "SELECT * FROM Users WHERE email='{}'".format(email)
        users = read_sql(my_db, cmd)
        if len(users) != 0:
            return {
                       "message": "User already exist"
                   }, 200

        # Insert user into database
        cmd = "SELECT max(id) FROM Users"
        id = read_sql(my_db, cmd)

        current_id = id[0]['max(id)']
        if not current_id:
            current_id = 1
        else:
            current_id += 1
        database_controller(my_db,
                            "INSERT INTO Users(id, username, password, list_id, email) Values ('{}', "
                            "'{}', '{}', '{}', '{}')".format(current_id, username, password, current_id, email))
        return {
                   "message": "Created successful",
                   "id": current_id
               }, 201


@c_api.route("/")
@c_api.response(200, 'OK')
@c_api.response(201, 'Created')
@c_api.response(400, 'Validation Error')
@c_api.response(404, 'Not Found')
class Categories(Resource):

    @c_api.doc(params={"c_name": 'Category name'})
    def post(self):
        """
        Used to create categories used by back end developer
        This API is also be designed for uses to add new category in future vision
        """
        name = get_argu('c_name')
        if not name:
            return {
                       "message": "Empty input"
                   }, 405
        else:
            name = name.lower()
        """
        remove invalid format
        """
        name = re.sub('\s+', ' ', name)
        length = int(len(name))
        if name[length - 1] == ' ':
            name = name[:-1]
        if name[0] == ' ':
            name = name[1:]
        name = name.replace(' ', '_')

        cmd = "SELECT * FROM Categories WHERE category_name='{}'".format(name)
        result = read_sql(my_db, cmd)
        id = get_current_id('Categories')
        if len(result) != 0:
            return {
                       "message": "Category '{}' already exist".format(name)
                   }, 200

        database_controller(my_db,
                            "INSERT INTO Categories(id, category_name) Values ('{}', '{}')".format(id, name))
        return {
                   "message": "Successed",
                   "id": id,
                   "category_name": name
               }, 201

    @c_api.doc(params={"c_name": 'Category name'})
    def delete(self):
        """
        Used to delete categories
        """

        name = parser.parse_args()['c_name']
        cmd = "SELECT * FROM Categories WHERE category_name='{}'".format(name)
        result = read_sql(my_db, cmd)
        if len(result) == 0:
            return {
                       "message": "Category not exist"
                   }, 200
        else:
            database_controller(my_db,
                                "DELETE FROM Categories WHERE category_name='{}'".format(name))

            return {
                       "message": "Successed",
                       "category_name": name
                   }, 200

    @c_api.doc(params={})
    def get(self):
        """
        Get all categories
        """
        result = read_sql(my_db,
                          "SELECT category_name from Categories")
        categories_list = []
        for i in result:
            categories_list.append(i['category_name'])
        if len(categories_list) == 0:
            return {
                       "message": "Empty categories list"
                   }, 404
        else:
            return {
                       "result": categories_list
                   }, 200


@i_api.route("/")
@i_api.response(200, 'OK')
@i_api.response(201, 'Created')
@i_api.response(400, 'Validation Error')
@i_api.response(404, 'Not Found')
class Ingredients(Resource):
    @i_api.doc(params={"i_name": 'Ingredient name', 'c_name': 'Category name', "img": 'image address'})
    def post(self):
        """
        Used to create ingredient
        """
        name = get_argu('i_name').lower()
        c_name = get_argu('c_name').lower()
        img = get_argu('img')

        # remove empty space
        name = re.sub('\s+', ' ', name)
        length = int(len(name))
        if name[length - 1] == ' ':
            name = name[:-1]
        if name[0] == ' ':
            name = name[1:]
        name = name.replace(' ', '_')

        cmd = "SELECT * FROM Ingredients WHERE name='{}'".format(name)
        result = read_sql(my_db, cmd)
        if len(result) != 0:
            return {
                       "message": "Ingredient already exist"
                   }, 200

        cmd = "SELECT max(id) FROM Ingredients"
        id = read_sql(my_db, cmd)
        if id[0]['max(id)'] is None:
            cur_id = 1
        else:
            cur_id = id[0]['max(id)'] + 1

        cmd = "SELECT * FROM Categories WHERE category_name='{}'".format(c_name)
        result = read_sql(my_db, cmd)
        if len(result) == 0:
            return {
                       "message": "Category is not found"
                   }, 404
        c_id = result[0]['id']

        database_controller(my_db,
                            "INSERT INTO Ingredients(id, name, c_id, Img_address) Values ('{}', '{}','{}','{}')".format(
                                cur_id, name,
                                c_id, img))
        return {
                   "message": "Ingredient created",
                   'id': cur_id,
                   "name": name,
                   'ingredient_id': c_id,
                   "ingredient_name": c_name,
               }, 201

    @i_api.doc(params={"i_name": 'Ingredient name'})
    def delete(self):
        """
        Used to delete ingredient
        """
        name = parser.parse_args()['i_name']
        # remove empty space
        name = re.sub('\s+', ' ', name)
        length = int(len(name))
        if name[length - 1] == ' ':
            name = name[:-1]
        if name[0] == ' ':
            name = name[1:]
        name = name.replace(' ', '_')

        cmd = "SELECT * FROM Ingredients WHERE name='{}'".format(name)
        result = read_sql(my_db, cmd)
        if len(result) == 0:
            return {
                       "message": "Ingredient not exist"
                   }, 200
        else:
            database_controller(my_db,
                                "DELETE FROM Ingredients WHERE name='{}'".format(name))

            return {
                       "message": "Successed",
                       "ingredient_name": name
                   }, 200

    @i_api.doc(params={"c_name": 'category name'})
    def get(self):
        """
        Get all ingredients
        """
        c_name = parser.parse_args()['c_name']
        ingredient_list = {}
        if c_name is None:
            result = read_sql(my_db,
                              "SELECT * from Ingredients")

            for i in result:
                ingredient_list[i['name']] = i['img_address']

            if len(ingredient_list) == 0:
                return {
                           "message": "Empty categories list"
                       }, 404
            else:
                return {
                           "result": ingredient_list
                       }, 200
        else:
            cmd = "SELECT * FROM Categories WHERE category_name='{}'".format(c_name)
            result = read_sql(my_db, cmd)
            if not result:
                return {
                           "message": 'invalid category'
                       }, 404
            else:

                id = result[0]['id']
                cmd = "SELECT * FROM Ingredients WHERE c_id='{}'".format(id)
                result = read_sql(my_db, cmd)
                for i in result:
                    ingredient_list[i['name']] = i['img_address']

                return {
                           "result": ingredient_list
                       }, 200


@i_api.route("/get_category_by_ingredient")
@i_api.response(200, 'OK')
@i_api.response(201, 'Created')
@i_api.response(400, 'Validation Error')
@i_api.response(404, 'Not Found')
class Get_category(Resource):
    @i_api.doc(params={"ingredient_name": "ingredient_name"})
    def get(self):
        """
        return ingredient's category
        """
        name = get_argu('ingredient_name').lower()

        cmd = "SELECT * FROM Ingredients i Join Categories c on c.id = i.c_id WHERE name='{}'".format(name)
        result = read_sql(my_db, cmd)
        if len(result) == 0:
            return {
                       "message": "ingredient not exist"
                   }, 404
        else:
            return result[0]['category_name'], 200


@i_api.route("/get_all")
@i_api.response(200, 'OK')
@i_api.response(201, 'Created')
@i_api.response(400, 'Validation Error')
@i_api.response(404, 'Not Found')
class All_ingredients(Resource):
    @i_api.doc(params={})
    def get(self):
        """
        return all ingredients with category, used for main page
        """
        cmd = "Select category_name from Categories"
        result = read_sql(my_db, cmd)
        name = [i['category_name'] for i in result]
        result_list = []
        for i in name:
            cmd = "Select i.name from Ingredients i Join Categories c on c.id = i.c_id where c.category_name='{}'".format(
                i)
            result = {}
            temp = read_sql(my_db, cmd)
            result[i] = temp
            for j in temp:
                j['name'] = j['name'].replace('_', ' ')
            result_list.append(result)
        return result_list, 200


@i_api.route("/get_not_used_ingredients")
@i_api.response(200, 'OK')
@i_api.response(201, 'Created')
@i_api.response(400, 'Validation Error')
@i_api.response(404, 'Not Found')
class Not_used_ingre(Resource):
    @i_api.doc(params={})
    def get(self):
        """
        recommend ingredients to recipes contributors
        """
        cmd = "Select id from Ingredients"
        result = read_sql(my_db, cmd)
        all_id = [i['id'] for i in result]
        cmd = "Select Distinct recipe_id from Recipe_list"
        result = read_sql(my_db, cmd)
        used_id = [i['recipe_id'] for i in result]
        not_used_list = []
        for i in all_id:
            if i not in used_id:
                not_used_list.append(i)
        not_used_name = []
        for i in not_used_list:
            cmd = "Select name, id from Ingredients Where id = {}".format(i)
            result = read_sql(my_db, cmd)
            if len(result) != 0:
                not_used_name.append(str(result[0]['name']))
        not_used_name = ','.join(not_used_name[0:4])
        return not_used_name, 200


@i_api.route("/validation")
@i_api.response(200, 'OK')
@i_api.response(201, 'Created')
@i_api.response(400, 'Validation Error')
@i_api.response(404, 'Not Found')
class Valid_ingredients(Resource):
    @r_api.doc(params={"ingredient_name": 'ingredient name'})
    def get(self):
        name = get_argu('ingredient_name').lower()
        cmd = "Select name from Ingredients where name = '{}'".format(name)
        result = read_sql(my_db, cmd)
        if len(result) == 0:
            return 'Not found', 400
        else:
            return 'Found', 200


@r_api.route("/")
@r_api.response(200, 'OK')
@r_api.response(201, 'Created')
@r_api.response(400, 'Validation Error')
@r_api.response(404, 'Not Found')
class Recipes(Resource):
    @r_api.doc(params={"id": 'recipe id'})
    def get(self):
        """
        return recipe with recipe id
        """
        id = parser.parse_args()['id']
        ingredients = []
        cmd = "Select i.name from Ingredient_list l Join Ingredients i on l.ingredient_id = i.id where l.recipe_id={}".format(
            id)
        result = read_sql(my_db, cmd)
        for i in result:
            ingredients.append(i['name'])

        cmd = "Select * from Recipes where id = {}".format(id)
        result = read_sql(my_db, cmd)

        return {
                   'name': result[0]['name'],
                   'img': result[0]['img'],
                   'description': result[0]['description'],
                   'time': result[0]['time'],
                   'serves': result[0]['serves'],
                   'author': result[0]['author'],
                   'ingredients': ingredients,
                   'steps': result[0]['steps'],
                   'tags': result[0]['tags'].split(','),
                   'MealType': result[0]['type']
               }, 200


@r_api.route("/create_recipe")
@r_api.response(200, 'OK')
@r_api.response(201, 'Created')
@r_api.response(400, 'Validation Error')
@r_api.response(404, 'Not Found')
class Create_recipe(Resource):
    @r_api.doc(params={"name": 'recipe name', 'img': 'image address', 'description': 'description', 'time': 'time',
                       'serves': 'serving number', 'author': 'author', 'ingredients': 'ingredients',
                       'steps': 'steps', 'tags': 'tags', 'mealtype': 'meal type'})
    def post(self):
        """
        create recipes
        """
        id = get_current_id('Recipes')
        name = get_argu('name')
        img = get_argu('img')
        description = get_argu('description')
        time = get_argu('time')
        serves = get_argu('serves')
        author = get_argu('author')
        ingredients = get_argu('ingredients').split(',')
        steps_ = get_argu('steps')
        tags = get_argu('tags')
        tags_ = tags.upper()
        type = get_argu('mealtype').upper()
        user_id = get_argu('user_id')
        food_dic = {}

        for i in ingredients:
            cmd = "Select * from Ingredients where name = '{}'".format(i)
            result = read_sql(my_db, cmd)
            if len(result) == 0:
                return {
                           "message": "Ingredient {} not found".format(i)
                       }, 404
            else:
                food_dic[result[0]['id']] = result[0]['name']

        # assign values in ingredients table
        for i in food_dic.keys():
            database_controller(my_db,
                                "INSERT INTO Ingredient_list(recipe_id, ingredient_id) Values ('{}', '{}')".format(id,
                                                                                                                   i)
                                )
        # assign values in recipes table
        database_controller(my_db,
                            "INSERT INTO Recipes(id,name,img,description,time,serves,author,list_id,steps,tags,type)"
                            " Values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
                            .format(id, name, img, description, time, serves, author, id, steps_, tags_, type)
                            )
        # assign data about who created this recipe
        database_controller(my_db,
                            "INSERT INTO Recipe_list(u_id, recipe_id)"
                            " Values ('{}', '{}')"
                            .format(user_id, id)
                            )
        return {
                   "message": "Recipe {} created successfully".format(name)
               }, 200


@r_api.route("/get_recipes")
@r_api.response(200, 'OK')
@r_api.response(201, 'Created')
@r_api.response(400, 'Validation Error')
@r_api.response(404, 'Not Found')
class Recipe(Resource):
    @r_api.doc(params={"meal_Type": 'meal type', 'Ingredients': 'list of ingredients'})
    def post(self):
        """
        search recipes by ingredients and meal type
        """

        type = get_argu('meal_Type')
        ingredients_list = get_argu('Ingredients')

        # if no meal type selected
        if not type:
            ingredient_dic = {}
            cmd = "Select id FROM Recipes"
            temp = read_sql(my_db, cmd)
            recipes_id = [i['id'] for i in temp]

            # Select all recipes with their ingredients
            for id in recipes_id:
                cmd = "Select * From Ingredient_list Where recipe_id={}".format(id)
                result = read_sql(my_db, cmd)
                ls = []
                for i in result:
                    ls.append(i['ingredient_id'])
                ingredient_dic[result[0]['recipe_id']] = ls

            if not ingredients_list:
                return {
                           "Message": "No ingredient input"
                       }, 400
            # has ingredients input
            else:
                ingredients_list = ingredients_list.split(',')
                length = len(ingredients_list)
                for i in range(length):
                    ingredients_list[i] = ingredients_list[i].lower()
                cmd = 'Select id, name from Ingredients where '
                for i in range(length):
                    if i != 0:
                        cmd += " or name='{}'".format(ingredients_list[i])
                    else:
                        cmd += "name='{}'".format(ingredients_list[i])
                result = read_sql(my_db, cmd)
                ingredients_id = [i['id'] for i in result]

            """
            # Recommendation
            The algorithm will compare input ingredients and all recipes
            """
            scores = {}
            for key in ingredient_dic.keys():
                scores[key] = 0

            for key in ingredient_dic.keys():
                for i in ingredients_id:
                    if i in ingredient_dic[key]:
                        scores[key] += 1

            recipes_list = []
            scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            scores = dict(scores)
            remove_id = [i for i in scores.keys() if scores[i] == 0]

            for i in remove_id:
                scores.pop(i)
            for i in scores.keys():
                cmd = "Select name, img, rating, serves, author, id from Recipes where id={}".format(i)
                temp = read_sql(my_db, cmd)
                recipes_list.append(temp[0])
            flag = 0
            for i in scores.values():
                if i != 0:
                    flag = 1

            if len(recipes_list) == 0 or flag == 0:
                return {
                           "message": "No recipe found"
                       }, 404
            else:

                if max(scores.values()) != length:
                    return recipes_list, 201
                else:
                    return recipes_list, 200
        # Searching with meal type
        else:
            type = type.split(',')

            for i in range(len(type)):
                type[i] = type[i].upper()
            cmd = "Select * From Recipes Where "
            for i in range(len(type)):
                if i != 0:
                    cmd += " or type='{}'".format(type[i])
                else:
                    cmd += "type='{}'".format(type[i])
            result = read_sql(my_db, cmd)
            recipes_id = [i['id'] for i in result]
            ingredient_dic = {}
            for id in recipes_id:
                cmd = "Select * From Ingredient_list Where recipe_id={}".format(id)
                result = read_sql(my_db, cmd)
                ls = []
                for i in result:
                    ls.append(i['ingredient_id'])
                ingredient_dic[result[0]['recipe_id']] = ls

        if not ingredients_list:
            return {
                       "Message": "No ingredient input"
                   }, 400
        else:
            ingredients_list = ingredients_list.split(',')
            length = len(ingredients_list)
            for i in range(length):
                ingredients_list[i] = ingredients_list[i].lower()
            cmd = 'Select id, name from Ingredients where '
            for i in range(length):
                if i != 0:
                    cmd += " or name='{}'".format(ingredients_list[i])
                else:
                    cmd += "name='{}'".format(ingredients_list[i])
            result = read_sql(my_db, cmd)
            ingredients_id = [i['id'] for i in result]

        """
        # Recommendation
        """
        scores = {}
        for key in ingredient_dic.keys():
            scores[key] = 0

        for key in ingredient_dic.keys():
            for i in ingredients_id:
                if i in ingredient_dic[key]:
                    scores[key] += 1

        recipes_list = []
        scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        scores = dict(scores)
        remove_id = [i for i in scores.keys() if scores[i] == 0]

        for i in remove_id:
            scores.pop(i)
        for i in scores.keys():
            cmd = "Select name, img, rating, serves, author, id from Recipes where id={}".format(i)
            temp = read_sql(my_db, cmd)
            recipes_list.append(temp[0])
        # scores = dict(scores)
        flag = 0
        for i in scores.values():
            if i != 0:
                flag = 1

        if len(recipes_list) == 0 or flag == 0:
            return {
                       "message": "No recipe found"
                   }, 404
        else:

            if max(scores.values()) != length:
                return recipes_list, 201
            else:
                return recipes_list, 200


@r_api.route("/recommend_ingredients")
@r_api.response(200, 'OK')
@r_api.response(201, 'Created')
@r_api.response(400, 'Validation Error')
@r_api.response(404, 'Not Found')
class Recipes_in(Resource):
    @r_api.doc(params={"meal_Type": 'meat type', 'Ingredients': 'list of ingredients'})
    def post(self):
        type = get_argu('meal_Type')
        ingredients_list = get_argu('Ingredients')

        if not type:
            return {
                       "Message": "No meal type input"
                   }, 400
        else:
            """
            The algorithm is similar to recommendation recipes
            By going through all recipes and compare with input ingredients
            """
            type = type.split(',')
            length = len(type)
            for i in range(length):
                type[i] = type[i].upper()
            cmd = "Select * From Recipes Where "
            for i in range(length):
                if i != 0:
                    cmd += " or type='{}'".format(type[i])
                else:
                    cmd += "type='{}'".format(type[i])
            result = read_sql(my_db, cmd)
            recipes_id = [i['id'] for i in result]
            ingredient_dic = {}
            for id in recipes_id:
                cmd = "Select * From Ingredient_list Where recipe_id={}".format(id)
                result = read_sql(my_db, cmd)
                ls = []
                for i in result:
                    ls.append(i['ingredient_id'])
                ingredient_dic[result[0]['recipe_id']] = ls

        if not ingredients_list:
            return {
                       "Message": "No ingredient input"
                   }, 400
        else:
            ingredients_list = ingredients_list.split(',')
            # print(ingredients_list[0])

            length = len(ingredients_list)
            for i in range(length):
                ingredients_list[i] = ingredients_list[i].lower()
            cmd = 'Select id, name from Ingredients where '
            for i in range(length):
                if i != 0:
                    cmd += " or name='{}'".format(ingredients_list[i])
                else:
                    cmd += "name='{}'".format(ingredients_list[i])
            result = read_sql(my_db, cmd)
            ingredients_id = [i['id'] for i in result]

        # print(ingredients_id)
        # print(ingredient_dic)
        scores = {}
        for i in ingredient_dic:
            scores[i] = 0
        for i in ingredient_dic.keys():
            for id in ingredients_id:
                if id in ingredient_dic[i]:
                    scores[i] += 1
        result_id = {}
        for i in scores.keys():
            if int(scores[i]) == len(ingredients_id) and len(ingredient_dic[i]) > int(scores[i]):
                result_id[i] = ingredient_dic[i]
        # print(result_id)

        recomment_list = []
        for i in result_id.keys():
            for id in ingredients_id:
                result_id[i].remove(id)

        for i in result_id.keys():
            for id in result_id[i]:
                if id not in recomment_list:
                    recomment_list.append(id)
        final = []
        for i in recomment_list:
            cmd = "Select name from Ingredients where id = '{}'".format(i)
            result = read_sql(my_db, cmd)
            final.append(result[0]['name'])
        if len(final) != 0:
            final = final[0]
            return final, 200


@r_api.route("/get_meal_type")
@r_api.response(200, 'OK')
@r_api.response(201, 'Created')
@r_api.response(400, 'Validation Error')
@r_api.response(404, 'Not Found')
class Get_mealType(Resource):
    @r_api.doc(params={})
    def get(self):
        cmd = "Select DISTINCT type from Recipes"
        temp = read_sql(my_db, cmd)
        result = [i['type'] for i in temp]

        for i in range(len(result)):
            if result[i] is None:
                result[i] = 'Else'

        result = sorted(result)
        return result, 200


@r_api.route("/delete_recipe")
@r_api.response(200, 'OK')
@r_api.response(201, 'Created')
@r_api.response(400, 'Validation Error')
@r_api.response(404, 'Not Found')
class Delete_recipe(Resource):
    @r_api.doc(params={'id': 'recipe_id'})
    def delete(self):
        id = parser.parse_args()['id']
        cmd = "DELETE FROM Recipe_list WHERE recipe_id = '{}'".format(id)
        database_controller(my_db, cmd)
        cmd = "DELETE FROM Recipes WHERE id = '{}'".format(id)
        database_controller(my_db, cmd)
        cmd = "DELETE FROM Ingredient_list WHERE recipe_id = '{}'".format(id)
        database_controller(my_db, cmd)
        return {
                   "message": "Deleted"
               }, 200


@r_api.route("/search_by_name")
@r_api.response(200, 'OK')
@r_api.response(201, 'Created')
@r_api.response(400, 'Validation Error')
@r_api.response(404, 'Not Found')
class Searching_recipe(Resource):
    @r_api.doc(params={'recipe_name': 'recipe_name'})
    def get(self):
        name = get_argu('recipe_name')
        cmd = "Select * from Recipes where name = '{}'".format(name)
        temp = read_sql(my_db, cmd)
        if len(temp) == 0:
            return 'Not found', 404
        else:
            result = []

            for i in temp:
                temp_dic = {}
                temp_dic['name'] = i['name']
                temp_dic['img'] = i['img']
                temp_dic['rating'] = i['rating']
                temp_dic['number_people'] = i['serves']
                temp_dic['author'] = i['author']
                temp_dic['id'] = i['id']
                result.append(temp_dic)

            return result, 200


# run app
app.run(port=8010, debug=True)

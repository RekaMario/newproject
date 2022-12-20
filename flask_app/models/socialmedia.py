from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

#Creation of the class of Post
class Socialmedia:
    db_name='ctuDB' # Our database name in the workbench
    def __init__(self,data):
        self.id = data['socialmedia_id'],
        self.website = data['website'],
        self.github = data['github'],
        self.twitter = data['twitter'],
        self.facebook = data['facebook'],
        self.linkedin = data['linkedin'],
        self.user_id = data['user_id']
        
        
        
        
        
        
    @classmethod
    def create_socialmedia(cls, data):
        query = "INSERT INTO socialmedia  ( website ,github , twitter , facebook , linkedin, user_id) VALUES( %(website)s, %(github)s ,%(twitter)s , %(facebook)s , %(linkedin)s, %(user_id)s );"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def update_socialmedia(cls, data):
        query = "UPDATE socialmedia SET website = %(website)s, github = %(github)s, twitter = %(twitter)s, facebook = %(facebook)s,linkedin = %(linkedin)s WHERE id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def get_all_socialmedia(cls):
        query = "SELECT * FROM socialmedia;"
        results = connectToMySQL(cls.db_name).query_db(query)
        socialmedia = []
        for row in results:
            socialmedia.append(row)
        return socialmedia
    
    
    @classmethod
    def get_socialmedia_by_id(cls, data):
        query = "SELECT *FROM users LEFT JOIN socialmedia ON users.id = socialmedia.user_id WHERE users.id = %(user_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if len(result) < 1:
            return False
        return result[0]
    
    
    
    
    @staticmethod
    def validate_socialmedia(socialmedia):
        is_valid = True

        if len(socialmedia['website']) < 6:
            flash("link must be at least 6 characters.", 'website')
            is_valid = False
        return is_valid
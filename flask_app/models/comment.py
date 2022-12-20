from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

#Creation of the class of Post
class Comment:
    db_name='ctuDB' # Our database name in the workbench
    def __init__(self,data):
        self.id = data['comment_id'],
        self.answer = data['answer'],
        self.user_id = data['user_id'],
        self.post_id = data['post_id'],
        self.created_at = data['created_at']
        
        
        
    
    #comment Section
    
    @classmethod
    def create_comment(cls, data):
        query= 'INSERT INTO comments (  answer ,user_id, post_id ) VALUES ( %(answer)s, %(user_id)s,%(post_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_all_comments(cls):
        query = "SELECT * FROM comments;"
        results = connectToMySQL(cls.db_name).query_db(query)
        comments = []
        for row in results:
            comments.append(row)
        return comments
    
    @classmethod
    def get_comment_by_id(cls, data):
        query= 'SELECT * FROM comments WHERE comment.id = %(comment_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]
    
    @classmethod
    def destroy_comment(cls, data):
        query= 'DELETE FROM comments WHERE comments.id = %(comment_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #
    
    @staticmethod
    def validate_comment(comment):
        is_valid = True
        if len(comment['answer']) < 2:
            flash("Post content must be at least 2 characters.", 'answer')
            is_valid = False
        return is_valid
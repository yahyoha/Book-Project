from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app= Flask(__name__)
api= Api(app)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
CORS(app)
db= SQLAlchemy(app)

## defining the book model
class BookModel(db.Model):
    order_id= db.Column(db.Integer, primary_key= True)
    novel= db.Column(db.String(100), nullable= False)
    novel_page= db.Column(db.String(256), nullable= False)
    author= db.Column(db.String(100), nullable= False)
    author_page= db.Column(db.String(256), nullable=False)
    country= db.Column(db.String(100), nullable= False)
    country_page= db.Column(db.String(256), nullable=False)


#used this for creating the db once
# db.create_all()  


book_post_args= reqparse.RequestParser()
book_post_args.add_argument('novel', type=str, help='Book name is required', required=True)
book_post_args.add_argument('novel_page', type=str, help='book page is required', required=False)
book_post_args.add_argument('author', type=str, help='author name is required', required=True)
book_post_args.add_argument('author_page', type=str, help='author page is required', required=False)
book_post_args.add_argument('country', type=str, help='country name is required', required=False)
book_post_args.add_argument('country_page', type=str, help='country page is required', required=False)



book_update_args= reqparse.RequestParser()
book_update_args.add_argument('novel', type=str, help='Book name is required')
book_update_args.add_argument('novel_page', type=str, help='book page is required')
book_update_args.add_argument('author', type=str, help='author name is required')
book_update_args.add_argument('author_page', type=str, help='author page is required')
book_update_args.add_argument('country', type=str, help='country name is required')
book_update_args.add_argument('country_page', type=str, help='country page is required')



resource_fields= {
    'order_id': fields.Integer,
    'novel': fields.String,
    'novel_page': fields.String,
    'author': fields.String,
    'author_page':fields.String,
    'country':fields.String,
    'country_page':fields.String
}

class Book(Resource):
    # getting details of a book entry
    @marshal_with(resource_fields)
    def get(self, book_order_id):
        result= BookModel.query.filter_by(order_id=book_order_id).first()
        if not result:
            abort(404, message= 'could not find a book with that order in the list')
        return result

    # creating new book entry
    @marshal_with(resource_fields)
    def post(self, book_order_id):
        result= BookModel.query.filter_by(order_id=book_order_id).first()
        args= book_post_args.parse_args()
        print(args)
        if result:
            abort(409, message="Book order_id is taken")
        book= BookModel(order_id= book_order_id, novel= args['novel'], novel_page= args['novel_page'],
                        author= args['author'], author_page= args['author_page'], 
                        country= args['country'], country_page= args['country_page'])
        db.session.add(book)
        db.session.commit()
        return book, 201


    # updating details of a book entry
    @marshal_with(resource_fields)
    def patch(self, book_order_id):
        print("PATCHINGGGGGG")
        args= book_update_args.parse_args()
        result= BookModel.query.filter_by(order_id=book_order_id).first()
        if not result:
            abort(404, message='book id does not exist')
        if args['novel']:
            result.novel=args['novel'] 
        if args['novel_page']:
            result.novel_page=args['novel_page']
        if args['author']:
            result.author=args['author']
        if args['author_page']:
            result.author_page=args['author_page']
        if args['country']:
            result.country=args['country']
        if args['country_page']:
            result.country_page=args['country_page']
        db.session.commit()
        return result, 200


    def delete(self, book_order_id):
        result= BookModel.query.filter_by(order_id=book_order_id).first()
        if not result:
            abort(404, message="book order it does not exist")
        db.session.delete(result)
        db.session.commit()
        return '', 204

    
api.add_resource(Book, "/book/<int:book_order_id>")

if __name__=='__main__':
    app.run()
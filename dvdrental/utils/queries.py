from .models import *

'''
`DBQueries` class is a collection of sqlAlchemy orm queries. It utilizes a session
'''

class DBQueries:

    def __init__(self, db_session):
        self.session = db_session

    def query_list_of_films_in_category(self, category: str):
        result = self.session.query(Film).where(Film.film_id.in_([item.film_id for item in self.query_category_film_id_execute(category).all()])).order_by(Film.film_id.asc())
        return [item.__dict__ for item in result]

    def query_category_film_id(self, category: str):
        result = self.session.query(FilmCategory).join(Category, FilmCategory.category_id == Category.category_id).where(Category.name == category)
        return result

    def query_category_film_id_execute(self, category: str):
        stmt = select(FilmCategory.film_id).select_from(FilmCategory).join(Category, FilmCategory.category_id == Category.category_id).where(Category.name == category)
        r = self.session.execute(stmt)
        return r


    def query_list_of_films_in_category_by_txt(self, category: str):
        q_txt = text("SELECT  film_id,  title  FROM  film  WHERE  film_id IN ( SELECT film_id  FROM  film_category  INNER JOIN category USING(category_id)  WHERE  name = 'Action' ) ORDER BY film_id;")
        result = self.session.query(Film).from_statement(q_txt).all()
        return result


    def query_for(self, name: str, *args, **kwargs):
        '''
        Accepts the name of a method and its arguments in DBQueries class and will execute the function
        :param name: method name
        :param args: accepts any number of arguments
        :param kwargs: accepts any number of keyword arguments
        :return: executes the function, 'name' arg, and returns what s returned from the function
        '''
        query = f'query_{name}'
        if hasattr(self, query) and callable(func := getattr(self, query)):
            return func(*args, **kwargs)

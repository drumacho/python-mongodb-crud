import os
import datetime
import tornado.ioloop
import tornado.web
import tornado.template
import pymongo


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        client = pymongo.MongoClient('localhost', 27017)
        db = client.python_mongodb_crud
        users = db.users

        self.render("index.html", items=users.find())


class CreateHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("edit.html", title='新規追加', action='add')

    # 登録処理
    def post(self):
        # POSTパラメータ取得
        name = self.get_argument('name')
        gender = self.get_argument('gender')
        birth_year = self.get_argument('birth_year')
        birth_month = self.get_argument('birth_month')
        birth_day = self.get_argument('birth_day')
        # TODO バリデーション
        birthday = f'{birth_year.zfill(4)}-{birth_month.zfill(2)}-{birth_day.zfill(2)}'
        user = {'name': name, 'gender': gender, 'birthday': birthday}

        # DBに登録
        client = pymongo.MongoClient('localhost', 27017)
        db = client.python_mongodb_crud
        users = db.users
        user_id = users.insert_one(user)
        self.redirect('/', permanent=True)


class UpdateHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("edit.html", title='編集', action='edit')

    def post(self):
        # TODO 更新処理
        self.redirect('/', permanent=True)


class DeleteHandler(tornado.web.RequestHandler):
    def get(self):
        # TODO 削除処理
        self.redirect('/', permanent=True)


def make_app():
    return tornado.web.Application(
        [
            tornado.web.url(r"/", IndexHandler, name='index'),
            tornado.web.url(r"/add", CreateHandler, name='add'),
            tornado.web.url(r"/edit", UpdateHandler, name='edit'),
            tornado.web.url(r"/delete", DeleteHandler, name='delete'),
        ],
        template_path=os.path.join(os.getcwd(), "templates"),
        static_path=os.path.join(os.getcwd(), "static"),
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
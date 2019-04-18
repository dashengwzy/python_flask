# 排序操作需要引入
import operator
import os

# 导入 bs4 库,创建 Beautiful Soup 对象,用来从html文本中提取文本内容
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, session, g
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads
# 引入Python中的jquery PyQuery库
from pyquery import PyQuery as pq

import config
import myglobal
from exts import db
from models import Article
from models import Banner
from models import Chemistry_data
from models import Hydrology_data
from models import Marine_chemistry
from models import Marine_hydrology
from models import Marine_organism
from models import Organism_data
from models import User
from datetime import timedelta
app = Flask(__name__)
# 配置文件上传的路径以及限制条件
app.config['UPLOADED_PHOTO_DEST'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static\images")
app.config['UPLOADED_PHOTO_ALLOW'] = ['png', 'jpg']
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
# 设置SECRET_KEY以使用session
app.config.update(SECRET_KEY='123456')
# 实例化 UploadSet 对象
photos = UploadSet('PHOTO')
# 将 app 的 config 配置注册到 UploadSet 实例 photos
configure_uploads(app, photos)
bootstrap = Bootstrap(app)
app.config.from_object(config)
# 新建一个Banner模型，采用models分开的方式
# flask-scripts的方式
db.init_app(app)
# 激活程序上下文
ctx = app.app_context()
ctx.push()


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return redirect(url_for('show', name=filename))
    return render_template('upload.html')


@app.route('/photo/<name>')
def show(name):
    if name is None:
        return "wrong"
    url = photos.url(name)
    return render_template('show.html', url=url, name=name)



@app.route('/index')
def index():
    # 查询最新上传的数据放到首页的面板内
    # 查询所有存放数据的表，每个表中的数据按照时间排列进存储在变量之中
    # 需要存储的是这个信息属于哪个表，id是什么，数据名称是什么，方便展示和跳转
    # data_all用来存储所有的数据信息，将来用传到前台用来展示
    data_all_new = []
    data_all_down = []
    marine_organisms = Organism_data.query.order_by('id').all()
    marine_hydrologys = Hydrology_data.query.order_by('id').all()
    marine_chemistrys = Chemistry_data.query.order_by('id').all()
    data_all_new = data_all_new + marine_hydrologys
    data_all_new = data_all_new + marine_organisms
    data_all_new = data_all_new + marine_chemistrys
    data_all_down = data_all_new.copy()
    # print(data_all_down.__len__())
    # 数据排序操作
    cmpfun_new = operator.attrgetter('data_time')  # 参数为排序依据的属性，根据上传时间进行排序
    data_all_new.sort(key=cmpfun_new, reverse=True)  # 根据配置进行排序
    cmpfun_down = operator.attrgetter('down_time')  # 参数为排序依据的属性，根据下载次数进行排序
    data_all_down.sort(key=cmpfun_down, reverse=True)  # 根据配置进行排序
    # 查询结果限制在5条内容
    articles = Article.query.order_by('time').limit(5).all()
    # 对过长的标题进行一些处理
    for article in articles:
        if len(article.title) > 18:
            num_str_1 = article.title[0:17]
            article.title = num_str_1
    context = {
        'banners': Banner.query.order_by('id').all(),
        'data_all_new': data_all_new,
        'data_all_down': data_all_down,
        'articles': articles
    }
    return render_template('index.html', **context)


# 海洋生物数据集的总展示页面
@app.route('/marine_organism/list/<int:page>/<int:state>', methods=['GET', 'POST'])
def marine_organism(page, state):
    if request.method == 'GET' and state == 0:
        if page is None:
            page = 1
        context = {
            'marine_organisms': Marine_organism.query.order_by('id').paginate(page=page, per_page=8),
            'state': 0
        }
        return render_template('marine_organism.html', **context)
    else:
        # 获取用户输入的关键字
        # search和分页不能同时实现的原因在于，search第二次分页因为走得是第一条路，所以数据不一样了。先不考虑直接点击按钮的问题
        key_word = request.form.get('organism_key_word')
        if key_word is None or key_word is "":
            key_word = myglobal.get_value()
            # 将关键字拼接成模糊字段
            args = '%' + key_word + '%'
        else:
            myglobal.set_value(key_word)
            # 将关键字拼接成模糊字段
            args = '%' + myglobal.get_value() + '%'
        marine_organism_search = Marine_organism.query.filter(
            Marine_organism.data_set_name.like(args)
        ).paginate(page=page, per_page=8)
        context = {
            'marine_organisms': marine_organism_search,
            'state': 1
        }
        return render_template('marine_organism.html', **context)


# 单个海洋生物数据集的展示页面
@app.route('/marine_organism_one/<marine_organism_id>/', methods=['GET', 'POST'])
def organism_one(marine_organism_id):
    # 如果是正常的加载当前页面
    if request.method == 'GET':
        marine_organism_one = Marine_organism.query.filter(Marine_organism.id == marine_organism_id).first()
        # 根据数据集的归属类型，查询到所有属于本数据集的所有数据
        organism_data = Organism_data.query.filter(Organism_data.data_kind == marine_organism_one.data_set_name).all()
        context = {
            'marine_organism_one': marine_organism_one,
            'organism_datas': organism_data
        }
        return render_template('marine_organism_one.html', **context)
    # 如果是从当前页面获取数据进行进一步操作
    else:
        # 获取用户输入的关键字
        key_word = request.form.get('key_word')
        # 将关键字拼接成模糊字段
        args = '%' + key_word + '%'
        marine_organism_one = Marine_organism.query.filter(Marine_organism.id == marine_organism_id).first()
        organism_datas = Organism_data.query.filter(Organism_data.data_name.like(args),
                                                    Organism_data.data_kind == marine_organism_one.data_set_name).all()
        context = {
            'marine_organism_one': marine_organism_one,
            'organism_datas': organism_datas
        }
        return render_template('marine_organism_one.html', **context)


# 如果点击的是下载按钮，则进行文件下载
@app.route('/download/file_name:<filename>/<string:tablename>/<int:id>', methods=['GET', 'POST'])
def download(filename,tablename,id):
    # 1. 先把你要更改的数据查找出来
    if tablename == 'hydrology_data':
        new1 = Hydrology_data.query.filter(Hydrology_data.id == id).first()
    elif tablename == "chemistry_data":
        new1 = Chemistry_data.query.filter(Chemistry_data.id == id).first()
    else:
        new1 = Organism_data.query.filter(Organism_data.id == id).first()
    # # 2. 把这条数据，你需要修改的地方进行修改
    newtime = new1.down_time + 1
    new1.down_time = newtime
    print(new1.down_time)
    # # 3. 做事务的提交
    db.session.commit()
    if os.path.isfile(os.path.join('static/upload_file', filename)):
        return send_from_directory('static/upload_file', filename, as_attachment=True)
    abort(404)


# 海洋水文数据集总展示页面
@app.route('/marine_hydrology/list/<int:page>/<int:state>', methods=['GET', 'POST'])
def marine_hydrology(page, state):
    if request.method == 'GET' and state == 0:
        if page is None:
            page = 1
        context = {
            'marine_hydrologys': Marine_hydrology.query.order_by('id').paginate(page=page, per_page=8),
            'state': 0
        }
        return render_template('marine_hydrology.html', **context)
    else:
        # 获取用户输入的关键字
        # search和分页不能同时实现的原因在于，search第二次分页因为走得是第一条路，所以数据不一样了。先不考虑直接点击按钮的问题
        key_word = request.form.get('hydrology_key_word')
        if key_word is None or key_word is "":
            key_word = myglobal.get_value()
            # 将关键字拼接成模糊字段
            args = '%' + key_word + '%'
        else:
            myglobal.set_value(key_word)
            # 将关键字拼接成模糊字段
            args = '%' + myglobal.get_value() + '%'
        marine_hydrology_search = Marine_hydrology.query.filter(
            Marine_hydrology.data_set_name.like(args)
        ).paginate(page=page, per_page=8)
        context = {
            'marine_hydrologys': marine_hydrology_search,
            'state': 1
        }
        return render_template('marine_hydrology.html', **context)


# 海洋水文单个数据展示页面
@app.route('/hydrology_one/<marine_hydrology_id>/', methods=['GET', 'POST'])
def hydrology_one(marine_hydrology_id):
    # 如果是正常的加载当前页面
    if request.method == 'GET':
        marine_hydrology_one = Marine_hydrology.query.filter(Marine_hydrology.id == marine_hydrology_id).first()
        # 根据数据集的归属类型，查询到所有属于本数据集的所有数据
        # print(marine_hydrology_one.data_set_name)
        hydrology_datas = Hydrology_data.query.filter(
            Hydrology_data.data_kind == marine_hydrology_one.data_set_name).all()
        context = {
            'marine_hydrology_one': marine_hydrology_one,
            'hydrology_datas': hydrology_datas
        }
        # for index,hydrology_data in enumerate(hydrology_datas):  # 第二个实例
        # print(len(hydrology_datas))
        return render_template('marine_hydrology_one.html', **context)
    # 如果是从当前页面获取数据进行进一步操作
    else:
        # 获取用户输入的关键字
        hy_key_word = request.form.get('hy_key_word')
        # 将关键字拼接成模糊字段
        args = '%' + hy_key_word + '%'
        marine_hydrology_one = Marine_hydrology.query.filter(Marine_hydrology.id == marine_hydrology_id).first()
        hydrology_datas = Hydrology_data.query.filter(Hydrology_data.data_name.like(args),
                                                      Hydrology_data.data_kind == marine_hydrology_one.data_set_name).all()
        context = {
            'marine_hydrology_one': marine_hydrology_one,
            'hydrology_datas': hydrology_datas
        }
        return render_template('marine_hydrology_one.html', **context)


# 海洋化学数据集总展示页面
@app.route('/marine_chemistry/list/<int:page>/<int:state>', methods=['GET', 'POST'])
def marine_chemistry(page, state):
    if request.method == 'GET' and state == 0:
        if page is None:
            page = 1
        context = {
            'marine_chemistrys': Marine_chemistry.query.order_by('id').paginate(page=page, per_page=8),
            'state': 0
        }
        return render_template('marine_chemistry.html', **context)
    else:
        # 获取用户输入的关键字
        # search和分页不能同时实现的原因在于，search第二次分页因为走得是第一条路，所以数据不一样了。先不考虑直接点击按钮的问题
        key_word = request.form.get('chdrology_key_word')
        if key_word is None or key_word is "":
            key_word = myglobal.get_value()
            # 将关键字拼接成模糊字段
            args = '%' + key_word + '%'
        else:
            myglobal.set_value(key_word)
            # 将关键字拼接成模糊字段
            args = '%' + myglobal.get_value() + '%'
        marine_chemistry_search = Marine_chemistry.query.filter(
            Marine_chemistry.data_set_name.like(args)
        ).paginate(page=page, per_page=8)
        context = {
            'marine_chemistrys': marine_chemistry_search,
            'state': 1
        }
        return render_template('marine_chemistry.html', **context)


# 海洋化学单个数据展示页面
@app.route('/chemistry_one/<marine_chemistry_id>/', methods=['GET', 'POST'])
def chemistry_one(marine_chemistry_id):
    # 如果是正常的加载当前页面
    if request.method == 'GET':
        marine_chemistry_one = Marine_chemistry.query.filter(Marine_chemistry.id == marine_chemistry_id).first()
        # 根据数据集的归属类型，查询到所有属于本数据集的所有数据
        chemistry_datas = Chemistry_data.query.filter(
            Chemistry_data.data_kind == marine_chemistry_one.data_set_name).all()
        context = {
            'marine_chemistry_one': marine_chemistry_one,
            'chemistry_datas': chemistry_datas
        }
        print(chemistry_datas)
        return render_template('marine_chemistry_one.html', **context)
    # 如果是从当前页面获取数据进行进一步操作
    else:
        marine_chemistry_one = Marine_chemistry.query.filter(Marine_chemistry.id == marine_chemistry_id).first()
        # 获取用户输入的关键字
        ch_key_word = request.form.get('ch_key_word')
        # 将关键字拼接成模糊字段
        args = '%' + ch_key_word + '%'
        marine_chemistry_one = Marine_chemistry.query.filter(Marine_chemistry.id == marine_chemistry_id).first()
        chemistry_datas = Chemistry_data.query.filter(Chemistry_data.data_name.like(args),
                                                      Chemistry_data.data_kind == marine_chemistry_one.data_set_name).all()
        context = {
            'marine_chemistry_one': marine_chemistry_one,
            'chemistry_datas': chemistry_datas
        }
        return render_template('marine_chemistry_one.html', **context)


# 数据服务展示页面
@app.route('/data', methods=['GET', 'POST'])
def data():
    return render_template('data.html')


# 资讯详情总展示页面
@app.route('/article_all/list/<int:page>/<int:state>', methods=['GET', 'POST'])
def article_all(page, state):
    articles = Article.query.order_by('id').paginate(page=page, per_page=8)
    # html_doc = articles.items[0].content
    # soup = BeautifulSoup(html_doc, 'html.parser')
    # .strings获取多个内容，不过需要遍历获取，输出的字符串中可能包含了很多空格或空行,使用 .stripped_strings 可以去除多余空白内容
    # for string in soup.stripped_strings:
    #     print(repr(string))
    # print(articles.items[0].content)
    # 对文章正文用BeautifulSoup进行文本提取，抽取文本内容重新赋值，以便前台展示
    for article in articles.items:
        html_doc = article.content
        soup = BeautifulSoup(html_doc, 'html.parser')
        for string in soup.stripped_strings:
            article.content = repr(string)[0:170]
            print(article.content)
            # article.content = soup.span.string
    if request.method == 'GET' and state == 0:
        if page is None:
            page = 1
        context = {
            'articles': articles,
            'state': 0
        }
        return render_template('article_all.html', **context)
    else:
        # 获取用户输入的关键字
        # search和分页不能同时实现的原因在于，search第二次分页因为走得是第一条路，所以数据不一样了。先不考虑直接点击按钮的问题
        key_word = request.form.get('article_key_word')
        if key_word is None or key_word is "":
            key_word = myglobal.get_value()
            # 将关键字拼接成模糊字段
            args = '%' + key_word + '%'
        else:
            myglobal.set_value(key_word)
            # 将关键字拼接成模糊字段
            args = '%' + myglobal.get_value() + '%'
        article_search = Article.query.filter(
            Article.title.like(args)
        ).paginate(page=page, per_page=8)
        context = {
            'articles': article_search,
            'state': 1
        }
        return render_template('article_all.html', **context)


# 资讯详情页面
@app.route('/article_one/<article_id>/', methods=['GET', 'POST'])
def article_one(article_id):
    article = Article.query.filter(Article.id == article_id).first()
    print(article.content)
    context = {
        'article': article,
    }
    return render_template('article_one.html', **context)


# 注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    # 如果是正常的加载当前页面
    if request.method == 'GET':
        return render_template('register.html')
    # 如果是从当前页面获取数据进行进一步操作
    else:
        # 获取用户输入的用户名
        username = request.form.get('username')
        # 获取用户输入的密码
        password = request.form.get('password')
        # 获取用户输入的密码
        organ = request.form.get('organ')
        # 在数据库里面查找是否已经有该用户
        User_if = User.query.filter(User.username == username).first()
        if User_if is None:
            # 增加数据
            # 增加：
            user1 = User(
                organ=organ,
                username=username,
                password=password,
            )
            db.session.add(user1)
            # 事务
            db.session.commit()
            return render_template('login.html')
        else:
            return render_template('register_two.html')


# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    # 如果是正常的加载当前页面
    if request.method == 'GET':
        context = {
            'state': 0,
        }
        return render_template('login.html', **context)
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username).first()
        if user and user.password == password:
            print(user.id)
            session['user_id'] = user.id
            # 如果想在31天内都不需要登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            context = {
                'state': 1,
            }
            return render_template('login.html', **context)

# 注销登录
@app.route('/logout/')
def logout():
    session.clear()
    context = {
        'state': 0,
    }
    return render_template('login.html', **context)



# 装饰函数，运行在最前面
@app.before_request
def before_request():
    # 初始化全局变量
    myglobal.set_value("")
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}



if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, g
from flask_uploads import UploadSet, IMAGES, configure_uploads, ALL
from flask_bootstrap import Bootstrap
from exts import db
from models import Banner
from models import Marine_organism
from models import Organism_data
from models import Marine_hydrology
from models import Hydrology_data
import config
import os
import myglobal


app = Flask(__name__)
# 配置文件上传的路径以及限制条件
app.config['UPLOADED_PHOTO_DEST'] =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "static\images")
app.config['UPLOADED_PHOTO_ALLOW'] = ['png', 'jpg']
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


# 下载文件测试函数
# @app.route('/download/file_name:<filename>', methods=['GET'])
# def download(filename):
#     if request.method == "GET":
#         if os.path.isfile(os.path.join('static/upload_file', filename)):
#             return send_from_directory('static/upload_file', filename, as_attachment=True)
#         abort(404)

# @app.route('/base')
# def base():
#     # 增加数据
#     # 增加：
#     hydrology_data1 = Hydrology_data(
#                      data_route='/static/upload_file/201812002.txt',
#                      data_name='201812002',
#                      data_time='2019-04-05 16:21:41',
#                      data_format='.txt',
#                      data_kind='波浪和风场数据',
#                      data_refresh='月更新',
#                     )
#     db.session.add(hydrology_data1)
#     # 事务
#     db.session.commit()
#     return render_template('base.html', title_name='海洋数据平台')


@app.route('/index')
def index():
    context = {
        'banners': Banner.query.order_by('id').all()
    }
    return render_template('index.html', **context)


@app.route('/marine_organism', methods=['GET', 'POST'])
def marine_organism():
    if request.method == 'GET':
        context = {
            'marine_organisms': Marine_organism.query.order_by('id').all()
        }
        return render_template('marine_organism.html', **context)
    else:
        # 获取用户输入的关键字
        key_word = request.form.get('key_word')
        # 将关键字拼接成模糊字段
        args = '%' + key_word + '%'
        marine_organism_search = Marine_organism.query.filter(Marine_organism.data_set_name.like(args)).all()
        context = {
            'marine_organisms': marine_organism_search
        }
        return render_template('marine_organism.html', **context)


# 单个海洋生物数据集的展示页面
@app.route('/marine_organism_one/<marine_organism_id>/', methods=['GET', 'POST'])
def organism_one(marine_organism_id):
    # 如果是正常的加载当前页面
    if request.method == 'GET':
        marine_organism_one = Marine_organism.query.filter(Marine_organism.id == marine_organism_id).first()
        # 根据数据集的归属类型，查询到所有属于本数据集的所有数据
        organism_data = Organism_data.query.filter(Organism_data.organism_data_kind == marine_organism_one.data_set_name).all()
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
        organism_datas = Organism_data.query.filter(Organism_data.organism_data_name.like(args)).all()
        context = {
            'marine_organism_one': marine_organism_one,
            'organism_datas': organism_datas
        }
        return render_template('marine_organism_one.html', **context)


# 如果点击的是下载按钮，则进行文件下载
@app.route('/organism_one_download/file_name:<filename>', methods=['GET', 'POST'])
def organism_one_download(filename):
        print(filename)
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
        print(key_word)
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
        print(marine_hydrology_one.data_set_name)
        hydrology_data = Hydrology_data.query.filter(
            Hydrology_data.data_kind == marine_hydrology_one.data_set_name).all()
        context = {
            'marine_hydrology_one': marine_hydrology_one,
            'hydrology_datas': hydrology_data
        }
        return render_template('marine_hydrology_one.html', **context)


# 装饰函数，运行在最前面
@app.before_request
def before_request():
    myglobal.set_value("")


if __name__=='__main__':
    app.run()

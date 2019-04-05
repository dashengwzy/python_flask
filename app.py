from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from exts import db
from models import Banner
from models import Marine_organism
import config

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(config)
db.init_app(app)

# 新建一个Banner模型，采用models分开的方式
# flask-scrpts的方式


@app.route('/base')
def base():
    # 增加数据
    # 增加：
    # marine_organism1 = Marine_organism(
    #                  route='/static/images/qq.jpg',
    #                  data_set_name='COPEPOD海洋生物数据集',
    #                  data_set_size='103M',
    #                  data_set_source='美国国家海洋渔业中心海岸带与海洋浮游生态、生产和观测数据库。',
    #                  )
    # db.session.add(marine_organism1)
    # # 事务
    # db.session.commit()
    # banner1 = Banner.query.filter(Banner.id == 1).first()
    # img_route = banner1.route
    return render_template('base.html', title_name='海洋数据平台')


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
        print(context)
        return render_template('marine_organism.html', **context)
    else:
        key_word = request.form.get('key_word')
        args = '%' + key_word + '%'
        marine_organism_search = Marine_organism.query.filter(Marine_organism.data_set_name.like(args)).all()
        context = {
            'marine_organisms': marine_organism_search
        }
        print(context)
        return render_template('marine_organism.html', **context)



# @app.route('/form',methods = ['GET','POST'])
# def hello_form():
#     if request.method == 'POST':
#      name = request.form.get('name')
#      print(name)_
#      return render_template('post_test.html', name=name)
#     else:
#      return render_template('post_test.html')


if __name__ == '__main__':
    app.run()

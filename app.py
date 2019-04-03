from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from exts import db
from models import Banner

import config

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(config)
db.init_app(app)

# 新建一个Banner模型，采用models分开的方式
# flask-scrpts的方式


@app.route('/base')
def add():
    #增加数据
    # # 增加：
    # banner1 = Banner(title='第一个轮播图_海洋生物',
    #                  route='/static/images/banner1.jpg',
    #                  main_title='海洋生物',
    #                  vice_title_one='海洋生物数据集覆盖美国近海、日本东部、爱尔兰、澳大利亚等海域',
    #                  vice_title_two='包括浮游动物、浮游植物、初级生产力、鱼类、贝类等数据',
    #                  button_font='查看数据')
    # banner2 = Banner(title='第二个轮播图_海洋水文',
    #                  route='/static/images/banner2.jpg',
    #                  main_title='海洋水文',
    #                  vice_title_one='通过台站、浮标、调查船等观测手段获取的海洋水文数据，覆盖全球海域',
    #                  vice_title_two='主要包括温度、盐度、波浪、水位及海流等要素',
    #                  button_font='查看数据')
    # banner3 = Banner(title='第三个轮播图_海底地形',
    #                  route='/static/images/banner2.png',
    #                  main_title='海底地形',
    #                  vice_title_one='海底地形数据集覆盖全球海洋、陆地的栅格高程地形数据',
    #                  vice_title_two='数据分辨率从5′、2′、1′、30″、15″不等',
    #                  button_font='查看数据')
    # db.session.add(banner1)
    # db.session.add(banner2)
    # db.session.add(banner3)
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


@app.route('/form',methods = ['GET','POST'])
def hello_form():
    if request.method == 'POST':
     name = request.form.get('name')
     print(name)
     return render_template('post_test.html', name=name)
    else:
     return render_template('post_test.html')


if __name__ == '__main__':
    app.run()

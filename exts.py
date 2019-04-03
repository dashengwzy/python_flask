#该文件用来存放构建数据库的操作


from flask_sqlalchemy import SQLAlchemy
#利用db创建模型，把所有模型都放在一个叫做modles的文件中
db = SQLAlchemy()

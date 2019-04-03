# 专门用来存放数据库命令

# Manager专门用来存放在终端写的脚本
from flask_script import Manager
# 做模型到表的迁移
# Flask-Migrate是用于处理SQLAlchemy数据库迁移的扩展工具。
# 当Model出现变更的时候，通过migrate去管理数据库变更。
from flask_migrate import Migrate, MigrateCommand
from app import app
from exts import db
# 把需要映射到数据库当中的模型导入，MigrateCommand就会读取导入的模型

from models import Banner

# init
# migrate
# upgrade
# 模型  ->  迁移文件  ->  表


manager = Manager(app)

# 创建migrate实例，第一个参数是Flask的实例，第二个是sqlalchemy的数据库实例
# 使用Migrate绑定app和db
migrate = Migrate(app,  db)

# manager是Flask-Script的实例，这条语句在flask_script中添加了一个db命令
# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()

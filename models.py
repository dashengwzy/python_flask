#专门用来定义数据模型

from exts import db

# 创建banner模型，然后要将模型映射到数据库的表当中
class Banner(db.Model):
    __tablename__ = 'banner'
    # 图片的主键ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 图片的描述信息
    title = db.Column(db.String(100), nullable=False)
    # 图片存放的路径
    route = db.Column(db.String(100),  nullable=False)
    # 轮播图主标题
    main_title = db.Column(db.String(100), nullable=False)
    # 轮播图第一行内容
    vice_title_one = db.Column(db.String(100), nullable=False)
    # 轮播图第二行内容
    vice_title_two = db.Column(db.String(100), nullable=False)
    # 轮播图按钮文字
    button_font = db.Column(db.String(100), nullable=False)
    # 按钮跳转链接
    button_link = db.Column(db.String(1000), nullable=False)
    
    
# 创建海洋生物数据集模型，然后利用manage插件将模型映射到数据库的表当中
class Marine_organism(db.Model):
    __tablename__ = 'marine_organism'
    # 海洋生物图片的主键ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 海洋生物数据集图片存放的路径
    route = db.Column(db.String(100),  nullable=False)
    # 海洋生物数据集名称
    data_set_name = db.Column(db.String(100), nullable=False)
    # 海洋生物数据集大小
    data_set_size = db.Column(db.String(100), nullable=False)
    # 海洋生物数据集来源
    data_set_source = db.Column(db.String(1000), nullable=False)
    # 海洋生物数据集时间范围
    data_set_time_frame = db.Column(db.String(100), nullable=False)
    # 海洋生物数据集空间位置
    data_set_loc = db.Column(db.String(100), nullable=False)
    # 海洋生物数据集摘要
    data_set_abstract = db.Column(db.String(10000), nullable=False)


# 创建海洋生物数据集表格对象，然后利用manage插件将模型映射到数据库的表当中
class Organism_data(db.Model):
    __tablename__ = 'organism_data'
    # 海洋生物数据集表格的主键ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 海洋生物数据集表格数据本身在文件夹存储的位置
    organism_data_route = db.Column(db.String(100), nullable=False)
    # 海洋生物数据集表格数据名称
    organism_data_name = db.Column(db.String(100),  nullable=False)
    # 海洋生物数据集上传时间
    organism_data_time = db.Column(db.DateTime, nullable=False)
    # 海洋生物数据集数据格式
    organism_data_format = db.Column(db.String(100), nullable=False)
    # 海洋生物数据集表格所属门类
    organism_data_kind = db.Column(db.String(100), nullable=False)


# 创建海洋生物数据集模型，然后利用manage插件将模型映射到数据库的表当中
class Marine_hydrology(db.Model):
    __tablename__ = 'marine_hydrology'
    # 海洋水文图片的主键ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 海洋水文数据集图片存放的路径
    route = db.Column(db.String(100),  nullable=False)
    # 海洋水文数据集名称
    data_set_name = db.Column(db.String(100), nullable=False)
    # 海洋水文数据集大小
    data_set_size = db.Column(db.String(100), nullable=False)
    # 海洋水文数据集来源
    data_set_source = db.Column(db.String(1000), nullable=False)
    # 海洋水文数据集时间范围
    data_set_time_frame = db.Column(db.String(100), nullable=False)
    # 海洋水文数据集空间位置
    data_set_loc = db.Column(db.String(100), nullable=False)
    # 海洋水文数据集摘要
    data_set_abstract = db.Column(db.String(10000), nullable=False)

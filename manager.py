from flask_shop import create_app,db
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager



app = create_app('develop')

# 初始化命令管理器
manager = Manager(app)
manager.add_command('db',MigrateCommand)

# 初始化迁移工具
migrate = Migrate(app,db)
'''
python manager.py db init  # 初始化迁移环境

python manager.py db migrate # 生成迁移脚本

python manager.py db upgrade # 执行迁移(将脚本应用到数据库)

!!!:main函数里必须是manager.run()
'''

@app.route('/')
def index():
    return 'Hello'

if __name__ == '__main__':
    app.run(port=app.config['PORT'])
    # python manager.py runserver --port=8088
    # manager.run()
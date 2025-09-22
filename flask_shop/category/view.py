from flask import request
from flask_shop.category import category,category_api    # 导入蓝图,Api实例
from flask_shop import models,db
from flask_restful import Resource
from flask_shop.utils.message import to_dict_msg


class Category(Resource):
    """
    Category类提供了对商品类别的增删改查接口
    """
    def post(self):
        """
        处理POST请求,用于添加新的商品类别
        :return: JSON格式响应信息
        """
        try:
            # 从表单获取并处理name,level,pid参数
            name = request.form.get('name').strip() if request.form.get('name').strip() else ''
            level = int(request.form.get('level').strip()) if request.form.get('level').strip() else None
            pid = int(request.form.get('pid').strip()) if request.form.get('pid') else None
            # 验证name和level是否都存在
            if all([name,level]):
                # 使用表单传递的数据创建新的Category对象
                c = models.Category(name=name,level=level,pid=pid)
                # 将新对象添加到数据库会话中
                db.session.add(c)
                # 提交事务以保存更改
                db.session.commit()
                # 返回成功响应
                return to_dict_msg(200,msg='增加商品类别成功')
            # 如果name或者level为空,返回错误响应
            return to_dict_msg(10002)

        except Exception as e:
            # 发生异常时返回错误响应
            return to_dict_msg(20000)

    def get(self):
        """
        处理GET请求,用户获取指定ID的商品类别信息
        :return: JSON响应信息
        """
        try:
            # 从请求参数中获取分类ID
            cid = request.args.get('cid')
            # 根据分类ID查询数据库
            c = models.Category.query.get(cid)
            if c:
                # 如果找到分类对象,返回其字典格式数据和查找成功响应信息
                return to_dict_msg(200,c.to_dict(),'获取商品分类信息成功')
            else:
                # 如果分类不存在,返回错误响应
                return to_dict_msg(status=10019)

        except Exception as e:
            # 发生异常时返回错误响应
            return to_dict_msg(20000)

    def put(self):
        """
        处理PUT请求,用于更新商品分类信息
        接收分类ID和新名称,验证后更新数据库中对应的名称
        :return: JSON响应信息
        """
        try:
            # 从表单中获取分类ID和新名称
            cid = request.form.get('cid')
            name = request.form.get('name')
            # 根据id查询对应的数据
            c = models.Category.query.get(cid)
            # 判断分类是否存在
            if c:
                # 如果提供了新的名称,则更新分类名称,否则保持原名称不变
                if name is not None:
                    c.name = name
                # 提交事务,将修改保存到数据库
                db.session.commit()
                return to_dict_msg(status=200,msg='更新商品分类信息成功!!!')
            # 若分类不存在,返回错误信息:数据不存在
            return to_dict_msg(status=10019)
        except Exception as e:
            return to_dict_msg(20000)

    def delete(self):
        """
        处理DELETE请求,用于删除指定ID的商品信息
        :return: JSON响应信息
        """
        try:
            # 从表单中获取分类ID
            cid = request.form.get('cid')
            # 如果传递的表单数据ID不为空,则查找该数据
            if cid is not None:
                c = models.Category.query.get(cid)
            # 如果分类ID为空,返回错误码和消息:数据不完整
            else:
                return to_dict_msg(10002)
            # 如果查找到分类信息,执行删除操作
            if c:
                db.session.delete(c)
                db.session.commit()
                return to_dict_msg(200,msg='删除商品分类成功')

        except Exception as e:
            # 发生异常时返回错误响应
            return to_dict_msg(20000)

# 将Category资源添加到API路由
category_api.add_resource(Category,'/category')



@category.route('/category_list')
def get_category_list():

    level = int(request.args.get('level')) if request.args.get('level') and int(request.args.get('level'))<=3  else 0
    pnum = int(request.args.get('pnum')) if request.args.get('pnum') else 0
    psize = int(request.args.get('psize')) if request.args.get('psize') else 0

    # 存储返回的数据
    cate_list = []
    base_query = models.Category.query.filter(models.Category.level==1)

    # 如果pnum,prize都不为空,则进行分页查询
    if all([pnum,psize]):
        categories = base_query.paginate(pnum,psize)
        if level:
            cate_list = get_tree(categories.items,level,True)
        else:
            cate_list = get_tree(categories.items,level,False)
        data = {
            'data':cate_list,
            'pnum':pnum,
            'psize':psize,
            'total':categories.total
        }
        return to_dict_msg(200,data=data,msg='获取商品分类列表成功')
    # 否则进行不分页查询
    else:
        # 查询并存储所有的一级分类
        categories = base_query.all()
        if level:
            cate_list = get_tree(categories,level,flag=True)
        else:
            cate_list = get_tree(categories,level,flag=False)
            # # 遍历所有的一级分类
            # for c in categories:
            #     # 将所有的一级分类转换格式为JSON
            #     f_dict = c.to_dict()
            #     # f_dict的children用于存储二级分类
            #     f_dict['children'] = []
            #     # 遍历二级分类
            #     for sc in c.children:
            #         # 将二级分类转换格式
            #         s_dict = sc.to_dict()
            #         # s_dict的children用于存储三级分类
            #         s_dict['children'] = []
            #         # 遍历三级分类
            #         for tc in sc.children:
            #             # 将三级分类添加到二级分类的children
            #             s_dict['children'].append(tc.to_dict())
            #         # 将二级分类添加到一级分类
            #         f_dict['children'].append(s_dict)
            #     # 将所有的一级分类存储
            #     cate_list.append()

        return to_dict_msg(200,{'data':cate_list},msg='获取商品分类列表成功')


def get_tree(info_list,level,flag):
    """
    递归生成层级目录的嵌套字典结构(适配前端树形展示)
    :param info_list:待处理的目录列表
    :param level:层级
    :param flag: 层级过滤规则开关
    :return:info_dict---嵌套字典列表,每个字典包含目录信息和children子目录信息
    """
    # 初始化存储最终嵌套结构的列表
    info_dict = []
    # 先判断输入的目录列表是否为空,为空则直接返回空列表(递归终止条件)
    if info_list:
        # 遍历目录列表中的每个目录实例
        for i in info_list:
            # 将当前目录转换为字典
            i_dict = i.to_dict()
            # 根据flag选择不同的层级过滤规则,递归获取子目录
            if flag:
                # 当目录层级<level时,递归获取子目录
                # 例:level=3,flag=True,保留1,2级目录,且为1,2级目录添加子目录
                if i.level < level:
                    i_dict['children'] = get_tree(i.children, level,flag)
            else:
                # 当前目录!=3时,递归获取子目录
                # 例:flag=False,保留1、2级目录，为其添加子目录；3级目录不添加子目录
                if i.level != 3:
                    i_dict['children'] = get_tree(i.children,level,flag)
            # 将处理完成的当前目录字典添加到结果列表
            info_dict.append(i_dict)
    # 返回最终的嵌套层级结构
    return info_dict


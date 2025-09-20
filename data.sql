insert into t_menu (id,name,level) value(1,'全部',0);
insert into t_menu (id,name,level,pid) value(2,'用户管理',1,1);
insert into t_menu (id,name,level,pid) value(3,'权限管理',1,1);
insert into t_menu (id,name,level,pid) value(4,'商品管理',1,1);
insert into t_menu (id,name,level,pid) value(5,'订单管理',1,1);
insert into t_menu (id,name,level,pid) value(6,'数据统计',1,1);
insert into t_menu (id,name,level,pid,path) value(21,'用户列表',2,2,'/user_list');
insert into t_menu (id,name,level,pid,path) value(31,'角色列表',2,3,'/auther_list');
insert into t_menu (id,name,level,pid,path) value(32,'权限列表',2,3,'/role_list');
insert into t_menu (id,name,level,pid,path) value(41,'商品列表',2,4,'/product_list');
insert into t_menu (id,name,level,pid,path) value(43,'分类列表',2,4,'/group_list');


INSERT INTO t_user (name, pwd, nick_name, phone, email) VALUES
('liubei', 'pbkdf2:sha256:150000$wGIxZQcx$dde239f50b5e71cbbec37b284ced22eb1f2046e57a181024195c2aee4877a101', '刘备', '13800138001', 'liubei@shuguo.com'),
('zhugeliang', 'pbkdf2:sha256:150000$xHJy2Rkz$a8d3c7e9f2b4567890a1234567890abcdef1234567890abcdef1234567890ab', '诸葛亮', '13800138002', 'zhugeliang@shuguo.com'),
('guanyu', 'pbkdf2:sha256:150000$yKzl3Tqw$b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b', '关羽', '13800138003', 'guanyu@shuguo.com'),
('zhangfei', 'pbkdf2:sha256:150000$zLm4Uvx$c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0', '张飞', '13800138004', 'zhangfei@shuguo.com'),
('zhaoyun', 'pbkdf2:sha256:150000$AOp5Vwy$d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1', '赵云', '13800138005', 'zhaoyun@shuguo.com'),
('caocao', 'pbkdf2:sha256:150000$BQq6Wxz$e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2', '曹操', '13800138006', 'caocao@weiguo.com'),
('simayi', 'pbkdf2:sha256:150000$CRr7Xya$f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3', '司马懿', '13800138007', 'simayi@weiguo.com'),
('guojia', 'pbkdf2:sha256:150000$DSs8Yzb$a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4', '郭嘉', '13800138008', 'guojia@weiguo.com'),
('zhangliao', 'pbkdf2:sha256:150000$ETt9Zac$b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5', '张辽', '13800138009', 'zhangliao@weiguo.com'),
('sunquan', 'pbkdf2:sha256:150000$FUu0Abd$c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6', '孙权', '13800138010', 'sunquan@wuguo.com'),
('zhouyu', 'pbkdf2:sha256:150000$GVv1Bce$d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7', '周瑜', '13800138011', 'zhouyu@wuguo.com'),
('lusu', 'pbkdf2:sha256:150000$HWw2Cdf$e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8', '鲁肃', '13800138012', 'lusu@wuguo.com'),
('lumeng', 'pbkdf2:sha256:150000$IXx3Deg$f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9', '吕蒙', '13800138013', 'lumeng@wuguo.com'),
('machao', 'pbkdf2:sha256:150000$JYy4Efh$a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0', '马超', '13800138014', 'machao@shuguo.com'),
('huangzhong', 'pbkdf2:sha256:150000$KZz5Fgi$b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1', '黄忠', '13800138015', 'huangzhong@shuguo.com'),
('dianwei', 'pbkdf2:sha256:150000$LAA6Ghj$c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2', '典韦', '13800138016', 'dianwei@weiguo.com'),
('xuchu', 'pbkdf2:sha256:150000$MBB7Hik$d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3', '许褚', '13800138017', 'xuchu@weiguo.com'),
('luxun', 'pbkdf2:sha256:150000$NCC8Jjl$e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4', '陆逊', '13800138018', 'luxun@wuguo.com'),
('taishici', 'pbkdf2:sha256:150000$ODD9Kkm$f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5', '太史慈', '13800138019', 'taishici@wuguo.com'),
('jiangwei', 'pbkdf2:sha256:150000$PEE0Lnn$a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6', '姜维', '13800138020', 'jiangwei@shuguo.com');








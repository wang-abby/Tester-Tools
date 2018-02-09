#coding: utf-8
class DBRouter(object):
	"""根据用户输入的搜索Id，动态选择所在的库
		根据店铺查询所属库及表：select
		floor(mod(26822, 1024) / 32)
		db_num, mod(mod(26822, 1024), 32)
		tab_num;

	"""
	def get_db(self,id):
		db = (id % 1024) // 32
		return db
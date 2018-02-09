#coding:utf-8

from __future__ import unicode_literals

from django.db import models
from django.db.models.base import ModelBase

# Create your models here.

class OrdersInfo(models.Model):
	order_id = models.CharField(primary_key=True,max_length=64)
	shop_id = models.IntegerField()
	order_time = models.DateField()
	order_status = models.IntegerField()
	consumer_id = models.IntegerField()
	channel_id = models.IntegerField()

	# 动态选择要查询的数据库
	def get_db(self, id):
		db = (id % 1024) // 32
		return db

	# 动态选择要查询的数据表
	@classmethod
	def get_sharding_table(cls, id=None):

		piece = (id % 1024) % 32
		if len(str(piece)) <= 4:
			piece = '0' * (4 - len(str(piece))) + str(piece)
		else:
			piece = str(piece)
		return cls._meta.db_table + piece

	@classmethod
	def sharding_get(cls, id=None, **kwargs):
		#assert isinstance(id, int), 'id must be integer!'
		table = cls.get_sharding_table(id)
		print "=======",table
		sql = "SELECT * FROM %s" % table
		#kwargs['id'] = id
		print "sql",sql
		condition = ' AND '.join([k + '=%s' for k in kwargs])
		print "condition:",condition
		params = [str(v) for v in kwargs.values()]
		print "params:", params
		where = " WHERE " + condition % params[0]
		searchSql = sql + where
		#print "searchSql",sql + where
		print "searchSql",searchSql
		try:
			return cls.objects.raw(searchSql)
			#return cls.objects.raw(sql + where, params=params)#[0]  # the5fire:这里应该模仿Queryset中get的处理方式
		except IndexError:
			# the5fire:其实应该抛Django的那个DoesNotExist异常
			return 'id must be integer!'#None

	@classmethod
	def sharding_listAll(cls, id=None):
		#assert isinstance(id, int), 'id must be integer!'
		table = cls.get_sharding_table(id)
		sql = "SELECT * FROM %s" % table
		try:
			return cls.objects.raw(sql)  # the5fire:这里应该模仿Queryset中get的处理方式
		except IndexError:
			# the5fire:其实应该抛Django的那个DoesNotExist异常
			return None
	class Meta:
		#managed = False
		db_table = 't_order_shop_'
		app_label = 'ordersInfo'

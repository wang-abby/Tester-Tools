#coding:utf-8
from django.utils.encoding import force_unicode,smart_unicode, smart_str, DEFAULT_LOCALE_ENCODING
from django.shortcuts import render

from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect,JsonResponse,FileResponse

from django.template import loader
from .models import OrdersInfo
from django.views.decorators.cache import never_cache
from django.db import connections
# Create your views here.

"""
#获取输入值
def get_searchId(request):
	warning = ''

	searchId
	searchId = request.GET.get("searchId")

	if searchId is None:
		warning = '没有订单数据！'
	else:
		searchId = int(searchId)
	print "-----",searchId,warning
	return searchId
"""

#@never_cache
def get_orders(request):
	t = loader.get_template('orderInfo.html')
	context = {}
	warning = ''
	orders = ''
	searchId = request.GET.get("searchId")
	queryType = request.GET.get("queryType")
	db = ''
	if searchId is None:
		warning = '没有订单数据！'
	else:
		searchId = int(unicode(searchId))
#动态计算要连接的数据库
		db = (searchId % 1024) // 32
		print "db=", db
		if (db // 8) == 0:
			connections.databases['used_db'] = {'ENGINE': 'django.db.backends.mysql',
												'HOST': '114.55.86.172',
												'PORT': '3316',
												'NAME': 'order_000' + str(db),
												'USER': 'orderopr',
												'PASSWORD': 'Yjaa#1234',
												'AUTOCOMMIT': True,
												'ATOMIC_REQUESTS': False,
												'CONN_MAX_AGE': 0,
												'OPTIONS': {},
												'TEST': {'CHARSET': 'utf-8',
														 'COLLATION': None,
														 'MIRROR': None,
														 'NAME': None},
												'TIME_ZONE': None,
												}

		elif (db // 8) == 1:
			if db < 10:
				connections.databases['used_db'] = {'ENGINE': 'django.db.backends.mysql',
													'HOST': '114.55.86.172',
													'PORT': '3317',
													'NAME': 'order_000' + str(db),
													'USER': 'orderopr',
													'PASSWORD': 'Yjaa#1234',
													'AUTOCOMMIT': True,
													'ATOMIC_REQUESTS': False,
													'CONN_MAX_AGE': 0,
													'OPTIONS': {},
													'TEST': {'CHARSET': 'utf-8',
															 'COLLATION': None,
															 'MIRROR': None,
															 'NAME': None},
													'TIME_ZONE': None,
													}
			else:
				connections.databases['used_db'] = {'ENGINE': 'django.db.backends.mysql',
													'HOST': '114.55.86.172',
													'PORT': '3317',
													'NAME': 'order_00' + str(db),
													'USER': 'orderopr',
													'PASSWORD': 'Yjaa#1234',
													'AUTOCOMMIT': True,
													'ATOMIC_REQUESTS': False,
													'CONN_MAX_AGE': 0,
													'OPTIONS': {},
													'TEST': {'CHARSET': 'utf-8',
															 'COLLATION': None,
															 'MIRROR': None,
															 'NAME': None},
													'TIME_ZONE': None,
													}

		elif (db // 8) == 2:
			connections.databases['used_db'] = {'ENGINE': 'django.db.backends.mysql',
												'HOST': '114.55.86.136',
												'PORT': '3318',
												'NAME': 'order_00' + str(db),
												'USER': 'orderopr',
												'PASSWORD': 'Yjaa#1234',
												'AUTOCOMMIT': True,
												'ATOMIC_REQUESTS': False,
												'CONN_MAX_AGE': 0,
												'OPTIONS': {},
												'TEST': {'CHARSET': 'utf-8',
														 'COLLATION': None,
														 'MIRROR': None,
														 'NAME': None},
												'TIME_ZONE': None,
												}

		elif (db // 8) == 3:
			connections.databases['used_db'] = {'ENGINE': 'django.db.backends.mysql',
												'HOST': '114.55.86.136',
												'PORT': '3319',
												'NAME': 'order_00' + str(db),
												'USER': 'orderopr',
												'PASSWORD': 'Yjaa#1234',
												'AUTOCOMMIT': True,
												'ATOMIC_REQUESTS': False,
												'CONN_MAX_AGE': 0,
												'OPTIONS': {},
												'TEST': {'CHARSET': 'utf-8',
														 'COLLATION': None,
														 'MIRROR': None,
														 'NAME': None},
												'TIME_ZONE': None,
												}
		else:
			name = 'order_' + str(db)
			raise Exception("The connection %s doesn't exist" % name)

#查询数据
		if queryType == 'shop':
			#orders = OrdersInfo.objects.filter(shop_id=searchId)
			orders = OrdersInfo.sharding_get(id=searchId,shop_id=searchId).using('used_db')
			print "length = ",len(list(orders))
		elif queryType == 'consumer':
			#orders = OrdersInfo.objects.filter(consumer_id=searchId)
			orders = OrdersInfo.sharding_get(id=searchId,consumer_id=searchId).using('used_db')
		else:
			orders = OrdersInfo.sharding_get(id=searchId).using('used_db')

		if len(list(orders)) == 0:#orders is None:
			warning = '该用户没有订单数据！'
		else:
			pass
	print "databases = ",connections.databases['used_db']
	context = {'orders': orders, 'warning': smart_unicode(warning)}
	html = t.render(context)
	return HttpResponse(html)


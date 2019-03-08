'''
CREATE TABLE IF NOT EXISTS `jd_bread`(
	item_id VARCHAR(100) NOT NULL,
	item_fullName VARCHAR(100) NOT NULL,
	item_name VARCHAR(100) NOT NULL,
	item_price VARCHAR(100) NOT NULL,
	item_brand VARCHAR(100) NOT NULL,
	gross_weight VARCHAR(100) NOT NULL,
	item_origin VARCHAR(100) NOT NULL,
	item_certification VARCHAR(100) NOT NULL,
	processing_technology VARCHAR(100) NOT NULL,
	packing_unit VARCHAR(100) NOT NULL,
	is_suger VARCHAR(100) NOT NULL,
	item_taste VARCHAR(100) NOT NULL,
	storage_condition VARCHAR(100) NOT NULL,
	item_classification VARCHAR(100) NOT NULL,
	cookie_classification VARCHAR(100) NOT NULL,
	item_package VARCHAR(100) NOT NULL,
	applicable_people VARCHAR(100) NOT NULL,
	cake_classification VARCHAR(100) NOT NULL,
	item_QGP VARCHAR(100) NOT NULL
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

'''


import pymysql

def saver(result):
    db = pymysql.connect("localhost", "root", "root", "jd", charset="utf8")
    cursor = db.cursor()
    print('准备插入...')
    sql = "INSERT INTO jd.jd_bread (item_id,item_fullName,item_name,item_price,item_brand,gross_weight,item_origin,\
    item_certification,processing_technology,packing_unit,is_suger,item_taste,storage_condition,item_classification,\
    cookie_classification,item_package,applicable_people,cake_classification,item_QGP) VALUES (%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,\
    %r,%r,%r,%r,%r,%r,%r);" % (
    result['item_id'], result['item_fullName'], result['item_name'], result['item_price'], result['item_brand'],
    result['gross_weight'], result['item_origin'], result['item_certification'], result['processing_technology'],
    result['packing_unit'],
    result['is_suger'], result['item_taste'], result['storage_condition'], result['item_classification'],
    result['cookie_classification'],
    result['item_package'], result['applicable_people'], result['cake_classification'], result['item_QGP'])

    cursor.execute(sql)
    db.commit()
    db.close()

if __name__ == '__main__':
    result = {'item_id': '5097736', 'item_fullName': '三只松鼠手撕面包饼干蛋糕零食大礼包酵母面包早餐口袋软面包礼盒1000g/盒', 'item_name': '三只松鼠面包', 'item_price': '29.80', 'item_brand': 'npl', 'gross_weight': '1.42kg', 'item_origin': '安徽省合肥市', 'item_certification': '其它', 'processing_technology': '其它', 'packing_unit': '箱装', 'is_suger': '含糖', 'item_taste': '原味', 'storage_condition': '常温', 'item_classification': '面包', 'cookie_classification': '其它', 'item_package': '礼盒装', 'applicable_people': '休闲娱乐', 'cake_classification': '西式糕点', 'item_QGP': '180天'}
    saver(result)
import pyodbc
from lxml import etree
from application import connect_db


class ConvertToXml():

	def sql_row_to_xml(sql):
		#создаем рутовый элемент
		NewDataSet = etree.Element("NewDataSet")
		#подключаемся к базе и выполняем хранимку
		try:
			cursor = connect_db.cursor()
			cursor.execute(sql)
			# проверяем наличие полей
			if cursor.description is None: 
				index_table = 0
				while cursor.nextset():
					# проверяем наличие полей иначе пропускаем итерацию
					if cursor.description is None: continue
					# переносим названия полей в кортеж
					colnames = tuple([desc[0] for desc in cursor.description])
					# формируем xml
					for row in cursor.fetchall():
						#если индекс ноль то формируем первый тег table без суффикса
						if index_table == 0:
							table = etree.SubElement(NewDataSet, "Table")
						else:
							table = etree.SubElement(NewDataSet, "Table" + str(index_table))
						#выводим данные из массива
						for index,data_row in enumerate(colnames):
							table_row = etree.SubElement(table, data_row)
							#проверяем, если пустое поле записываем пустую строку
							if row[index] is None:
								table_row.text = ''
							else:
								table_row.text = str(row[index])
					# прибавляем 1 к индексу
					index_table = index_table + 1
			else:
				# переносим названия полей в кортеж
				colnames = tuple([desc[0] for desc in cursor.description])
				# формируем xml
				for row in cursor.fetchall():
					table = etree.SubElement(NewDataSet, "Table")
					#выводим данные из массива
					for index,data_row in enumerate(colnames):
						table_row = etree.SubElement(table, data_row)
						#проверяем, если пустое поле записываем пустую строку
						if row[index] is None:
							table_row.text = ''
						else:
							table_row.text = str(row[index])
				index_table = 1
				while cursor.nextset():
						# проверяем наличие полей иначе пропускаем итерацию
						if cursor.description is None: continue
						# переноси названия полей в кортеж
						colnames = tuple([desc[0] for desc in cursor.description])
						# формируем xml
						for row in cursor.fetchall():
							table = etree.SubElement(NewDataSet, "Table" + str(index_table))
							#выводим данные из массива
							for index,data_row in enumerate(colnames):
								table_row = etree.SubElement(table, data_row)
								#проверяем, если пустое поле записываем пустую строку
								if row[index] is None:
									table_row.text = ''
								else:
									table_row.text = str(row[index])
						index_table = index_table + 1
		except pyodbc.Error as err:
			#если произошла ошибка в базе то возвращаем её
			NewDataSet = "Ошибка в основной базе:" + str(err)
		
		
		return NewDataSet
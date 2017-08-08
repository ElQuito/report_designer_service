import pyodbc
from application import connect_db,connect_db_lite 
from application.lib.ConvertToXml import ConvertToXml
import lxml.etree as ET
from lxml import etree
from datetime import datetime, date, time, timedelta


#класс формирования отчёта
class Report():
	
	def report_proc(self,request,proc_name,row_fields):
		#создаем переменную с пустым преобразованием
		empty_xslt = '<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"></xsl:stylesheet>'
		#формируем строку вызова процедуры
		proc_string = ''
		for row in row_fields:
			proc_string = proc_string + "@" + str(row.name) + " = '" + str(request.args.get(row.name)) + "' "
			#проверяем что это последний элемент и не добавляем запятую
			if len(row_fields) != row_fields.index(row) + 1:
				proc_string = proc_string + ", "
		#создаем объект xml из метода класса ConvertToXml
		xml_result = ConvertToXml.sql_row_to_xml("EXEC [dbo].[" + proc_name.proc_name + "] "+ str(proc_string) +";")
		
		#проверяем если ошибка в базе то выводим сообщение
		if xml_result[0:22] != 'Ошибка в основной базе':
			#формируем дерево xml
			tree = ET.ElementTree(xml_result)
			#создаем переменную вывода ошибки
			error = ''
			#подгружаем xslt и преобразуем в зависимости от типа
			if proc_name.html_xsl != '':
				#проверяем на ошибку в преобразовании
				try:
					newdom_html =self.xml_xslt_transform(proc_name.html_xsl,tree)
				except etree.XMLSyntaxError as e:
					newdom_html = 'None'
					error = 'Ошибка в xslt преобразовании HTML:' + str(e)
			else:
				#если преобразование не загружено подставляем пустое преобразование
				newdom_html =self.xml_xslt_transform(empty_xslt,tree)
			if proc_name.excel_xsl != '':
				#проверяем на ошибку в преобразовании
				try:
					newdom_excel =self.xml_xslt_transform(proc_name.excel_xsl,tree)
				except etree.XMLSyntaxError as e:
					newdom_excel = 'None'
					error = 'Ошибка в xslt преобразовании EXCEL:' + str(e)
			else:
				#если преобразование не загружено подставляем пустое преобразование
				newdom_excel =self.xml_xslt_transform(empty_xslt,tree)
			if proc_name.word_xsl != '':
				#проверяем на ошибку в преобразовании
				try:
					newdom_word =self.xml_xslt_transform(proc_name.word_xsl,tree)
				except etree.XMLSyntaxError as e:
					newdom_word = 'None'
					error = 'Ошибка в xslt преобразовании WORD:' + str(e)
			else:
				#если преобразование не загружено подставляем пустое преобразование
				newdom_word =self.xml_xslt_transform(empty_xslt,tree)
		else:
			error = xml_result
			newdom_html = 'None'
			newdom_excel = 'None'
			newdom_word = 'None'

			
		return (newdom_html,newdom_excel,newdom_word,error)
		
	#метод генерации преобразования
	def xml_xslt_transform(self,content,tree):
		xslt = ET.XML(content.encode('utf-8'))
		transform = ET.XSLT(xslt)
		newdom = transform(tree)
		return ET.tounicode(newdom)
		
	#метод быстрого поиска	
	def search_proc(self,search,typedata):
		#вызываем хранимую процедуру для быстрого поиска	
		cursor = connect_db.cursor()
		cursor.execute("EXEC [dbo].[ddm_reporting_service_GetSearchList] @searchTerm = '"+str(search)+"', @typedata = '"+str(typedata)+"';")
		rows = cursor.fetchall()
		return rows
		
#класс получения настроек отчёта		
class Report_Settings(connect_db_lite.Model):
	__tablename__ = 'reports'
	id_reports = connect_db_lite.Column(connect_db_lite.Integer, primary_key = True)
	name = connect_db_lite.Column(connect_db_lite.Text)
	html_xsl = connect_db_lite.Column(connect_db_lite.Text)
	excel_xsl = connect_db_lite.Column(connect_db_lite.Text)
	word_xsl = connect_db_lite.Column(connect_db_lite.Text)
	proc_name = connect_db_lite.Column(connect_db_lite.Text)
	field_sort = connect_db_lite.Column(connect_db_lite.Text)
	def __repr__(self):
		return '<Report_Settings %r>' % (self.id_reports)
		
#класс получения полей отчёта		
class Report_Fields(connect_db_lite.Model):
	__tablename__ = 'fields_report'
	id_field = connect_db_lite.Column(connect_db_lite.Integer, primary_key = True)
	id_report = connect_db_lite.Column(connect_db_lite.Integer, connect_db_lite.ForeignKey('reports.id_reports'))
	name = connect_db_lite.Column(connect_db_lite.Text)
	type = connect_db_lite.Column(connect_db_lite.Text)
	label = connect_db_lite.Column(connect_db_lite.Text)
	def __repr__(self):
		return '<Report_Fields %r>' % (self.id_field)
		
#класс получения полей коллекций		
class Report_Fields_Collection(connect_db_lite.Model):
	__tablename__ = 'fields_collection'
	id_field_collection = connect_db_lite.Column(connect_db_lite.Integer, primary_key = True)
	id_field = connect_db_lite.Column(connect_db_lite.Integer, connect_db_lite.ForeignKey('fields_report.id_field'))
	value = connect_db_lite.Column(connect_db_lite.Text)
	label = connect_db_lite.Column(connect_db_lite.Text)
	def __repr__(self):
		return '<Report_Fields_Collection %r>' % (self.id_field_collection)
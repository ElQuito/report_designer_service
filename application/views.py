from flask import render_template, request, make_response, jsonify,redirect,url_for
from application import application,connect_db_lite
from application.models.model import Report,Report_Settings,Report_Fields,Report_Fields_Collection
from application.lib.CreateFields import CreateFields
from markupsafe import Markup

#основная страница
@application.route('/')
def index():
	reports = Report_Settings.query.all()
	return render_template('index.html',reports = reports)

#страница выбранного отчёта по id	
@application.route('/report/<id>/')
def report(id):
	#получам название отчёта
	report_name = Report_Settings.query.filter_by(id_reports=id).first()
	#получаем поля отчёта
	rows = Report_Fields.query.filter_by(id_report=id).all()
	#получаем коллекции
	field_collection = Report_Fields_Collection.query.join(Report_Fields, Report_Fields_Collection.id_field==Report_Fields.id_field).filter(Report_Fields.id_report == id)
	#формируем html поля
	result = CreateFields.Create_Html_Field(rows,field_collection)
	#переводим строку в список с сортировкой
	if report_name.field_sort is not None:
		field_sort = [int(x) for x in report_name.field_sort.split(',') if report_name.field_sort]
		# добавляем в список сортировки недостающие id если таковые имеются
		field_id = [row.id_field for row in rows]
		result_var=list(set(field_id) - set(field_sort))
		field_sort.extend(result_var)
	else:
		field_sort = 'сортировка отсутствует'
	return render_template('report.html',headers=result[0],fields=result[1],id=id,report_name=report_name,field_sort=field_sort) 

	
#страница выбранного отчёта по id без дизайна
@application.route('/only_report/<id>/')
def only_report(id):
	#получам название отчёта
	report_name = Report_Settings.query.filter_by(id_reports=id).first()
	#получаем поля отчёта
	rows = Report_Fields.query.filter_by(id_report=id).all()
	#получаем коллекции
	field_collection = Report_Fields_Collection.query.join(Report_Fields, Report_Fields_Collection.id_field==Report_Fields.id_field).filter(Report_Fields.id_report == id)
	#формируем html поля
	result = CreateFields.Create_Html_Field(rows,field_collection)
	#переводим строку в список с сортировкой
	if report_name.field_sort is not None:
		field_sort = [int(x) for x in report_name.field_sort.split(',') if report_name.field_sort]
		# добавляем в список сортировки недостающие id если таковые имеются
		field_id = [row.id_field for row in rows]
		result_var=list(set(field_id) - set(field_sort))
		field_sort.extend(result_var)
	else:
		field_sort = 'сортировка отсутствует'
	return render_template('headless/report.html',headers=result[0],fields=result[1],id=id,report_name=report_name,field_sort=field_sort)
	
#страница вывода результата отчёта	
@application.route('/report_result/<id>/', methods = ['GET'])
def report_result(id):
	#получам название хранимой процедуры
	proc_name = Report_Settings.query.filter_by(id_reports=id).first()
	#получаем поля
	row_fields = Report_Fields.query.filter_by(id_report=id).all()
	#создаем объект и получаем данные с хранимки
	rows = Report()
	rows = rows.report_proc(request,proc_name,row_fields)
	return render_template('report_result.html',html_content = Markup(rows[0]),excel_content=rows[1],word_content=rows[2],error=rows[3])
	
#страница вывода результата отчёта без дизайна	
@application.route('/only_report_result/<id>/', methods = ['GET'])
def only_report_result(id):
	#получам название хранимой процедуры
	proc_name = Report_Settings.query.filter_by(id_reports=id).first()
	#получаем поля
	row_fields = Report_Fields.query.filter_by(id_report=id).all()
	#создаем объект и получаем данные с хранимки
	rows = Report()
	rows = rows.report_proc(request,proc_name,row_fields)
	return render_template('headless/report_result.html',html_content = Markup(rows[0]),excel_content=rows[1],word_content=rows[2],error=rows[3])

#страница скачивания excel
@application.route('/upload_excel',methods = ['POST'])
def upload_excel():
	content = request.form['content_excel']
	#добавляем строку юникода
	xml_header_excel = u'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><?mso-application progid="Excel.Sheet"?>'
	response = make_response(xml_header_excel + content)
	#передаем заголовок для скачивания файла
	response.headers["Content-Disposition"] = "attachment; filename=report.xml"
	return response

#страница скачивания word	
@application.route('/upload_word',methods = ['POST'])
def upload_word():
	content = request.form['content_word']
	#добавляем строку юникода
	xml_header_word = u'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><?mso-application progid="Word.Document"?>'
	response = make_response(xml_header_word + content)
	#передаем заголовок для скачивания файла
	response.headers["Content-Disposition"] = "attachment; filename=report.xml"
	return response	

#страница быстрого поиска	
@application.route('/autocomplete', methods=['GET'])
def autocomplete():
	#быстрый поиск по справочникам
	typedata = request.args.get('typedata')
	search = request.args.get('q')
	rows = Report()
	rows = rows.search_proc(search,typedata)
	lrows = []
	for row in rows:
		lrows.append(list(row))
	return jsonify(matching_results=lrows)

	
#принимает параметры сортироки полей
@application.route('/field_sort', methods=['POST'])
def field_sort():
	#получам настройки отчёта
	report_settings = Report_Settings.query.filter_by(id_reports = request.form['report_id']).first()
	report_settings.field_sort=request.form['field_sort']
	connect_db_lite.session.commit()
	return 'ok!'

#админка для создания отчёта	
@application.route('/reports_admin', methods=['GET','POST'])
def reports_admin():
	if request.method == "POST":
		t = Report_Settings(name=request.form['name'], html_xsl=request.form['html_xsl'],excel_xsl=request.form['excel_xsl'],word_xsl=request.form['word_xsl'],proc_name=request.form['proc_name'])
		connect_db_lite.session.add(t)
		connect_db_lite.session.commit()
		return redirect(url_for('reports_admin'))
	else:
		reports = Report_Settings.query.all()
		return render_template('reports_admin.html',reports=reports)
		
		
#обновление отчёта
@application.route('/report_update/<id>/',methods=['GET','POST'])
def report_update(id):
	#получам настройки отчёта
	report_settings = Report_Settings.query.filter_by(id_reports = id).first()
	#получам все поля отчёта
	report_fields = Report_Fields.query.filter_by(id_report = id)
	#получам коллекции полей
	field_collection = Report_Fields_Collection.query.join(Report_Fields, Report_Fields_Collection.id_field==Report_Fields.id_field).filter(Report_Fields.id_report == id)
	#принимаем пост данные для обновления настроек отчёта
	if request.method == "POST" and 'form_update_settings' in request.form:
		report_settings.name=request.form['name']
		report_settings.html_xsl=request.form['html_xsl']
		report_settings.excel_xsl=request.form['excel_xsl']
		report_settings.word_xsl=request.form['word_xsl']
		report_settings.proc_name=request.form['proc_name']
		connect_db_lite.session.commit()
		return redirect(url_for('report_update',id = id))
	#принимаем пост данные для добавления нового поля
	elif request.method == "POST" and 'form_new_field' in request.form:
		t = Report_Fields(id_report=request.form['id_report'], name=request.form['name'],type=request.form['type'],label=request.form['label'])
		connect_db_lite.session.add(t)
		connect_db_lite.session.commit()
		return redirect(url_for('report_update',id = id))
	#принимаем пост данные для добавления коллекции
	elif request.method == "POST" and 'field_collection_add' in request.form:
		t = Report_Fields_Collection(id_field=request.form['id_field'], value=request.form['field_collection_value'],label=request.form['field_collection_label'])
		connect_db_lite.session.add(t)
		connect_db_lite.session.commit()
		return redirect(url_for('report_update',id = id))
	#принимаем пост данные для обновления поля
	elif request.method == "POST" and 'form_update_field' in request.form:
		#получам поле отчёта
		report_field = Report_Fields.query.filter_by(id_field = request.form['id_field_update']).first()
		report_field.name=request.form['name']
		report_field.type=request.form['type']
		report_field.label=request.form['label']
		connect_db_lite.session.commit()
		return redirect(url_for('report_update',id = id))
	#принимаем пост данные для обновления коллекции
	elif request.method == "POST" and 'field_collection_update' in request.form:
		report_field_collection = Report_Fields_Collection.query.filter_by(id_field_collection = request.form['id_field_collection']).first()
		report_field_collection.value=request.form['field_collection_value']
		report_field_collection.label=request.form['field_collection_label']
		connect_db_lite.session.commit()
		return redirect(url_for('report_update',id = id))
	else:
		#переводим строку в список с сортировкой
		if report_settings.field_sort is not None:
			field_sort = [int(x) for x in report_settings.field_sort.split(',') if report_settings.field_sort]
			# добавляем в список сортировки недостающие id если таковые имеются
			field_id = [row.id_field for row in report_fields]
			result_var=list(set(field_id) - set(field_sort))
			field_sort.extend(result_var)
		else:
			field_sort = 'сортировка отсутствует'
		return render_template('report_update.html',report_settings=report_settings,report_fields=report_fields,field_collection=field_collection,field_sort=field_sort)

		
#удаляем отчёт и поля и коллекций
@application.route('/report_remove',methods=['POST'])
def report_remove():
	if request.method == "POST":
		id_field_var = Report_Fields.query.filter_by(id_report=request.form['id_reports'])
		list_field_id = []
		for id_field_var_one in id_field_var:
			list_field_id.append(id_field_var_one.id_field)
		#удаляем коллекции
		Report_Fields_Collection.query.filter(Report_Fields_Collection.id_field.in_(list_field_id)).delete(synchronize_session='fetch')
		#удаляем поля
		Report_Fields.query.filter_by(id_report=request.form['id_reports']).delete()
		#удаляем отчёт
		Report_Settings.query.filter_by(id_reports=request.form['id_reports']).delete()
		#сохраняем
		connect_db_lite.session.commit()
		return redirect(url_for('reports_admin'))
		
#удаляем поле и коллекцию
@application.route('/field_remove/<id>/',methods=['GET','POST'])
def field_remove(id):
	if request.method == "POST":
		#удаляем коллекции
		Report_Fields_Collection.query.filter_by(id_field=request.form['id_field']).delete()
		#удаляем поля
		Report_Fields.query.filter_by(id_field=request.form['id_field']).delete()
		connect_db_lite.session.commit()
		return redirect(url_for('report_update',id = id))
		
#удаляем коллекцию
@application.route('/collection_remove/<id>/',methods=['GET','POST'])
def collection_remove(id):
	if request.method == "POST":
		#удаляем коллекции
		Report_Fields_Collection.query.filter_by(id_field_collection=request.form['id_field_collection']).delete()
		connect_db_lite.session.commit()
		return redirect(url_for('report_update',id = id))
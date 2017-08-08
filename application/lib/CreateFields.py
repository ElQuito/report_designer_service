from markupsafe import Markup
# класс генерации полей html
class CreateFields():

	def Create_Html_Field(rows,field_collection):
		headers = []
		fields = {}
		for row in rows:
			# поле дата
			if row.type == 'date':
				fields.update({row.id_field: Markup('<div class="row"><div class="col-xs-2"  align="right"><label>' + row.label + '</label></div><div class="col-xs-2"><div class="form-group"><div class="input-group date" id="' + row.name + '_div"><input type="text" class="form-control" name="' + row.name + '" id="' + row.name + '"/><span class="input-group-addon"><span class="glyphicon glyphicon-calendar"></span></span></div></div></div></div><script type="text/javascript">$(function () {$("#' + row.name + '_div").datetimepicker({locale: "ru",format: "YYYY-MM-DD"});});</script>') })
			# поле справочник: подразделений, сотрудников, справочник подразделений контрагента, сотрудник контрагент, справочник виды карточек, универсальный справочник
			if row.type == 'subdivision' or row.type == 'employees' or row.type == 'сompanies' or row.type == 'partners_employees' or row.type == 'ref_kinds_card_kinds' or row.type == 'ref_universal_item':
				fields.update({row.id_field:Markup("""<div class="row"><div class="col-xs-2"  align="right"><label>%s</label></div><div class="col-xs-6"><input name="%s" type="hidden" id="%s" /><input name="%s_field" type="text" id="%s_field" onkeypress="return add_select_option(event,this.value,document.getElementById('%s').value,'%s')" onkeyup="return add_select_option(event,this.value,document.getElementById('%s').value,'%s')" style="width:390px;margin-bottom:2px;"/></div></div><div class="row"><div class="col-xs-2"></div><div class="col-xs-4"><select size="4" id="%s_list" style="width:390px;height:110px;"></select><br/><br/></div><div class="col-xs-1"><button type="button" class="btn btn-default btn-sm" onclick="remove_select_option('%s')"><img src="/static/images/delete.gif"/></button></div></div><script type="text/javascript">$(document).ready(function () { showrow("#%s","%s") });</script>""" % (row.label, row.name,row.name,row.name,row.name,row.name,row.name,row.name,row.name,row.name,row.name,row.name,row.type))})
				headers.append(row.name)
			# поле да/нет
			if row.type == 'checkbox':
				fields.update({row.id_field:Markup('<div class="row"><div class="col-xs-2"  align="right"><label>' + row.label + '</label></div><div class="col-xs-1"><input type="checkbox" id="' + row.name + '" name="' + row.name + '" value="1" /></div></div>')})
			# поле переключатели
			if row.type == 'radio':
				input_string = ''
				for field_collection_one in field_collection:
					if field_collection_one.id_field == row.id_field:
						input_string = input_string + '<input name="' + row.name + '" type="radio" value="' + field_collection_one.value + '" checked /> '+ field_collection_one.label + ' '
				fields.update({row.id_field:Markup('<div class="row"><div class="col-xs-2"  align="right"><label>' + row.label + '</label></div><div class="col-xs-4">%s</div></div>' % (input_string))})
			# поле список
			if row.type == 'select':
				input_string = ''
				for field_collection_one in field_collection:
					if field_collection_one.id_field == row.id_field:
						input_string = input_string + '<option value="'+field_collection_one.value+'">'+ field_collection_one.label + '</option>'
				fields.update({row.id_field:Markup('<div class="row"><div class="col-xs-2"  align="right"><label>' + row.label + '</label></div><div class="col-xs-2"><select id="' + row.name + '" name="' + row.name + '" >%s</select></div></div>' % (input_string))})
			# поле поле
			if row.type == 'field_input':
				fields.update({row.id_field:Markup('<div class="row"><div class="col-xs-2"  align="right"><label>' + row.label + '</label></div><div class="col-xs-2"><input type="text" id="' + row.name + '" name="' + row.name + '" /></div></div>')})
		return (headers,fields)	
	// функция jquery ajax для быстрого поиска
    function showrow(txtboxobject, typedata) {
		$(function() {
			$(txtboxobject + '_field').autocomplete({
				delay: 500, // время задержки при поиске
				minLength: 3, // длина текста для активизации поиска
				source:function(request, response) {
					$.getJSON("../../autocomplete",{
						typedata: typedata, // передаем тип справочника
						q: request.term, // передаем текст поиска
					}, function(data) {
						response($.map(data.matching_results, function (item) {
							return {
								label: item[0],
								val: item[1]
							}
						}))
					});
				},
				select: function(event, ui) {
					$(txtboxobject + '_field').val(ui.item.label);
					$(txtboxobject).val(ui.item.val);
				}
			});
		});
	}
	// функция добавляет элемент в список
	function add_select_option(e,value_name,value_guid,element_id) {
		if (e.keyCode == 13) {
			var x = document.getElementById(element_id + '_list');
			var option = document.createElement("option");
			option.text = value_name;
			option.value = value_guid;
			var array = [''];
			for(var i = 0; i < array.length; i++) {
				  if (typeof x[i] == 'undefined'  || x[i] == null){
					break;	
				  }
				  array.push(x[i].value);
			}
			if(array.indexOf(option.value) == -1){
				x.add(option);
				document.getElementById(element_id).value = '';
				document.getElementById(element_id + '_field').value = '';
			}
		}
		
	}
	// функция удалает элемент из списка
	function remove_select_option(element_id){
		var x = document.getElementById(element_id + '_list');
		x.remove(x.selectedIndex);
	}
	// функция отключает ненужные поля перед отправкой и очищает поля после отправки
	function disabled_input_hidden(array){
		for(var i = 0; i < array.length; i++) {
			  document.getElementById(array[i] + '_field').disabled = true
		}
		window.setTimeout(function() {
		for (var i = 0; i < array.length; i++) {
				document.getElementById(array[i]).value = '';
			}
		  }, 0);
	}
	// функция создает список гуидов из селектора и передает в скрытое поле
	function create_list_to_hidden(array){
		for(var i = 0; i < array.length; i++) {
			var x = document.getElementById(array[i] + '_list');
			var x2 = '';
			for(var i1 = 0; i1 < x.length; i1++) {
				  if (typeof x[i1] == 'undefined'){
					break;	
				  }
				  x2 = x2 + '{' + x[i1].value + '}';
				  
				  if( i1 != (x.length - 1)){
					x2 = x2 + ';'
				  }
			}
			if (x2 == ''){
				document.getElementById(array[i]).disabled = true;
			} else {
				document.getElementById(array[i]).value = x2;
			}
			
		}
	}
	
	// функция скрывает форму создания отчёта
	function showModalWin() {

		var darkLayer = document.createElement('div'); // слой затемнения
		darkLayer.id = 'shadow'; // id чтобы подхватить стиль
		document.body.appendChild(darkLayer); // включаем затемнение

		var modalWin = document.getElementById('popupWin'); // находим наше "окно"
		modalWin.style.display = 'block'; // "включаем" его

		darkLayer.onclick = function () {  // при клике на слой затемнения все исчезнет
			darkLayer.parentNode.removeChild(darkLayer); // удаляем затемнение
			modalWin.style.display = 'none'; // делаем окно невидимым
			return false;
		};
	}
	// функция скрывает и раскрывет форму 
	function showDivElement(element_id) {
		if (document.getElementById(element_id).style.display == 'none'){
			document.getElementById(element_id).style.display = 'block';
		}else {
			document.getElementById(element_id).style.display = 'none';
		}
			
	}
	// функция пердупреждения об удалении отчёта
	function warnAboutRemoval(){
		 if(confirm('Удаилть отчёт и все его поля?')) { 
			document.forms['report_remove'].submit();
		 } 
		 else { 
			return false; 					
		 } 
	}
	// функция пердупреждения об удалении поля
	function warnAboutRemovalField(){
		 if(confirm('Удаилть поле?')) { 
			document.forms['field_remove'].submit();
		 } 
		 else { 
			return false; 					
		 } 
	}
	//Динамическая навигация
	$(function () {
          $.each($('.nav').find('li'), function() {
              $(this).toggleClass('active',
                  $(this).find('a').attr('href') == window.location.pathname);
          });
      });
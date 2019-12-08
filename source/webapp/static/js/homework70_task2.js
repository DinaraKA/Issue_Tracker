$.ajax({
    url: 'http://localhost:8000/api/login/',
    method: 'post',
    data: JSON.stringify({username: 'admin', password: 'admin12345'}),
    dataType: 'json',
    contentType: 'application/json',
    success: function(response, status){console.log(response);localStorage.setItem('api_token', response.token)},
    error: function(response, status){console.log(response);}
});

// 1task

$.ajax({
    url: 'http://localhost:8000/api/projects/',
    method: 'get',
	headers: {'Authorization': "Token" + localStorage.getItem('api_token')},
    dataType: 'json',
    success: function(response, status){console.log(response);},
    error: function(response, status){console.log(response);}
});

// 2task

$.ajax({
    url: 'http://localhost:8000/api/tasks/',
    method: 'get',
    dataType: 'json',
    success: function(response, status){console.log(response);},
    error: function(response, status){console.log(response);}
});

// 3task

$.ajax({
    url: 'http://localhost:8000/api/projects/1/',
    method: 'get',
    dataType: 'json',
    success: function(response, status){console.log(response.tasks);},
    error: function(response, status){console.log(response);}
});

// 4task

let newProduct = JSON.stringify({
     'summary': 'Занятие #70. Домашнее задание.',
     'description': 'Задание 1\n' +
         'Настройте аутентификацию по токену для API проекта трекер. Добавьте в API точку входа для входа (выдачи токена). Добавьте проверки:\n' +
         'Просмотр проектов - кто угодно\n' +
         'Просмотр задач - кто угодно\n' +
         'Редактирование проектов (создание, изменение, удаление) - по наличию соответствующих разрешений.\n' +
         'Редактирование задач (создание, изменение, удаление) - по наличию соответствующих разрешений.\n' +
         'Задание 2\n' +
         'Напишите следующие AJAX-запросы с помощью jQuery к вашему API:\n' +
         'Выбор всех проектов;\n' +
         'Выбор всех задач;\n' +
         'Выбор всех задач заданного проекта;\n' +
         'Создание задачи;\n' +
         'Удаление задачи.\n' +
         'Результаты должны выводиться в консоль. Если запрос возвращает вам больше данных, чем нужно, выведите только ту часть, которая нужна.',
     'status': 2,
     'type': 1,
     'project': 2
 });

$.ajax({
    url: 'http://localhost:8000/api/tasks/',
    method: 'post',
    headers: {'Authorization': "Token "  + localStorage.getItem('api_token')},
    data: newProduct,
    dataType: 'json',
    contentType: 'application/json',
    success: function(response, status){console.log(response);},
    error: function(response, status){console.log(response);}
});

// 5task

$.ajax({
    url: 'http://localhost:8000/api/tasks/13/',
    method: 'delete',
    headers: {'Authorization': "Token " + localStorage.getItem('api_token')},
    dataType: 'json',
    contentType: 'application/json',
    success: function(response, status){console.log(response);},
    error: function(response, status){console.log(response);}
});
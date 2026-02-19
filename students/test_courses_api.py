import pytest
from django.urls import reverse
from students.models import Course


@pytest.mark.django_db
class TestCoursesAPI:
    """Тесты для API курсов"""

    def test_retrieve_course(self, api_client, course_factory):
        """Тест получения конкретного курса"""
        # Создаем курс через фабрику
        course = course_factory()
        
        # Строим URL и делаем запрос
        url = reverse('courses-detail', args=[course.id])
        response = api_client.get(url)
        
        # Проверяем код ответа
        assert response.status_code == 200
        
        # Проверяем, что вернулся именно тот курс
        assert response.data['id'] == course.id
        assert response.data['name'] == course.name

    def test_list_courses(self, api_client, course_factory):
        """Тест получения списка курсов"""
        # Создаем несколько курсов через фабрику
        courses = course_factory(_quantity=5)
        
        # Делаем запрос на получение списка
        url = reverse('courses-list')
        response = api_client.get(url)
        
        # Проверяем код ответа
        assert response.status_code == 200
        
        # Проверяем, что получили все курсы
        assert len(response.data) == len(courses)
        
        # Проверяем, что ID курсов соответствуют созданным
        response_ids = [item['id'] for item in response.data]
        expected_ids = [course.id for course in courses]
        assert sorted(response_ids) == sorted(expected_ids)

    def test_filter_courses_by_id(self, api_client, course_factory):
        """Тест фильтрации курсов по ID"""
        # Создаем несколько курсов
        courses = course_factory(_quantity=3)
        target_course = courses[0]
        
        # Фильтруем по ID конкретного курса
        url = reverse('courses-list')
        response = api_client.get(url, data={'id': target_course.id})
        
        # Проверяем код ответа
        assert response.status_code == 200
        
        # Проверяем, что вернулся только один курс с нужным ID
        assert len(response.data) == 1
        assert response.data[0]['id'] == target_course.id
        assert response.data[0]['name'] == target_course.name

    def test_filter_courses_by_name(self, api_client, course_factory):
        """Тест фильтрации курсов по имени"""
        # Создаем курсы с разными именами
        course1 = course_factory(name='Python Development')
        course2 = course_factory(name='Java Programming')
        course3 = course_factory(name='Python Advanced')
        
        # Фильтруем по имени, содержащему 'Python'
        url = reverse('courses-list')
        response = api_client.get(url, data={'name': 'Python'})
        
        # Проверяем код ответа
        assert response.status_code == 200
        
        # Проверяем, что вернулись только курсы с 'Python' в названии
        assert len(response.data) == 2
        for course in response.data:
            assert 'Python' in course['name']

    def test_create_course(self, api_client):
        """Тест успешного создания курса"""
        # Подготавливаем данные для создания
        course_data = {
            'name': 'New Test Course'
        }
        
        # Делаем запрос на создание
        url = reverse('courses-list')
        response = api_client.post(url, data=course_data, format='json')
        
        # Проверяем код ответа
        assert response.status_code == 201
        
        # Проверяем, что курс действительно создался
        assert response.data['name'] == course_data['name']
        assert Course.objects.filter(name=course_data['name']).exists()

    def test_update_course(self, api_client, course_factory):
        """Тест успешного обновления курса"""
        # Создаем курс через фабрику
        course = course_factory(name='Old Name')
        
        # Данные для обновления
        update_data = {
            'name': 'Updated Course Name'
        }
        
        # Делаем запрос на обновление
        url = reverse('courses-detail', args=[course.id])
        response = api_client.put(url, data=update_data, format='json')
        
        # Проверяем код ответа
        assert response.status_code == 200
        
        # Проверяем, что данные обновились
        course.refresh_from_db()
        assert course.name == update_data['name']
        assert response.data['name'] == update_data['name']

    def test_delete_course(self, api_client, course_factory):
        """Тест успешного удаления курса"""
        # Создаем курс через фабрику
        course = course_factory()
        course_id = course.id
        
        # Делаем запрос на удаление
        url = reverse('courses-detail', args=[course.id])
        response = api_client.delete(url)
        
        # Проверяем код ответа
        assert response.status_code == 204
        
        # Проверяем, что курс действительно удален
        assert not Course.objects.filter(id=course_id).exists()

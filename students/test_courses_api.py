import pytest
from django.urls import reverse
from students.models import Course

@pytest.mark.django_db
class TestCoursesAPI:
    """Тесты для API курсов"""

    def test_retrieve_course(self, api_client, course_factory):
        course = course_factory()
        url = reverse('courses-detail', args=[course.id])
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert response.data['id'] == course.id
        assert response.data['name'] == course.name

    def test_list_courses(self, api_client, course_factory):
        courses = course_factory(_quantity=5)
        url = reverse('courses-list')
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert len(response.data) == len(courses)

    def test_filter_courses_by_id(self, api_client, course_factory):
        courses = course_factory(_quantity=3)
        target_course = courses[0]
        url = reverse('courses-list')
        response = api_client.get(url, data={'id': target_course.id})
        
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['id'] == target_course.id

    def test_filter_courses_by_name(self, api_client, course_factory):
        course_factory(name='Python Development')
        course_factory(name='Java Programming')
        course_factory(name='Python Advanced')
        
        url = reverse('courses-list')
        response = api_client.get(url, data={'name': 'Python'})
        
        assert response.status_code == 200
        assert len(response.data) == 2
        for course in response.data:
            assert 'Python' in course['name']

    def test_create_course(self, api_client):
        course_data = {'name': 'New Test Course'}
        url = reverse('courses-list')
        response = api_client.post(url, data=course_data, format='json')
        
        assert response.status_code == 201
        assert response.data['name'] == course_data['name']
        assert Course.objects.filter(name=course_data['name']).exists()

    def test_update_course(self, api_client, course_factory):
        course = course_factory(name='Old Name')
        update_data = {'name': 'Updated Course Name'}
        url = reverse('courses-detail', args=[course.id])
        response = api_client.put(url, data=update_data, format='json')
        
        assert response.status_code == 200
        course.refresh_from_db()
        assert course.name == update_data['name']

    def test_delete_course(self, api_client, course_factory):
        course = course_factory()
        course_id = course.id
        url = reverse('courses-detail', args=[course.id])
        response = api_client.delete(url)
        
        assert response.status_code == 204
        assert not Course.objects.filter(id=course_id).exists()

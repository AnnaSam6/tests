import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from students.models import Course, Student

@pytest.fixture
def api_client():
    """Фикстура для API клиента"""
    return APIClient()

@pytest.fixture
def course_factory():
    """Фабрика для создания курсов"""
    def factory(**kwargs):
        return baker.make(Course, **kwargs)
    return factory

@pytest.fixture
def student_factory():
    """Фабрика для создания студентов"""
    def factory(**kwargs):
        return baker.make(Student, **kwargs)
    return factory

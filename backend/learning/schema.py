import graphene
from graphene_django import DjangoObjectType

from learning.models import Course, Lesson, Author


class CourseType(DjangoObjectType):
    class Meta:
        model = Course


class LessonType(DjangoObjectType):
    class Meta:
        model = Lesson 


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author


class Query(graphene.ObjectType):
    courses = graphene.List(CourseType)
    lessons = graphene.List(LessonType)

    def resolve_courses(self, info, **kwargs):
        return Course.objects.all()

    def resolve_lessons(self, info, **kwargs):
        return Lesson.objects.all()
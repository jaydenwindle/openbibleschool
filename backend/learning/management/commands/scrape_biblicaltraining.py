from django.core.management.base import BaseCommand
from datetime import datetime
from selenium import webdriver

from learning.models import Author, Course, Lesson, Video, Audio


class Command(BaseCommand):
    help = 'Scrape course information from biblicaltraining.org'

    def handle(self, *args, **kwargs):
        course_list_url = 'https://www.biblicaltraining.org/classes/all'

        driver = webdriver.Chrome()
        driver.get(course_list_url)

        course_rows = driver.find_elements_by_xpath("//table/tbody/tr")
        courses = []

        for course in course_rows:
            columns = course.find_elements_by_tag_name('td')

            course_link_element = columns[0].find_element_by_tag_name('a')
            course_author_link_element = columns[1].find_element_by_tag_name('a')

            course_url = course_link_element.get_attribute('href')
            course_name = course_link_element.text
            course_author_link = course_author_link_element.get_attribute('href')
            course_author_name = course_author_link_element.text
            course_category = columns[-1].text


            if course_category != 'Non-English':
                author_instance, created = Author.objects.get_or_create(name=course_author_name)
                if created:
                    print(f'New author found: {course_author_name}')

                course_instance, created = Course.objects.get_or_create(
                    name=course_name,
                    original_url=course_url,
                    original_host="http://biblicaltraining.org",
                )
                course_instance.authors.set([author_instance])
                course_instance.save()
                if created:
                    print(f'New Course Found: {course_name}')
                    print(f'\tAuthor: {course_author_name}')
                    print(f'\tURL: {course_url}')
        
                courses.append({
                    "instance": course_instance,
                    "url": course_url
                })
        
        lessons = []

        for course in courses:
            instance = course['instance']
            url = course['url']

            driver.get(url)

            description = driver.find_element_by_css_selector('.course-body .pane-content').text
            instance.description = description
            instance.save()

            metadata_elements = driver.find_elements_by_css_selector('.courses-sidebar > ul > li')
            metadata = {}

            for element in metadata_elements:
                key = element.find_element_by_class_name('pane-title').text
                value = element.find_element_by_class_name('pane-content').text
                print(key, value)
                metadata[key] = value
            
            instance.data = metadata
            instance.save()

            lessons = driver.find_elements_by_class_name('lecture-item')

            for lesson in lessons:
                lesson_link_element = lesson.find_element_by_css_selector('.views-field-title a')
                lesson_description = lesson.find_element_by_css_selector('.views-field-body').text
                lesson_number = lesson.find_element_by_css_selector('.views-field-counter').text
                lesson_url = lesson_link_element.get_attribute('href')
                lesson_name = lesson_link_element.text

                lesson_instance, created = Lesson.objects.get_or_create(
                    course=instance,
                    name=lesson_name,
                    index=lesson_number,
                    description=lesson_description,
                    original_url=lesson_url
                )
                if created:
                    print(f'New Lesson Found: {lesson_name}')
                    print(f'\tLesson #{lesson_number}')
                    print(f'\tURL: {lesson_url}')

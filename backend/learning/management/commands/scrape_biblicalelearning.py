from django.core.management.base import BaseCommand
from datetime import datetime
from selenium import webdriver

from learning.models import Author, Course, Lesson, Video, Audio


class Command(BaseCommand):
    help = 'Scrape course information from biblicalelearning.org'

    def handle(self, *args, **kwargs):
        author_list_url = 'http://biblicalelearning.org/authors/'

        driver = webdriver.Chrome()
        driver.implicitly_wait(30)
        driver.get(author_list_url)

        authors = driver.find_elements_by_class_name('page-list-ext-title')

        author_urls = []
        for author in authors:
            url = str(author.find_element_by_tag_name('a').get_attribute('href')) 
            author_urls.append(url)

        for author_url in author_urls:
            driver.get(author_url)

            author_name = driver.find_element_by_class_name('entry-title').text

            driver.implicitly_wait(0)
            pages = driver.find_elements_by_xpath("//div[@class='se-pagination']/a")
            page_urls = [None]
            for page in pages:
                page_urls.append(str(page.get_attribute('href')))
            visited = {}
            driver.implicitly_wait(30)

            for page_url in page_urls:
                if page_url and not visited.get(page_url, False):
                    driver.get(page_url)
                    visited[page_url] = True

                lessons = driver.find_elements_by_xpath("//table[@class='enmse-more-messages']/tbody/tr")

                for lesson in lessons:
                    name = lesson.find_element_by_class_name('enmse-title-cell').text
                    urls = lesson.find_elements_by_tag_name('a')
                    recorded_at = lesson.find_element_by_css_selector('.enmse-date-cell:not(.enmse-speaker-cell)').text
                    if recorded_at:
                        recorded_at = datetime.strptime(recorded_at, '%B %d, %Y')
                
                    if str.find(name, author_name) == 0 and name.count(',') >= 2:
                        author, course, lecture = name.split(', ', 2)
                    else:
                        author = course = lecture = False

                        # Manual overrides
                        # ---------------

                        # Incorrect names
                        incorrect_names = [
                            'Dr. Herb Batemen',
                            'Dr. Dan Darko',
                            'Dr. Dan Darco',
                            'Don Fowler',
                            'Dr. David Howard',
                            'Dr. Jennings Mark',
                            'Dr. Mar Wilson',
                            'Dr. Gay Yates',
                            'Dr Gary Yates',
                            'Cynthia Parker',
                            'David Turner',
                        ]

                        for incorrect_name in incorrect_names:
                            if str.find(name, incorrect_name) == 0:
                                author, course, lecture = name.split(', ', 2)
                                author = author_name 

                        # Alternative naming schemes
                        if str.find(name, 'Psalms of the Exodus') == 0:
                            author = author_name 
                            course, lecture = name.split(' -- ')
                        if author_name == 'Dr. Craig Keener' and str.find(name, 'Acts') == 0:
                            author = author_name 
                            course, lecture = name.split(', ', 1)
                        if author_name == 'Dr. Dave Mathewson' and str.find(name, 'Revelation') == 0:
                            author = author_name 
                            course, lecture = name.split(', ', 1)
                        
                        # Author Single Course
                        if author_name == 'Dr. Kevin E. Frederick':
                            author = author_name
                            course = 'Waldensians'
                            lecture = name
                        if author_name == 'Dr. Kevin E. Frederick':
                            author = author_name
                            course = 'Waldensians'
                            lecture = name

                        # One off errors
                        if name == 'Dr. John Oswalt, Isaiah Session 12 -- Isaiah 24-25':
                            author = author_name
                            course = 'Isaiah'
                            lecture = 'Session 12 -- Isaiah 24-25'
                        
                        if not (author and course and lecture):
                            print('unparseable', author_name, name)
                    
                    if author and course and lecture:
                        author_instance, created = Author.objects.get_or_create(name=author_name)
                        if created:
                            print(f'New author found: {author_name}')

                        course_instance, created = Course.objects.get_or_create(
                            name=course,
                            original_host="http://biblicalelearning.org",
                        )
                        course_instance.authors.set([author_instance])
                        course_instance.save()
                        if created:
                            print(f'New course found: {course}')

                        lesson_instance, created = Lesson.objects.get_or_create(
                            name=lecture,
                            course=course_instance,
                            recording_date=recorded_at,
                        )
                        if created:
                            print(f'New lecture found: {lecture}')

                        for url in urls:
                            lesson_type = url.text
                            url_path = url.get_attribute('href')

                            if lesson_type == 'Watch':
                                lesson_video, created = Video.objects.get_or_create(
                                    original_url=url_path,
                                    lesson=lesson_instance
                                )
                                if created:
                                    print(f'New video found: {url_path}')

                            if lesson_type == 'Listen':
                                lesson_audio = Audio.objects.get_or_create(
                                    original_url=url_path,
                                    lesson=lesson_instance
                                )
                                if created:
                                    print(f'New audio found: {url_path}')


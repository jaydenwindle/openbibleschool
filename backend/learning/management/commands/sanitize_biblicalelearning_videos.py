from django.core.management.base import BaseCommand
from selenium import webdriver

from learning.models import Author, Course, Lesson, Video, Audio


class Command(BaseCommand):
    help = 'Scrape course information from biblicalelearning.org'

    def handle(self, *args, **kwargs):
        biblical_elearning_videos = Video.objects.filter(
            lesson__original_host='http://biblicalelearning.org',
            video_id__isnull=True
        )
        num_videos = len(biblical_elearning_videos)
        print(num_videos)

        driver = webdriver.Chrome()
        driver.implicitly_wait(30)

        for index, video in enumerate(biblical_elearning_videos):
            driver.get(video.original_url)
            try:
                driver.implicitly_wait(0)
                youtube_url = driver.find_element_by_tag_name('iframe').get_attribute('src')
                driver.implicitly_wait(30)
            except Exception as e:
                print(e)
                continue

            youtube_id = youtube_url.split('/')[-1].split('?')[0]

            video.video_id = youtube_id
            video.save()

            print("{0:.0%}".format(index/num_videos), youtube_url)


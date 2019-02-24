import requests
from django.utils.dateparse import parse_duration
from django.core.management.base import BaseCommand
from selenium import webdriver

from learning.models import Author, Course, Lesson, Video, Audio


class Command(BaseCommand):
    help = 'Scrape course information from biblicalelearning.org'

    def handle(self, *args, **kwargs):
        youtube_videos = Video.objects.filter(video_id__isnull=False)
        total_duration = None

        for video in youtube_videos:
            api_key="AIzaSyBBUXxtAlXI4mul2uevdqa6aNcfkmVPyII"
            searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+video.video_id+"&key="+api_key+"&part=contentDetails"
            
            response = requests.get(searchUrl).json()

            try:
                duration = parse_duration(response['items'][0]['contentDetails']['duration'])
            except Exception:
                print(response)

            video.duration = duration
            video.save()

            if not total_duration:
                total_duration = duration
            else:
                total_duration += duration

            print(duration, total_duration)
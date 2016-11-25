#!/usr/bin/env python


import youtube_dl
import re

#Compile regex for youtube check
reg = re.compile("^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$")


def urlcheck(url):
    if reg.match(url) is not None: 
        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
        with ydl:
            try:
                result = ydl.extract_info(url, download=False) 
            except youtube_dl.utils.DownloadError:
                return False

        if 'entries' in result:
            return False
        else:
            return True
    else:
        return False
           

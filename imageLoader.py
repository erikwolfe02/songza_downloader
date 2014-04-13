import os
import shutil
import threading
import urllib2


class ImageLoader(threading.Thread):
    def __init__(self, image_url, image_name, callback, threadId="imageLoaderThread"):
        threading.Thread.__init__(self)
        self.thread_id = threadId
        self.image_url = image_url
        self.image_name = image_name
        self.callback = callback

    def run(self):
        self.callback(self.download_image())

    def download_image(self):
        image_path = "temp/" + self.image_name + ".jpg"
        if not os.path.exists(image_path):
            response = urllib2.urlopen(self.image_url)
            with open(image_path, 'wb') as dest:
                shutil.copyfileobj(response, dest)
        return image_path





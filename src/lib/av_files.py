import os
import time

import lib.constants as c



class AvFile(object):

    def __init__(self,
                 name,
                 vid_file = None,
                 aud_file = None,
                 preview_file = None,
                 log_file = None,
    ):
        self.name = name
        self.vid_file = vid_file
        self.aud_file = aud_file
        self.preview_file = preview_file
        self.log_file = log_file

        self.has_been_viewed = False



    def mark_as_viewed(self):
        self.log_file = f"{c.SAVED_VIDEOS_DIR}/{self.name}.log"
        fp = open(self.log_file, 'a')
        fp.write(f"{int(time.time() * 1000)}\n")
        fp.close()



class AvFiles(object):

    def __init__(self):
        # a dictionary of namekey => AvFile
        self.av_files = []
        self.name_index = {}
        self.pointer_index = 0
        self.unviewed_count = 0

        self.load_data()


    def load_data(self):
        self.load_file_data()
        self.point_to_first_unread()


    def load_file_data(self):
        av_files = {}
        for filename in os.listdir(c.SAVED_VIDEOS_DIR):
            i_dot = filename.rfind(".")
            name_key = filename[0:i_dot]
            ext = filename[i_dot:]
            full_path = f"{c.SAVED_VIDEOS_DIR}/{filename}"

            av_file = None
            if name_key in av_files:
                av_file = av_files[name_key]
            else:
                av_file = AvFile(name_key)
                av_files[name_key] = av_file

            # print(f"full_path = {full_path}")

            if ext == '.mp4':
                av_file.vid_file = full_path
            elif ext == '.wav':
                av_file.aud_file = full_path
            elif ext == '.jpg':
                av_file.preview_file = full_path
            elif ext == '.log':
                av_file.log_file = full_path
                av_file.has_been_viewed = True

        self.av_files = list(av_files.values())

        # sorted by unviewed, then viewed and by date descending within
        self.av_files.sort(key=lambda x: (x.has_been_viewed, int(x.name) * -1))
        print(f"av_files: got av_files")

        self.name_index = {}
        for i in range(len(self.av_files)):
            f = self.av_files[i]
            self.name_index[f.name] = i
            print(f"av_files: [{i}] = {(f.name, f.has_been_viewed)}")


    def get_by_name(self, name_key):
        return self.av_files[self.name_index[name_key]]


    def point_to_name(self, name_key):
        self.pointer_index = self.name_index[name_key]


    def point_to_first_unread(self):
        num_av_files = len(self.av_files)

        i = 0
        while i < num_av_files:
            if self.av_files[i].has_been_viewed:
                i -= 1
                break
            i += 1

        self.unviewed_count = min(max(i + 1, 0), num_av_files)
        self.pointer_index = min(max(i, 0), max(num_av_files - 1, 0))

        print(f"av_files: {self.unviewed_count} / {num_av_files} unviewed. pointer_index={self.pointer_index}")

        return self.pointer_index

    def increment_pointer(self):
        if self.is_next_file():
            self.pointer_index += 1
            return True
        return False


    def decrement_pointer(self):
        if self.is_previous_file():
            self.pointer_index -= 1
            return True
        return False


    def current_av_file(self):
        num_av_files = len(self.av_files)
        if num_av_files <= 0:
            return None

        return self.av_files[self.pointer_index]


    def is_previous_file(self):
        num_av_files = len(self.av_files)
        return num_av_files > 0 and self.pointer_index + 1 < num_av_files


    def previous_av_file(self):
        if not self.is_previous_file():
            return None

        return self.av_files[self.pointer_index + 1]


    def is_next_file(self):
        num_av_files = len(self.av_files)
        return num_av_files > 1 and self.pointer_index > 0


    def next_av_file(self):
        if not self.is_next_file():
            return None

        return self.av_files[self.pointer_index - 1]


    def mark_as_viewed(self, name_key):
        self.av_files[name_key].mark_as_viewed()




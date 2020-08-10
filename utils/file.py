import os


# /home/vaad/xxx/videos/black_mirror.mp4 -> 600342
def get_file_size(file):
    file_bytes = os.path.getsize(file)
    return file_bytes


# black_mirror.mp4 -> black_mirror
def get_file_name(file_name):
    return file_name.split('.')[0]


# black_mirror.mp4 -> mp4
def get_file_type(file_name):
    return file_name.split('.')[1]

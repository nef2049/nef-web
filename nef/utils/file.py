import os


# /home/vaad/xxx/videos/black_mirror.mp4 -> 600342
def get_file_size(file):
    file_bytes = os.path.getsize(file)
    return file_bytes


# black_mirror.mp4 -> black_mirror
def get_file_name(file_name):
    file_type = get_file_type(file_name)
    return file_name[:-len(file_type) - 1]


# black_mirror.mp4 -> mp4
def get_file_type(file_name):
    return file_name.split('.')[-1]


# xxx.zip in {"zip","7z", ...}?
def file_allowed(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_extensions

from nef.bp import bp_file_system
import config
import os
import flask
import time


@bp_file_system.route('/')
@bp_file_system.route('/<path:subdir>')
def document(subdir=''):
    if subdir == '':
        os.chdir(config.UPLOAD_PATH)
    else:
        fullname = config.UPLOAD_PATH + os.sep + subdir
        if os.path.isfile(fullname):
            filename = fullname.split(os.sep)[-1]
            dir_path = fullname[:-len(filename)]
            return flask.send_from_directory(dir_path, filename, as_attachment=True)
        else:
            os.chdir(fullname)

    current_dir = os.getcwd()
    current_list = os.listdir(current_dir)
    contents = []
    for i in sorted(current_list):
        full_path = current_dir + os.sep + i
        if os.path.isdir(full_path):
            extra = os.sep
        else:
            extra = ''

        content = dict()
        content['filename'] = i + extra
        content['mtime'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                         time.localtime(os.stat(full_path).st_mtime))
        content['size'] = str(round(os.path.getsize(full_path) / 1024)) + 'k'
        contents.append(content)

    return flask.render_template('file_system.html', contents=contents, subdir=subdir, ossep=os.sep)

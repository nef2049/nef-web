from nef.bp import bp_audios


@bp_audios.route('/')
def hello_world():
    return 'Hello Audios'

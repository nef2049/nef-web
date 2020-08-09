import bp

@bp.bp_audios.route('/')
def hello_world():
    return 'Hello Audios'

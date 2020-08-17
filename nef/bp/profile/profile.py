from nef.bp import bp_profile


@bp_profile.route("/")
def index():
    return "success"

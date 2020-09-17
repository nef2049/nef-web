from nef.bp import bp_fund
import requests
import json
import threading


requests_prefix = "jsonpgz("
requests_suffix = ");"

# TODO: save it to db...
fund_code_list = {
    "003096",
    "161725",
    "005693",
    "160222",
    "160221",
    "519674",
    "001156",
    "002079",
    "004966",
}


@bp_fund.route("")
@bp_fund.route("/")
def list_funds():
    data = dict()
    threads = []

    for code in fund_code_list:
        t = threading.Thread(target=fund, args=(code, data))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    return data


@bp_fund.route("/specific/<fund_code>")
def spec_fund(fund_code):
    return fund(fund_code)


@bp_fund.route("/add/<fund_code>")
def add_fund_code(fund_code):
    fund_code_list.add(str(fund_code))
    return str(fund_code_list)


@bp_fund.route("/delete/<fund_code>")
def delete_fund_code(fund_code):
    fund_code_list.remove(str(fund_code))
    return str(fund_code_list)


@bp_fund.route("/list")
def list():
    return str(fund_code_list)


def fund(fund_code, data_dict=None):
    url = 'http://fundgz.1234567.com.cn/js/{}.js?rt=1589463125600'.format(fund_code)
    result = requests.get(url)
    content = result.content.decode("utf-8")
    content = content[len(requests_prefix):-len(requests_suffix)]
    try:
        j_data = json.loads(content)
        j_data_convert = dict()
        j_data_convert["code"] = j_data["fundcode"]
        # j_data_convert["name"] = j_data["name"]
        j_data_convert["unit_worth"] = j_data["dwjz"]
        j_data_convert["unit_worth_time"] = j_data["jzrq"]
        j_data_convert["estimate_worth"] = j_data["gsz"]
        j_data_convert["estimate_rate"] = float(j_data["gszzl"])
        j_data_convert["update_time"] = j_data["gztime"]

        if data_dict is not None:
            data_dict[j_data["name"]] = j_data_convert

        return j_data_convert
    except:
        return dict()

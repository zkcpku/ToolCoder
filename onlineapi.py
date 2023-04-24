import re
from duckduckgo_search import ddg

def extract_function_signatures(text):
    text = text.replace("("," ( ")
    text = text.split()
    left_p_idx = []
    for i,e in enumerate(text):
        if e == "(" or e == "()":
            left_p_idx.append(i)
    def extract_api_name(token_list, i):
        this_token_list = token_list[:i]
        could_dot = False
        rtn_api = ""
        for each_token in this_token_list[::-1]:
            if could_dot and each_token == ".":
                rtn_api = each_token+rtn_api
                could_dot = False
            elif could_dot:
                return rtn_api
            elif not could_dot and each_token != ".":
                rtn_api = each_token+rtn_api
                could_dot = True
            else:
                assert False
                return rtn_api
    def remove_prefix_dot(api_name):
        while api_name.startswith("."):
            api_name = api_name[1:]
        while api_name.endswith("."):
            api_name = api_name[:-1]
        return api_name
    all_apis = [remove_prefix_dot(extract_api_name(text, e)) for e in left_p_idx]
    return all_apis
def extract_torchdata_api(page):
    href = page['href']
    body = page['body']
    href_api = None
    body_api = None
    special_func_name = None
    try:
        href_api = href.split("/")[-1].replace(".html","")
        body_api = extract_function_signatures(body)
        special_func_name = body.split("functional name:")[-1].split(")")[0].strip()
    except Exception as e:
        print(e)
        # {'most_common_apis': [],'search_page': None,'apis_count': None}
    most_common_apis = []
    if href_api is not None:
        most_common_apis.append([href_api, 10])
    if body_api is not None:
        for each in body_api:
            most_common_apis.append([each, 1])
    if special_func_name is not None:
        most_common_apis.append([special_func_name, 100])
    most_common_apis = sorted(most_common_apis, key=lambda x: x[1], reverse=True)
    return {'most_common_apis': most_common_apis, "search_page": page}
                
# extract_function_signatures(r[0]['title'] + " " + r[0]['body'] + " lower ( )")

def search_in_datagy(search_inp):
    try:
        site_template = search_inp + " site:https://datagy.io/"
        r = ddg(site_template, max_results=1)

        search_page = r[0]
        apis = extract_function_signatures(r[0]['title'] + " " + r[0]['body'])
        apis_count = {}
        for e in apis:
            if e in apis_count:
                apis_count[e] += 1
            else:
                apis_count[e] = 1
        most_common_apis = sorted(apis_count.items(), key=lambda x: x[1], reverse=True)
        # most_common_apis = most_common_apis[0]
        return {"most_common_apis": most_common_apis, "search_page": search_page, "apis_count": apis_count}
    except Exception as e:
        return {"error": str(e), "r": r}


def search_in_torchdata(search_inp):
    try:
        site_template = search_inp + " site:https://pytorch.org/data/beta"
        r = ddg(site_template, max_results=1)

        search_page = r[0]
        rtn = extract_torchdata_api(search_page)
        # most_common_apis = most_common_apis[0]
        return rtn
    except Exception as e:
        return {"error": str(e), "r": r}


def search_in_ddg(search_inp):
    site_template = search_inp
    r = ddg(site_template, max_results=5)
    search_pages = list(r)
    return {"search_pages": search_pages}


        
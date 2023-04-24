import re
from duckduckgo_search import ddg

def extract_function_signatures(text):
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
                return rtn_api
    def remove_prefix_dot(api_name):
        while api_name.startswith("."):
            api_name = api_name[1:]
        while api_name.endswith("."):
            api_name = api_name[:-1]
        return api_name
    all_apis = [remove_prefix_dot(extract_api_name(text, e)) for e in left_p_idx]
    return all_apis
                
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

def search_in_ddg(search_inp):
    site_template = search_inp
    r = ddg(site_template, max_results=5)
    search_pages = list(r)
    return {"search_pages": search_pages}


        
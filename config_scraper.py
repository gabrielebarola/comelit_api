import os, json, sys
import requests
from bs4 import BeautifulSoup

def scrape_category(cat, endpoint_name, c_map, url, s):
    c_map[cat] = {}
    resp = s.get(url+INFO_ENDPOINT.format(endpoint_name))
    data = resp.json()

    #creating an object for each env
    for i in data["env_desc"]:
        c_map[cat][i] = []

    for i in range(data["num"]):
        env_index = data["env"][i]
        env_name = data["env_desc"][env_index]
        
        c_map[cat][env_name].append(
            {
                "ref": data["desc"][i],
                "type": data["type"][i]
            }
        )

    #clean up empty envs
    for i in c_map[cat].copy():
        if len(c_map[cat][i])==0:
            del c_map[cat][i]

    return c_map

PATH = os.path.join("conf", "conf.json")
LOGIN_ENDPOINT = "/login.cgi"
INFO_ENDPOINT = "/user/icon_desc.json?type={}"

def main():
    if len(sys.argv)!=3:
        print("Wrong number of arguments")
        sys.exit()

    form_data = {
        "dom": sys.argv[2]
    } 

    url = "http://" + sys.argv[1]

    comelit_map = {}

    with requests.session() as s:

        r = s.post(url+LOGIN_ENDPOINT, data=form_data)

        if r.status_code==200:
            if input("would you like to scrape lights? (Y/n): ") != "n":
                comelit_map = scrape_category("lights", "light", comelit_map, url, s)

            if input("would you like to scrape shutters? (Y/n): ") != "n":
                comelit_map = scrape_category("shutters", "shutter", comelit_map, url, s)

            if input("would you like to scrape others? (Y/n): ") != "n":
                comelit_map = scrape_category("others", "other", comelit_map, url, s)

            os.makedirs(os.path.dirname(PATH), exist_ok=True)
            with open(PATH, "w") as map_file:
                json.dump(comelit_map, map_file, indent=4)

if __name__ == "__main__":
    main()

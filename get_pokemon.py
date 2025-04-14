from urllib import request, error
import json, os, glob, csv

# url = "https://pokeapi.co/api/v2/pokedex/1/"

def generationi_csv():
    dirname = "pokemon_varieties_info"
    notallow_species = {"gmax", "mega", "x", "y", "build", "mode", "totem", "alola", "galar", "hisui", "breed", "starter", "cap", "star", "belle", "phd", "libre", "cosplay"}
    os.chdir(dirname)
    pfiles = sorted(os.listdir(), key=lambda x: int(x.split("_")[0]))
    for pfile in pfiles: 
        with open(pfile, "r") as f:
            pdata= json.load(f)
            pid = pdata["id"]
            pname = pdata["name"]
            ptype1 = pdata['types'][0]["type"].get("name")
            try:
                ptype2 = pdata['types'][1]["type"].get("name")
            except IndexError as e:
                ptype2 = pdata['types'][0]["type"].get("name")
            pstat_hp = pdata['stats'][0]["base_stat"]
            pstat_atta = pdata['stats'][1]["base_stat"]
            pstat_defe = pdata['stats'][2]["base_stat"]
            pstat_spat = pdata['stats'][3]["base_stat"]
            pstat_spde = pdata['stats'][4]["base_stat"]
            pstat_spee = pdata['stats'][5]["base_stat"]
            
            if not pname.split("-")[-1] in notallow_species:                    
                # print(f"{pid}, {pname}, {ptype1}, {ptype2}, {pstat_hp}, {pstat_atta}, {pstat_defe}, {pstat_spat}, {pstat_spde}, {pstat_spee}") 
                pinfo = (pid,pname,ptype1,ptype2,pstat_hp,pstat_atta,pstat_defe,pstat_spat,pstat_spde,pstat_spee)
                with open("pokedex_generationi.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(pinfo)
            if pid == 151:
                break


def get_info(url, filename, directory_name):    
    headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36" }
    # directory_name = "pokemon_species_info"
    if not os.path.exists(f"../{directory_name}"):
        os.makedirs(f"../{directory_name}")
                    
    try:
        request_details = request.Request(url, headers=headers)
        response = request.urlopen(request_details).read()
        data = json.loads(response.decode("utf-8"))
        with open(f"../{directory_name}/{filename}", "w", encoding="utf-8") as file:
            print(f"Creating file for {filename}")
            json.dump(data, file, ensure_ascii=True, indent=4)
        # print(response.decode("utf-8"))
    except error.HTTPError as error:
        print(error)

def change_filenames():
    os.chdir('pokemon_varieties_info')
    pokemon_files = sorted(os.listdir(), key=lambda x: int(x.split("_")[0]))
    for pokemon_file in pokemon_files:
        os.rename(pokemon_file, pokemon_file.upper())

# with open("nationaldex.json", "r") as file:
#     data = json.load(file)
#     for item in data["pokemon_entries"]:
#         entry_number = item["entry_number"]
#         pokemon_name = item["pokemon_species"]["name"]
#         pokemon_url =item["pokemon_species"]["url"]
#         filename = f"{entry_number}_{pokemon_name}.json"
#         get_info(pokemon_url, filename)

# os.chdir('pokemon_species_info')
# files: coming from os.listdir() sorted alphabetically, thus not numerically
# pokemon_files = sorted(os.listdir(), key=lambda x: int(x.split("_")[0]))
# noallow_species = ("mega", "gmax")
# pokemon_cnt = 0
# for pokemon_file in pokemon_files:
#     with open(pokemon_file, "r") as f:
#         pokemon_data = json.load(f)
#         pokemon_id = pokemon_data["id"]
#         for item in pokemon_data["varieties"]["pokemon"]:
#             print(item)
            # pokemon_name = item["pokemon"]["name"]
            # pokemon_url = item["pokemon"]["url"]
            # pokemon_cnt += 1
            # pokemon_fname = f"{pokemon_cnt}_{pokemon_id}_{pokemon_name}.json"
            # get_info(pokemon_url, pokemon_fname, "pokemon_varieties_info")

def show_evolutions():
    os.chdir('pokemon_varieties_info')
    pokemon_files = glob.glob('*-y.json')
    for pokemon_file in pokemon_files:
        print(pokemon_file)


remove_evolutions()
# show_evolutions()
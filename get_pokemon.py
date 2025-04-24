from urllib import request, error
import json, os, glob, csv
import requests


# url = "https://pokeapi.co/api/v2/pokemon/1/"

def request_data(url):

    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    else:
        print("Request successful.")
        data = r.json()
        return data
    finally:
        print("Request finished.")

def add_nrows(row, filename):

    with open(filename, "r", newline="") as f:
        reader = csv.reader(f)
        cnt = sum(1 for row in reader)
        if(cnt != 0):
            tmp = list(row)
            tmp.insert(0, cnt)
            row = tuple(tmp)
            return row
        else:
            return row

def record_data(row, filename):

    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        row = add_nrows(row, filename)
        writer.writerow(row)

def retrieve_data(url):

    data = request_data(url)
    try:
        for item in data["pokemon_entries"]:
            id = item["entry_number"]
            name  = item["pokemon_species"]["name"]
            pokemon = (id, name)
            record_data(pokemon, "pokedex.csv")
    except Exception as e:
        print(f"Error is {e}")

def pokemon_type(type):

    match type:
        case "normal":
            type = 1
        case "grass":
            type = 2
        case "fire":
            type = 3
        case "water":
            type = 4
        case "electric":
            type = 5
        case "fighting":
            type = 6
        case "flying":
            type = 7
        case "poison":
            type = 8
        case "ground":
            type = 9
        case "psychic":
            type = 10
        case "rock":
            type = 11
        case "ice":
            type = 12
        case "bug":
            type = 13
        case "dragon":
            type = 14
        case "ghost":
            type = 15
        case "dark":
            type = 16
        case "steel":
            type = 17
        case "fairy":
            type = 18
        case "stellar":
            type = 19
        case _:
            type = 0
    return type
# This function can retrieve this following data:
# "is_baby"
# "is_legendary"
# "is_mythical"
# "generation" "name"
# "varieties"

def retrieve_species_data(url):

    data = request_data(url)
    try:
        s_generation = data["generation"]["name"]
        id = data["id"]
        match s_generation:
            case "generation-i":
                i_gen = 1
            case "generation-ii":
                i_gen = 2
            case "generation-iii":
                i_gen = 3
            case "generation-iv":
                i_gen = 4
            case "generation-v":
                i_gen = 5
            case "generation-vi":
                i_gen = 6
            case "generation-vii":
                i_gen = 7
            case "generation-viii":
                i_gen = 8
            case "generation-ix":
                i_gen = 9

        for item in data["varieties"]:
            info = list([])
            specie = item["pokemon"]["name"]
            url = item["pokemon"]["url"]
            specie_id = url.split("/")[-2]
            info.append(id)
            info.append(specie)
            pokemon = request_data(url)
            type1 = pokemon_type(pokemon["types"][0]["type"].get("name"))
            info.append(type1)
            try:
                type2 = pokemon_type(pokemon["types"][1]["type"].get("name"))
                info.append(type2)
            except IndexError as e:
                type2 = pokemon_type("")
                info.append(type2)
            info.append(i_gen)
            info.append(specie_id)
            info = tuple(info)
            record_data(info, "pokedex_species.csv")
    except Exception as e:
        print(f"Error is {e}")



# def generationi_csv():
#     dirname = "pokemon_varieties_info"
#     notallow_species = {"gmax", "mega", "x", "y", "build", "mode", "totem", "alola", "galar", "hisui", "breed", "starter", "cap", "star", "belle", "phd", "libre", "cosplay"}
#     os.chdir(dirname)
#     pfiles = sorted(os.listdir(), key=lambda x: int(x.split("_")[0]))
#     for pfile in pfiles: 
#         with open(pfile, "r") as f:
#             pdata= json.load(f)
#             pid = pdata["id"]
#             pname = pdata["name"]
#             ptype1 = pdata['types'][0]["type"].get("name")
#             try:
#                 ptype2 = pdata['types'][1]["type"].get("name")
#             except IndexError as e:
#                 ptype2 = ""
#             pstat_hp = pdata['stats'][0]["base_stat"]
#             pstat_atta = pdata['stats'][1]["base_stat"]
#             pstat_defe = pdata['stats'][2]["base_stat"]
#             pstat_spat = pdata['stats'][3]["base_stat"]
#             pstat_spde = pdata['stats'][4]["base_stat"]
#             pstat_spee = pdata['stats'][5]["base_stat"]
            
#             if not pname.split("-")[-1] in notallow_species:                    
#                 # print(f"{pid}, {pname}, {ptype1}, {ptype2}, {pstat_hp}, {pstat_atta}, {pstat_defe}, {pstat_spat}, {pstat_spde}, {pstat_spee}") 
#                 pinfo = (pid,pname,ptype1,ptype2,pstat_hp,pstat_atta,pstat_defe,pstat_spat,pstat_spde,pstat_spee)
#                 with open("pokedex_generationi.csv", "a", newline="") as f:
#                     writer = csv.writer(f)
#                     writer.writerow(pinfo)
#             if pid == 151:
#                 break


# def get_info(url, filename, directory_name):    
#     headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36" }
#     # directory_name = "pokemon_species_info"
#     if not os.path.exists(f"../{directory_name}"):
#         os.makedirs(f"../{directory_name}")
                    
#     try:
#         request_details = request.Request(url, headers=headers)
#         response = request.urlopen(request_details).read()
#         data = json.loads(response.decode("utf-8"))
#         with open(f"../{directory_name}/{filename}", "w", encoding="utf-8") as file:
#             print(f"Creating file for {filename}")
#             json.dump(data, file, ensure_ascii=True, indent=4)
#         # print(response.decode("utf-8"))
#     except error.HTTPError as error:
#         print(error)

# def change_filenames():
#     os.chdir('pokemon_varieties_info')
#     pokemon_files = sorted(os.listdir(), key=lambda x: int(x.split("_")[0]))
#     for pokemon_file in pokemon_files:
#         os.rename(pokemon_file, pokemon_file.upper())

def get_all_species():
    with open("pokedex.csv", "r") as f:
        csv_reader = csv.DictReader(f)
        url = "https://pokeapi.co/api/v2/pokemon-species/"
        for row in csv_reader:
            full_url = f"{url}{row['name']}"
            retrieve_species_data(full_url)

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

def main():
    url = "https://pokeapi.co/api/v2/pokedex/1/"
    header = ("index", "id" "name")
    header_species = ("index", "id", "name", "type1", "type2", "generation", "apid")
    record_data(header, "pokedex.csv")
    retrieve_data(url)
    record_data(header_species, "pokedex_species.csv")
    get_all_species()
main()

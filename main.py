import json, csv, os, requests

URL = "https://pokeapi.co/api/v2/pokemon-species"
ENTRIES = 1025
SPECIES_LOGFILE = "log_species"
VARIETY_LOGFILE = "log_variety"
SPRITES_LOGFILE = "log_sprites"

def download_sprite(logfile, url, id, name, entry):
    sprites_dirname = "pokemon_sprites"
    if not os.path.exists(sprites_dirname):
        os.makedirs(sprites_dirname)

    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(f"{sprites_dirname}/{id}-{entry}-{name}.png", 'wb') as file:
            file.write(r.content)
    except requests.exceptions.RequestException as e:
        line = f"ERROR {e} on entry {entry}\n"
    except requests.exceptions.Timeout as e:
        line = f"Timeout ERROR {e} on entry: {entry}\n"
    except requests.exceptions.ConnectionError as e:
        line = f"Connection ERROR {e} on entry: {entry}\n"
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            line = f"A 404 HTTP error on entry: {entry}"
    except Exception as e:
        line = f"An unexpected ERROR occurred {e} on entry: {entry}\n"
    else:
        line = f"Downloaded entry: {entry}\n"
    
    log(line, logfile)
    
def validate_types(type):
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
        case _:
            type = 0
    return type
    

def validate_generation(generation_str):
    match generation_str:
        case "generation-i":
            generation = 1
        case "generation-ii":
            generation = 2
        case "generation-iii":
            generation = 3
        case "generation-iv":
            generation = 4
        case "generation-v":
            generation = 5
        case "generation-vi":
            generation = 6
        case "generation-vii":
            generation = 7
        case "generation-viii":
            generation = 8
        case "generation-ix":
            generation = 9
        case _:
            generation = 0
    return generation

def filter(pokemon):
    pokemon_not_allowed = ["cap", "star", "belle", "phd", "libre", "cosplay", "breed", "starter", "totem", "build", "mode", "gulping", "gorging"]
    split_pokemon_name = pokemon.split("-")
    if not set(pokemon_not_allowed).isdisjoint(set(split_pokemon_name)):
        return False
    else:
        return True

def log(line, file):

    with open(file, "a", newline="") as log:
        log.write(line)

def record(data):

    with open("pokedex_test01.csv", "a", newline="") as pokedex:
        writer = csv.writer(pokedex)
        writer.writerow(data)

def request(url, file, cnt):
    # entry = url.split("/")[6]
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        line = f"ERROR {e} on entry {cnt}\n"
    except requests.exceptions.Timeout as e:
        line = f"Timeout ERROR {e} on entry: {cnt}\n"
    except requests.exceptions.ConnectionError as e:
        line = f"Connection ERROR {e} on entry: {cnt}\n"
    except Exception as e:
        line = f"An unexpected ERROR occurred {e} on entry: {cnt}\n"
    else:
        line = f"SUCCESS on entry {cnt}\n"
        return response
    finally:
        log(line, file)

if __name__ == "__main__":
    header = ["id", "entry", "name", "is_baby", "is_legendary", "is_mythical", "generation", "type1", "type2", "hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]
    record(header)
    pokemon_counter = 0
    for entry in range(ENTRIES):
        entry = entry + 1
        request_url = f"{URL}/{entry}"
        response = request(request_url, SPECIES_LOGFILE, entry)
        data = response.json()
        pokemon_baby = 0 if data["is_baby"] == False else 1
        pokemon_legendary = 0 if data["is_legendary"] == False else 1
        pokemon_mythical = 0 if data["is_mythical"] == False else 1
        pokemon_generation = validate_generation(data["generation"].get("name"))
        for item in data["varieties"]:
            pokemon_name = item["pokemon"]["name"]
            if filter(pokemon_name):
                split_pokemon_name = pokemon_name.split("-")
                pokemon_zygarde = set(("10", "50"))
                if not set(pokemon_zygarde).isdisjoint(set(split_pokemon_name)):
                    if pokemon_name == "zygarde-50" or pokemon_name == "zygarde-10":
                        continue
                    else:
                        if pokemon_name == "zygarde-10-power-construct":
                            pokemon_name = "zygarde-10-form"
                        elif pokemon_name == "zygarde-50-power-construct":
                            pokemon_name = "zygarde-50-form"

                pokemon = []
                pokemon_counter += 1
                pokemon_url = item["pokemon"]["url"]
                pokemon_specie_id = int(pokemon_url.split("/")[6])
                pokemon_baby = 0 if data["is_baby"] == False else 1
                pokemon_legendary = 0 if data["is_legendary"] == False else 1
                pokemon_mythical = 0 if data["is_mythical"] == False else 1
                pokemon_generation = validate_generation(data["generation"].get("name"))
                pokemon_data = request(pokemon_url, VARIETY_LOGFILE, pokemon_counter)
                pokemon_data_json = pokemon_data.json()
                # pokemon_sprite_url = pokemon_data_json["sprites"]["front_default"]
                pokemon_sprite_url = pokemon_data_json["sprites"]["other"]["official-artwork"]["front_default"]
                print(pokemon_sprite_url)
                try:
                    pokemon_type1 = validate_types(pokemon_data_json["types"][0]["type"].get("name"))
                    pokemon_type2 = validate_types(pokemon_data_json["types"][1]["type"].get("name"))
                except IndexError as e:
                    pokemon_type2 = validate_types(0)
                
                pokemon_hp = pokemon_data_json["stats"][0]["base_stat"]
                pokemon_attack = pokemon_data_json["stats"][1]["base_stat"]
                pokemon_defense = pokemon_data_json["stats"][2]["base_stat"]
                pokemon_spattack = pokemon_data_json["stats"][3]["base_stat"]
                pokemon_spdefense = pokemon_data_json["stats"][4]["base_stat"]
                pokemon_speed = pokemon_data_json["stats"][5]["base_stat"]

                pokemon.append(pokemon_counter)
                pokemon.append(entry)
                pokemon.append(pokemon_name)
                pokemon.append(pokemon_baby)
                pokemon.append(pokemon_legendary)
                pokemon.append(pokemon_mythical)
                pokemon.append(pokemon_generation)
                pokemon.append(pokemon_type1)
                pokemon.append(pokemon_type2)
                pokemon.append(pokemon_hp)
                pokemon.append(pokemon_attack)
                pokemon.append(pokemon_defense)
                pokemon.append(pokemon_spattack)
                pokemon.append(pokemon_spdefense)
                pokemon.append(pokemon_speed)
                download_sprite(SPRITES_LOGFILE, pokemon_sprite_url, pokemon_counter, pokemon_name, entry)
                record(pokemon)
            else:
                continue
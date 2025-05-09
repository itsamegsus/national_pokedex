import psycopg2
import csv

MAINFILE = "pokedex_test01.csv"
DBNAME = "pokedex"
DBUSER = "postgres"
DBPASS = "admin"
DBHOST = "localhost"


try:
    con = psycopg2.connect(
        dbname = DBNAME,
        user = DBUSER, 
        host = DBHOST,
        password = DBPASS
    )
    cur = con.cursor()    
    queries = ("""
        DROP TABLE IF EXISTS pokemon CASCADE
        """,
        '''
        CREATE TABLE IF NOT EXISTS pokemon (
            pokemon_id INTEGER GENERATED ALWAYS AS IDENTITY,
            pokemon_entry INTEGER NOT NULL,
            pokemon_name VARCHAR(255) NOT NULL,
            pokemon_type1 INTEGER NOT NULL,
            pokemon_type2 INTEGER NOT NULL,
            pokemon_hp INTEGER NOT NULL,
            pokemon_attack INTEGER NOT NULL,
            pokemon_defense INTEGER NOT NULL,
            pokemon_spattack INTEGER NOT NULL,
            pokemon_spdefense INTEGER NOT NULL,
            pokemon_speed INTEGER NOT NULL,
            pokemon_generation INTEGER NOT NULL, 
            pokemon_spriteid INTEGER NOT NULL,
            PRIMARY KEY(pokemon_id),
            CONSTRAINT fk_pokemon_type1 FOREIGN KEY (pokemon_type1)
            REFERENCES pokemon_types (type_id),
            CONSTRAINT fk_pokemon_type2 FOREIGN KEY (pokemon_type2)
            REFERENCES pokemon_types (type_id),
            CONSTRAINT fk_pokemon_generation FOREIGN KEY (pokemon_generation)
            REFERENCES pokemon_generations (generation_id)
        );
    ''')
    for query in queries:
        cur.execute(query)

    with open(MAINFILE, "r") as db:
        pokedex = csv.DictReader(db)
        for pokemon in pokedex:
            information = list(pokemon.values())
            information.pop(0)
            if int(information[7])== int('0'):
                information[7] = None
            query = '''
            INSERT INTO pokemon (
            pokemon_entry,
            pokemon_name,
            pokemon_type1,
            pokemon_type2,
            pokemon_hp,
            pokemon_attack,
            pokemon_defense,
            pokemon_spattack,
            pokemon_spdefense,
            pokemon_speed,
            pokemon_generation, 
            pokemon_spriteid
            ) VALUES {0}'''.format(tuple(pokemon.values()))
            print(query.format(tuple(pokemon)))
            cur.execute(query)

    queries = ("""
        DROP TABLE IF EXISTS pokemon_types CASCADE
        """,
        """
        CREATE TABLE IF NOT EXISTS pokemon_types (
            type_id INTEGER GENERATED ALWAYS AS IDENTITY,
            type_name VARCHAR(255) NOT NULL,
            PRIMARY KEY(type_id)
        ) 
        """)
    for query in queries:
        cur.execute(query)
    # cur.execute(sql.SQL("DROP TABLE {}").format(sql.Identifier("pokemon_types")))

    pokemon_types = ("normal", "grass", "fire", "water", "electric", "fighting", "flying", "poison", "ground", "psychic", "rock", "ice", "bug", "dragon", "ghost", "dark", "steel", "fairy")
    for pokemon_type in pokemon_types:
        query = "INSERT INTO pokemon_types (type_name) VALUES ('{0}')".format(pokemon_type)
        print(query)
        cur.execute(query)

    queries = ("""
        DROP TABLE IF EXISTS pokemon_generations CASCADE
        """,
        """
        CREATE TABLE IF NOT EXISTS pokemon_generations (
            generation_id INTEGER GENERATED ALWAYS AS IDENTITY,
            generation_name VARCHAR(255) NOT NULL,
            PRIMARY KEY(generation_id)
        ) 
        """)
    for query in queries:
        cur.execute(query)

    generation_names = ("Kanto", "Johto", "Hoenn", "Sinnoh", "Unova", "Kalos", "Alola", "Galar", "Paldea")
    print(generation_names)
    for name in generation_names:
        query = "INSERT INTO pokemon_generations (generation_name) VALUES ('{0}')".format(name)
        print(query)
        cur.execute(query)

    con.commit()
    cur.close()

except Exception as e:
    print(e)
finally: 
    if con is not None:
        con.close()
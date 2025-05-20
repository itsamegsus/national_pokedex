from flask import Flask, render_template, redirect, url_for, request
import psycopg2

app = Flask(__name__)

DBNAME = "pokedex"
DBUSER = "postgres"
DBPASS = "admin"
DBHOST = "localhost"

def connection():
    try:
        con = psycopg2.connect(
            dbname = DBNAME,
            user = DBUSER, 
            host = DBHOST,
            password = DBPASS
        )
        return con
    except Exception as e:
        return e
    
def get_types():
    query_types = 'SELECT * FROM pokemon_types;'
    con = connection()
    cur = con.cursor()
    cur.execute(query_types)
    types = cur.fetchall()
    cur.close()
    con.close()
    return types

def get_generations():
    query_region = 'SELECT * FROM pokemon_generations'
    con = connection()
    cur = con.cursor()
    cur.execute(query_region)
    regions = cur.fetchall()
    cur.close()
    con.close()
    return regions

@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/home', methods=["POST", "GET"])
def home():
    query_search = """
            SELECT p.pokemon_id, p.pokemon_entry, p.pokemon_name, pt1.type_name, pt2.type_name, pg.generation_name
            FROM pokemon AS p
            LEFT JOIN pokemon_types AS pt1 ON p.pokemon_type1 = pt1.type_id
            LEFT JOIN pokemon_types AS pt2 ON p.pokemon_type2 = pt2.type_id
            LEFT JOIN pokemon_generations AS pg ON p.pokemon_generation = pg.generation_id
        """
    types = get_types()
    regions = get_generations()

    if request.method == "POST":
        try:    
            
            con = connection()
            cur = con.cursor()            
            
            name = request.form["name"]
            type1 = int(request.form["pokemon-type-1"])
            type2 = int(request.form["pokemon-type-2"])
            region = int(request.form["pokemon-region"])
           
            query_search += f" WHERE p.pokemon_name LIKE '%{name}%'" 

            if type1 != 0:
                query_search += f" AND p.pokemon_type1 = {type1}"

            if type2 != 0:
                query_search += f" AND p.pokemon_type2 = {type2}"

            if region != 0:
                query_search += f" AND p.pokemon_generation = {region}"

            cur.execute(query_search)
            pokemon = cur.fetchall()
            print(type(pokemon))
            cur.close()
            con.close()
            
            return render_template('index.html', types=types, regions=regions, nm=name, t1=type1, t2=type2, re=region, pokemon=pokemon)
        except Exception as e:
            return render_template('index.html', types=str(e))
    else:
        print("else no post")
        try:
            con = connection()
            cur = con.cursor()
            cur.execute(query_search)
            pokemon = cur.fetchall()
            cur.close()
            con.close()   
            return render_template('index.html', types=types, regions=regions, pokemon=pokemon)
        except Exception as e:
            return render_template('index.html', types=str(e))
        
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
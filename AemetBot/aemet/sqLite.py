import sqlite3
from .constants import DATA_BASE_NAME


def create_initialize_database():
    # Create community.db database
    conn = sqlite3.connect(DATA_BASE_NAME)
    # Create cursor
    cursor = conn.cursor()
    # Create table
    create_data_base(cursor)
    # Insert values into database
    initialize_data_base(cursor)
    # Execute the previous command
    conn.commit()
    # Close the connection
    conn.close()


def create_data_base(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS communities (code TEXT PRIMARY KEY, community TEXT NOT NULL, 
        province TEXT NOT NULL, abbreviation TEXT NOT NULL)""")


def initialize_data_base(cursor):
    cursor.execute("INSERT OR IGNORE INTO communities VALUES ('04', 'Andalucia', 'Almería', 'and'), "
                   "('11', 'Andalucia', 'Cádiz', 'and'),"
                   "('14', 'Andalucia', 'Córdoba', 'and'),"
                   "('18', 'Andalucia', 'Granada', 'and'),"
                   "('21', 'Andalucia', 'Huelva', 'and'),"
                   "('23', 'Andalucia', 'Jaén', 'and'),"
                   "('29', 'Andalucia', 'Málaga', 'and'),"
                   "('41', 'Andalucia', 'Sevilla', 'and'),"
                   "('22', 'Aragon', 'Huesca', 'arn'),"
                   "('44', 'Aragon', 'Teruel', 'arn'),"
                   "('50', 'Aragon', 'Zaragoza', 'arn'),"
                   "('33', 'Asturias', 'Asturias', 'ast'),"
                   "('07', 'Islas Baleares', 'Mallorca', 'bal'),"
                   "('35', 'Islas Canarias', 'Gran canaria', 'coo'),"
                   "('38', 'Islas Canarias', 'La gomera', 'coo'),"
                   "('39', 'Cantabria', 'Cantabria', 'can'),"
                   "('05', 'Castilla Leon', 'Ávila', 'cle'),"
                   "('09', 'Castilla Leon', 'Burgos', 'cle'),"
                   "('24', 'Castilla Leon', 'León', 'cle'),"
                   "('34', 'Castilla Leon', 'Palencia', 'cle'),"
                   "('37', 'Castilla Leon', 'Salamanca', 'cle'),"
                   "('40', 'Castilla Leon', 'Segovia', 'cle'),"
                   "('42', 'Castilla Leon', 'Soria', 'cle'),"
                   "('47', 'Castilla Leon', 'Valladolid', 'cle'),"
                   "('49', 'Castilla Leon', 'Zamora', 'cle'),"
                   "('02', 'Castilla La Mancha', 'Albacete', 'clm'),"
                   "('13', 'Castilla La Mancha', 'Ciudad Real', 'clm'),"
                   "('16', 'Castilla La Mancha', 'Cuenca', 'clm'),"
                   "('19', 'Castilla La Mancha', 'Guadalajara', 'clm'),"
                   "('45', 'Castilla La Mancha', 'Toledo', 'clm'),"
                   "('08', 'Catalunya', 'Barcelona', 'cat'),"
                   "('17', 'Catalunya', 'Girona', 'cat'),"
                   "('25', 'Catalunya', 'Lleida', 'cat'),"
                   "('43', 'Catalunya', 'Tarragona', 'cat'),"
                   "('03', 'Comunidad Valenciana', 'Alacant/Alicante', 'val'),"
                   "('12', 'Comunidad Valenciana', 'Castelló/Castellón', 'val'),"
                   "('46', 'Comunidad Valenciana', 'València/Valencia', 'val'),"
                   "('06', 'Extremadura', 'Badajoz', 'ext'),"
                   "('10', 'Extremadura', 'Cáceres', 'ext'),"
                   "('15', 'Galicia', 'A Coruña', 'gal'),"
                   "('27', 'Galicia', 'Lugo', 'gal'),"
                   "('32', 'Galicia', 'Ourense', 'gal'),"
                   "('36', 'Galicia', 'Pontevedra', 'gal'),"
                   "('28', 'Comunidad de Madrid', 'Madrid', 'mad'),"
                   "('30', 'Murcia', 'Murcia', 'mur'),"
                   "('31', 'Navarra', 'Navarra', 'nav'),"
                   "('01', 'Euskadi', 'Araba/Álava', 'pva'),"
                   "('48', 'Euskadi', 'Bizkaia', 'pva'),"
                   "('20', 'Euskadi', 'Gipuzkoa', 'pva'),"
                   "('26', 'La Rioja', 'La Rioja', 'rio')")


def check_values(conn):
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM communities LIMIT 1')
    return cursor.fetchone()[0]
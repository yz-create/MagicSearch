import sys
import os

# Ajouter TOUS les chemins nécessaires au PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(project_root, 'src')

sys.path.insert(0, project_root)
sys.path.insert(0, src_path)

# Maintenant on peut importer
from db_connection import DBConnection

def find_user_table(cursor):
    """Trouve le nom exact de la table User dans la base"""
    # Chercher toutes les variantes possibles
    cursor.execute("""
        SELECT table_schema, table_name 
        FROM information_schema.tables 
        WHERE LOWER(table_name) = 'user'
        ORDER BY table_schema = 'public' DESC;
    """)
    
    tables = cursor.fetchall()
    if tables:
        print(f"\n📋 Tables trouvées:")
        for table in tables:
            # Gérer à la fois les tuples et les dictionnaires
            if isinstance(table, dict):
                schema = table['table_schema']
                name = table['table_name']
            else:
                schema = table[0]
                name = table[1]
            print(f"   • {schema}.{name}")
        
        # Retourner le premier résultat
        first_table = tables[0]
        if isinstance(first_table, dict):
            return (first_table['table_schema'], first_table['table_name'])
        else:
            return first_table
    return None

def list_all_tables(cursor):
    """Liste toutes les tables de la base pour diagnostiquer"""
    cursor.execute("""
        SELECT table_schema, table_name 
        FROM information_schema.tables 
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY table_schema, table_name;
    """)
    
    tables = cursor.fetchall()
    print(f"\n📊 Toutes les tables de la base ({len(tables)}):")
    for table in tables:
        if isinstance(table, dict):
            print(f"   • {table['table_schema']}.{table['table_name']}")
        else:
            print(f"   • {table[0]}.{table[1]}")

def migrate():
    """Fix the User table to auto-generate idUser"""
    
    conn = None
    try:
        print("🔌 Connexion à la base de données via DBConnection...")
        
        db = DBConnection()
        conn = db.connection
        cursor = conn.cursor()
        
        # Lister toutes les tables pour diagnostiquer
        list_all_tables(cursor)
        
        # Trouver la table User
        print("\n🔍 Recherche de la table User...")
        table_info = find_user_table(cursor)
        
        if not table_info:
            print("\n❌ Aucune table 'User' trouvée dans la base de données!")
            print("\n💡 Suggestions:")
            print("   1. Vérifiez que la table existe bien dans votre base")
            print("   2. Le nom pourrait être différent (user, users, Users, etc.)")
            print("   3. Créez la table avec votre ORM si elle n'existe pas encore")
            return
        
        schema_name = table_info[0]
        table_name = table_info[1]
        full_table_name = f'"{schema_name}"."{table_name}"'
        
        print(f"✓ Table trouvée: {full_table_name}")
        
        # Définir le search_path
        cursor.execute(f'SET search_path TO {schema_name}, public;')
        
        # Nom de la séquence (utiliser le nom exact de la table)
        seq_name = f'{table_name}_idUser_seq'
        
        # Vérifier si la séquence existe déjà
        print(f"\n🔍 Vérification de la séquence '{seq_name}'...")
        cursor.execute("""
            SELECT 1 FROM pg_sequences 
            WHERE schemaname = %s AND sequencename = %s;
        """, (schema_name, seq_name))
        
        if cursor.fetchone() is None:
            print(f"\n🔧 Création de la séquence pour idUser...")
            
            # Créer la séquence
            cursor.execute(f'CREATE SEQUENCE "{schema_name}"."{seq_name}";')
            print("   ✓ Séquence créée")
            
            # Définir la valeur initiale de la séquence
            cursor.execute(f"""
                SELECT setval('"{schema_name}"."{seq_name}"', 
                COALESCE((SELECT MAX("idUser") FROM {full_table_name}), 0) + 1);
            """)
            result = cursor.fetchone()
            # Gérer dict ou tuple
            setval = result['setval'] if isinstance(result, dict) else result[0]
            print(f"   ✓ Valeur initiale définie à: {setval}")
            
            # Associer la séquence à la colonne
            cursor.execute(f"""
                ALTER TABLE {full_table_name}
                ALTER COLUMN "idUser" 
                SET DEFAULT nextval('"{schema_name}"."{seq_name}"'::regclass);
            """)
            print("   ✓ Séquence associée à la colonne idUser")
            
            conn.commit()
            print("\n✅ Migration réussie !")
            print("   → La colonne idUser s'auto-incrémentera désormais")
        else:
            print("\n⚠️  La séquence existe déjà, aucune action nécessaire")
        
        cursor.close()
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        if conn:
            conn.rollback()
        import traceback
        traceback.print_exc()
        raise
    finally:
        if conn:
            conn.close()
            print("\n🔌 Connexion fermée")

if __name__ == "__main__":
    print("=" * 60)
    print("  Migration: Fix User table auto-increment")
    print("=" * 60)
    print(f"Project root: {project_root}")
    print(f"Src path: {src_path}")
    print("=" * 60)
    migrate()
    print("=" * 60)
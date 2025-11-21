import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(project_root, 'src')

sys.path.insert(0, project_root)
sys.path.insert(0, src_path)

from db_connection import DBConnection


def find_user_table(cursor):
    """Find the exact name of the User table in the database."""
    cursor.execute("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE LOWER(table_name) = 'user'
        ORDER BY table_schema = 'public' DESC;
    """)

    tables = cursor.fetchall()
    if tables:
        print("Tables found:")
        for table in tables:
            if isinstance(table, dict):
                schema = table['table_schema']
                name = table['table_name']
            else:
                schema = table[0]
                name = table[1]
            print(f"   • {schema}.{name}")

        first_table = tables[0]
        if isinstance(first_table, dict):
            return (first_table['table_schema'], first_table['table_name'])
        else:
            return first_table
    return None


def list_all_tables(cursor):
    """List all tables in the database for diagnostics."""
    cursor.execute("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY table_schema, table_name;
    """)

    tables = cursor.fetchall()
    print(f"\nAll tables in the database ({len(tables)}):")
    for table in tables:
        if isinstance(table, dict):
            print(f"   • {table['table_schema']}.{table['table_name']}")
        else:
            print(f"   • {table[0]}.{table[1]}")


def migrate():
    """Fix the User table to auto-generate idUser."""
    conn = None
    try:
        print(" Connecting to the database via DBConnection...")

        db = DBConnection()
        conn = db.connection
        cursor = conn.cursor()

        list_all_tables(cursor)

        print("\n Searching for the User table...")
        table_info = find_user_table(cursor)

        if not table_info:
            print("No 'User' table found in the database!")
            print("Suggestions:")
            print("   1. Make sure the table actually exists")
            print("   2. The name might be different (user, users, Users, etc.)")
            print("   3. Create the table with your ORM if it does not exist yet")
            return

        schema_name = table_info[0]
        table_name = table_info[1]
        full_table_name = f'"{schema_name}"."{table_name}"'

        print(f"✓ Table found: {full_table_name}")

        cursor.execute(f'SET search_path TO {schema_name}, public;')

        seq_name = f'{table_name}_idUser_seq'

        print(f"Checking sequence '{seq_name}'...")
        cursor.execute("""
            SELECT 1 FROM pg_sequences
            WHERE schemaname = %s AND sequencename = %s;
        """, (schema_name, seq_name))

        if cursor.fetchone() is None:
            print("Creating sequence for idUser...")

            cursor.execute(f'CREATE SEQUENCE "{schema_name}"."{seq_name}";')
            print("Sequence created")

            cursor.execute(f"""
                SELECT setval('"{schema_name}"."{seq_name}"',
                COALESCE((SELECT MAX("idUser") FROM {full_table_name}), 0) + 1);
            """)
            result = cursor.fetchone()
            setval = result['setval'] if isinstance(result, dict) else result[0]
            print(f"   ✓ Initial value set to: {setval}")

            cursor.execute(f"""
                ALTER TABLE {full_table_name}
                ALTER COLUMN "idUser"
                SET DEFAULT nextval('"{schema_name}"."{seq_name}"'::regclass);
            """)
            print("   ✓ Sequence attached to idUser column")

            conn.commit()
            print(" Migration successful!")
            print("   → The idUser column will now auto-increment")
        else:
            print("Sequence already exists, no action needed")

        cursor.close()

    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
        import traceback
        traceback.print_exc()
        raise
    finally:
        if conn:
            conn.close()
            print("Connection closed")


if __name__ == "__main__":
    print("=" * 60)
    print("  Migration: Fix User table auto-increment")
    print("=" * 60)
    print(f"Project root: {project_root}")
    print(f"Src path: {src_path}")
    print("=" * 60)
    migrate()
    print("=" * 60)

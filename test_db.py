# test_db.py
import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="ecommerce",
        user="usuario", 
        password="senha",
        port="5432"
    )
    print("✅ Conectado ao PostgreSQL com sucesso!")
    
    # Testar uma query simples
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"📊 PostgreSQL Version: {version[0]}")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Erro na conexão: {e}")   
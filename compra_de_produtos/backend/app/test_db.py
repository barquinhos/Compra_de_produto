from database.session import engine, SessionLocal

def test_connection():
    try:
        with engine.connect() as connection:
            print("✅ Conexão com PostgreSQL bem-sucedida!")
            
        # Operação simples
        with SessionLocal() as db:
            result = db.execute("SELECT version()")
            version = result.scalar()
            print(f"📊 PostgreSQL Version: {version}")
            
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")

if __name__ == "__main__":
    test_connection()
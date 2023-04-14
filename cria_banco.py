import sqlite3

connecttion = sqlite3.connect('banco.db')
cursor = connecttion.cursor()

CRIA_TABELA = "CREATE TABLE IF NOT EXISTS hoteis (hotel_id text PRIMARY KEY,\
    nome text, estrela real, diaria real, cidade text)"

cursor.execute(CRIA_TABELA)

connecttion.commit()
connecttion.close()

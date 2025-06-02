#!/usr/bin/env python3
"""
Скрипт для просмотра содержимого базы данных Cinema API
"""
import sqlite3
import json
from datetime import datetime

def connect_db(db_path='data/cinema_v2.db'):
    """Подключение к базе данных"""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Для доступа к колонкам по имени
        return conn
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")
        return None

def show_tables(conn):
    """Показать все таблицы"""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = cursor.fetchall()
    
    print("🗂️  Таблицы в базе данных:")
    print("=" * 40)
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) as count FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"📋 {table[0]} ({count} записей)")
    print()

def show_table_data(conn, table_name, limit=10):
    """Показать данные из таблицы"""
    cursor = conn.cursor()
    
    # Получаем структуру таблицы
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    print(f"📊 Структура таблицы '{table_name}':")
    print("-" * 60)
    for col in columns:
        print(f"  {col[1]} ({col[2]}) {'NOT NULL' if col[3] else 'NULL'} {'PRIMARY KEY' if col[5] else ''}")
    
    # Получаем данные
    cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
    rows = cursor.fetchall()
    
    if rows:
        print(f"\n📦 Данные таблицы '{table_name}' (показано {len(rows)} из них):")
        print("-" * 60)
        for i, row in enumerate(rows, 1):
            print(f"  📝 Запись {i}:")
            for col_name in row.keys():
                value = row[col_name]
                if value is not None and len(str(value)) > 100:
                    value = str(value)[:100] + "..."
                print(f"    {col_name}: {value}")
            print()
    else:
        print(f"\n📭 Таблица '{table_name}' пуста")
    print()

def main():
    print("🎬 Cinema API - Просмотр базы данных")
    print("=" * 50)
    
    conn = connect_db()
    if not conn:
        return
    
    try:
        # Показать все таблицы
        show_tables(conn)
        
        # Показать данные из каждой таблицы
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            show_table_data(conn, table_name, limit=5)
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main() 
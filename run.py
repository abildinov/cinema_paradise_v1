#!/usr/bin/env python3
"""
Скрипт для запуска Cinema API сервера
"""
import sys
import subprocess
import pkg_resources

def check_dependencies():
    """Проверка установленных зависимостей"""
    required_packages = [
        'fastapi>=0.104.0',
        'uvicorn>=0.24.0',
        'sqlalchemy>=2.0.20',
        'pydantic>=2.5.0'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            pkg_resources.require(package)
            print(f"✅ {package} установлен")
        except pkg_resources.DistributionNotFound:
            missing_packages.append(package)
            print(f"❌ {package} не найден")
        except pkg_resources.VersionConflict as e:
            missing_packages.append(package)
            print(f"⚠️  {package} - конфликт версий: {e}")
    
    return missing_packages

def install_dependencies():
    """Установка недостающих зависимостей"""
    print("🔧 Установка зависимостей...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Зависимости установлены успешно")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки зависимостей: {e}")
        return False

def run_server():
    """Запуск сервера"""
    print("🚀 Запуск Cinema API сервера...")
    try:
        import uvicorn
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except ImportError:
        print("❌ uvicorn не найден. Попытка запуска через Python модуль...")
        subprocess.run([sys.executable, '-m', 'uvicorn', 'main:app', '--reload', '--host', '0.0.0.0', '--port', '8000'])

def main():
    print("🎬 Cinema API - Запуск сервера")
    print("=" * 40)
    
    # Проверка Python версии
    python_version = sys.version_info
    print(f"🐍 Python версия: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Требуется Python 3.8 или выше!")
        sys.exit(1)
    
    # Проверка зависимостей
    missing = check_dependencies()
    
    if missing:
        print(f"\n⚠️  Найдены недостающие зависимости: {len(missing)}")
        response = input("Установить автоматически? (y/n): ").strip().lower()
        
        if response in ['y', 'yes', 'да']:
            if not install_dependencies():
                sys.exit(1)
        else:
            print("Установите зависимости вручную:")
            print("pip install -r requirements.txt")
            sys.exit(1)
    
    print("\n🌐 Сервер будет доступен по адресам:")
    print("• Swagger UI: http://localhost:8000/docs")
    print("• ReDoc: http://localhost:8000/redoc")
    print("• API: http://localhost:8000/api/v1/")
    print("\n⏹️  Для остановки нажмите Ctrl+C\n")
    
    # Запуск сервера
    run_server()

if __name__ == "__main__":
    main() 
# 🐍 Установка Python 3.11 для Cinema API

## ⚠️ Проблема
Python 3.13 несовместим с SQLAlchemy 2.0.x и некоторыми другими пакетами.

## ✅ Решение: Python 3.11

### 1. **Скачать Python 3.11**
- Перейдите на [python.org/downloads](https://python.org/downloads/)
- Скачайте **Python 3.11.10** (последняя стабильная версия)
- Выберите "Windows installer (64-bit)"

### 2. **Установка**
1. Запустите установщик
2. ✅ **ОБЯЗАТЕЛЬНО**: Отметьте "Add Python to PATH"
3. Выберите "Customize installation"
4. На экране "Optional Features" оставьте все по умолчанию
5. На экране "Advanced Options":
   - ✅ Install for all users
   - ✅ Add Python to environment variables
   - ✅ Precompile standard library
   - ✅ Download debugging symbols
6. Нажмите "Install"

### 3. **Проверка установки**
```cmd
python --version
# Должно показать: Python 3.11.x
```

### 4. **Настройка проекта**
```cmd
# Создание виртуального окружения с Python 3.11
python -m venv venv311

# Активация
venv311\Scripts\activate.bat

# Установка зависимостей
pip install --upgrade pip
pip install -r requirements.txt

# Запуск API
python main.py
```

## 🚀 Альтернативные способы

### Если у вас уже установлен Python 3.13

#### Способ 1: pyenv-win (рекомендуемый)
```powershell
# Установка pyenv-win
git clone https://github.com/pyenv-win/pyenv-win.git %USERPROFILE%\.pyenv

# Добавьте в PATH:
# %USERPROFILE%\.pyenv\pyenv-win\bin
# %USERPROFILE%\.pyenv\pyenv-win\shims

# Установка Python 3.11
pyenv install 3.11.10
pyenv local 3.11.10
```

#### Способ 2: Conda/Miniconda
```cmd
# Скачайте Miniconda с conda.io
# Затем:
conda create -n cinema python=3.11
conda activate cinema
pip install -r requirements.txt
```

#### Способ 3: Docker (если установлен)
```cmd
# Используйте готовый Dockerfile
docker build -f Dockerfile.py311 -t cinema-api .
docker run -p 8000:8000 cinema-api
```

## 🎯 После установки Python 3.11

```cmd
# Проверьте версию
python --version

# Создайте новое виртуальное окружение
python -m venv venv

# Активируйте
venv\Scripts\activate.bat

# Установите зависимости
pip install --upgrade pip
pip install -r requirements.txt

# Запустите API
python main.py
```

## 🌐 Результат
После установки Python 3.11 у вас будет:
- ✅ Полная совместимость с SQLAlchemy
- ✅ Работающая база данных SQLite/PostgreSQL
- ✅ Все 36 API endpoints
- ✅ JWT аутентификация
- ✅ Swagger документация на http://localhost:8000/docs

## 📋 Проверочный список
- [ ] Python 3.11.x установлен
- [ ] Виртуальное окружение создано
- [ ] Зависимости установлены без ошибок
- [ ] `python main.py` запускается без ошибок
- [ ] API доступен на localhost:8000/docs 
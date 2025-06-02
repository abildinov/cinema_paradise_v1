# 🔗 Настройка Git репозитория и GitHub

## 📋 **Пошаговая инструкция создания репозитория**

### **Шаг 1: Инициализация локального репозитория**

Откройте **новое окно PowerShell** или **Command Prompt** в папке проекта и выполните:

```bash
# Инициализация git репозитория
git init

# Добавление всех файлов (кроме исключенных в .gitignore)
git add .

# Первый коммит
git commit -m "🎬 Initial commit: Cinema Paradise v1.0 - Working FastAPI + React system"
```

### **Шаг 2: Создание репозитория на GitHub**

1. **Перейдите на GitHub.com** и войдите в свой аккаунт
2. **Нажмите "New repository"** (зеленая кнопка)
3. **Заполните данные:**
   - **Repository name:** `cinema-paradise`
   - **Description:** `🎬 Cinema Paradise - Полнофункциональная система управления кинотеатром с FastAPI + React`
   - **Visibility:** Public или Private (на ваш выбор)
   - **НЕ создавайте** README.md, .gitignore, license (у нас уже есть)

4. **Нажмите "Create repository"**

### **Шаг 3: Связывание с GitHub**

После создания репозитория GitHub покажет команды. Выполните:

```bash
# Добавление удаленного репозитория
git remote add origin https://github.com/ВАШ-USERNAME/cinema-paradise.git

# Указание основной ветки
git branch -M main

# Загрузка на GitHub
git push -u origin main
```

### **Шаг 4: Проверка загрузки**

1. **Обновите страницу** вашего репозитория на GitHub
2. **Убедитесь, что все файлы загружены:**
   - ✅ `cinema_api_tortoise.py` - основной API файл
   - ✅ `frontend/` - папка с веб-интерфейсом
   - ✅ `README.md` - документация
   - ✅ `requirements.txt` - зависимости
   - ✅ `.gitignore` - исключения
   - ❌ `data/` - база данных (исключена)
   - ❌ `__pycache__/` - кэш Python (исключен)
   - ❌ `venv/` - виртуальное окружение (исключено)

## 🎯 **Результат**

После выполнения всех шагов у вас будет:

✅ **Рабочий локальный Git репозиторий**  
✅ **Репозиторий на GitHub с полным кодом**  
✅ **Возможность откатываться к текущей версии**  
✅ **Готовность к разработке мобильного приложения**  

## 🚀 **Следующие шаги**

После создания репозитория мы сможем:

1. **Создать ветку для мобильного приложения:**
   ```bash
   git checkout -b feature/mobile-app
   ```

2. **Разрабатывать React Native приложение**

3. **Делать коммиты по ходу разработки:**
   ```bash
   git add .
   git commit -m "📱 Add mobile app: Login screen"
   git push origin feature/mobile-app
   ```

4. **Создавать Pull Request** при завершении

## 🔄 **Полезные Git команды**

```bash
# Проверка статуса
git status

# Просмотр истории коммитов
git log --oneline

# Создание новой ветки
git checkout -b feature/new-feature

# Переключение между ветками
git checkout main
git checkout feature/mobile-app

# Откат к предыдущему коммиту (ОПАСНО!)
git reset --hard HEAD~1

# Просмотр изменений
git diff

# Добавление конкретного файла
git add filename.py

# Отмена изменений в файле
git checkout -- filename.py
```

## 🛡️ **Бэкап стратегия**

**Текущее состояние (до мобильного приложения):**
- 🎬 Полностью рабочая система Cinema Paradise
- ✅ FastAPI сервер с 36+ эндпоинтами  
- ✅ React веб-интерфейс
- ✅ JWT аутентификация
- ✅ Система бронирования билетов
- ✅ Админ панель

**В случае проблем:**
```bash
# Вернуться к стабильной версии
git checkout main
git reset --hard origin/main
```

## 🎭 **Советы**

1. **Делайте коммиты часто** - каждую логическую единицу изменений
2. **Используйте понятные сообщения коммитов:**
   - `📱 Add: Login screen for mobile app`
   - `🐛 Fix: API endpoint authentication issue`
   - `✨ Feature: Movie rating system`
   - `📚 Docs: Update API documentation`

3. **Создавайте отдельные ветки** для крупных фич
4. **Тестируйте перед коммитом** - убедитесь что всё работает

---

**🎬 После создания репозитория мы сможем безопасно разрабатывать мобильное приложение!** 
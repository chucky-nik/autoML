# Инструкция по загрузке проекта в репозиторий

## Файлы для коммита

### Обязательные файлы:
- ✅ `README.md` - описание проекта
- ✅ `requirements.txt` - зависимости
- ✅ `.gitignore` - исключения для Git
- ✅ `notebooks/scrabble_rating_solution.ipynb` - основной ноутбук
- ✅ `src/` - исходный код проекта
- ✅ `INSTRUCTIONS.md` - инструкции по заданию (если есть)
- ✅ `CHECKLIST.md` - чеклист (если есть)

### Опциональные файлы:
- `results/` - графики и submission (обычно не коммитят, но можно)
- `data/.gitkeep` - для сохранения структуры папки

### НЕ коммитить:
- ❌ `data/*.csv` - данные (слишком большие)
- ❌ `results/*.png` - графики (можно, но обычно не нужно)
- ❌ `results/submission.csv` - submission файл
- ❌ `__pycache__/` - кэш Python
- ❌ `.ipynb_checkpoints/` - кэш Jupyter
- ❌ `catboost_info/` - артефакты CatBoost

## Команды для Git

```bash
# Инициализация репозитория (если еще не инициализирован)
git init

# Добавление всех файлов
git add README.md requirements.txt .gitignore
git add notebooks/
git add src/
git add INSTRUCTIONS.md CHECKLIST.md

# Коммит
git commit -m "Initial commit: Scrabble Player Rating Prediction project"

# Добавление remote (замените на ваш URL)
git remote add origin <your-repo-url>

# Push
git push -u origin main
```

## Проверка перед коммитом

```bash
# Проверить, что будет закоммичено
git status

# Убедиться, что данные не попадут в репозиторий
git check-ignore data/*.csv
```

# Инструкция по использованию проекта

## Шаг 1: Установка зависимостей

```bash
cd scrabble_rating_project
pip install -r requirements.txt
```

## Шаг 2: Загрузка данных

### Вариант 1: Использование Kaggle API

1. Установите Kaggle API:
```bash
pip install kaggle
```

2. Настройте API credentials (скачайте `kaggle.json` с сайта Kaggle и поместите в `~/.kaggle/`)

3. Скачайте данные:
```bash
kaggle competitions download -c scrabble-player-rating
unzip scrabble-player-rating.zip -d data/
```

### Вариант 2: Ручная загрузка

1. Перейдите на страницу соревнования: https://www.kaggle.com/competitions/scrabble-player-rating/data
2. Скачайте все файлы данных
3. Поместите их в папку `data/`:
   - `games.csv`
   - `turns.csv`
   - `train.csv`
   - `test.csv`
   - `sample_submission.csv`

## Шаг 3: Запуск ноутбука

```bash
cd notebooks
jupyter notebook scrabble_rating_solution.ipynb
```

Или используйте JupyterLab:
```bash
jupyter lab
```

## Шаг 4: Выполнение анализа

Откройте ноутбук и выполните все ячейки последовательно. Ноутбук включает:

1. **Загрузку и предобработку данных**
2. **Анализ целевой переменной** (распределение, аномалии, временной анализ)
3. **Анализ признаков** (типизация, пропуски, корреляции)
4. **Бейзлайн с LightAutoML** (2 конфигурации)
5. **Собственное решение** (3 пайплайна)
6. **Сравнение результатов и генерацию submission**

## Результаты

После выполнения ноутбука будут созданы:

- Графики в папке `results/`:
  - `target_distribution.png` - распределение целевой переменной
  - `target_temporal.png` - временной анализ
  - `missing_values.png` - анализ пропущенных значений
  - `correlation_matrix.png` - матрица корреляций
  - `feature_importance_correlation.png` - важность признаков
  - `model_comparison.png` - сравнение моделей
  
- Файл submission: `results/submission.csv`

## Примечания

- Убедитесь, что у вас достаточно памяти для обработки данных (особенно `turns.csv` может быть большим)
- Время обучения моделей может занять от 10 до 30 минут в зависимости от конфигурации
- Если возникают проблемы с импортом модулей, убедитесь, что вы запускаете ноутбук из корневой директории проекта


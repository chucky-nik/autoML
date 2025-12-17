# autoML

# Scrabble Player Rating Prediction

## Описание проекта

Проект для решения задачи предсказания рейтинга игроков Scrabble на основе данных соревнования Kaggle [Scrabble Player Rating](https://www.kaggle.com/competitions/scrabble-player-rating/data).

## Структура проекта

```
scrabble_rating_project/
├── data/                    # Данные соревнования (нужно скачать)
│   ├── games.csv
│   ├── turns.csv
│   ├── train.csv
│   ├── test.csv
│   └── sample_submission.csv
├── notebooks/               # Jupyter ноутбуки
│   └── scrabble_rating_solution.ipynb
├── src/                     # Исходный код
│   ├── pipelines/          # Пайплайны обработки данных
│   └── utils/              # Вспомогательные функции
├── results/                 # Результаты (графики, модели, submission)
└── README.md
```

## Установка зависимостей

```bash
pip install -r requirements.txt
```

Или установите зависимости вручную:
```bash
pip install -U lightautoml pandas numpy scikit-learn matplotlib seaborn scipy
pip install lightgbm catboost optuna jupyter notebook
```

## Загрузка данных

Для загрузки данных с Kaggle используйте Kaggle API:

```bash
kaggle competitions download -c scrabble-player-rating
unzip scrabble-player-rating.zip -d data/
```

Или скачайте данные вручную с [страницы соревнования](https://www.kaggle.com/competitions/scrabble-player-rating/data) и поместите файлы в папку `data/`.

## Запуск

1. Откройте ноутбук `notebooks/scrabble_rating_solution.ipynb`
2. Убедитесь, что данные находятся в папке `data/`
3. Запустите все ячейки ноутбука

## Результаты

После выполнения ноутбука будут созданы:
- Графики анализа данных в папке `results/`
- Файл submission в `results/submission.csv`
- Сравнение результатов всех моделей

## Описание решения

### 1. Анализ целевой переменной
- Распределение рейтинга
- Выявление аномальных значений
- Временной анализ

### 2. Анализ признаков
- Типизация признаков (числовые, категориальные, временные)
- Анализ пропущенных значений
- Корреляционный анализ
- Генерация новых признаков

### 3. Бейзлайн с LightAutoML
- Конфигурация 1: TabularAutoML с LightGBM
- Конфигурация 2: TabularAutoML с LightGBM и CatBoost
- Выбор лучшей конфигурации

### 4. Собственное решение
- **Pipeline 1**: LightGBM с автоматическим отбором признаков (Feature Selection)
- **Pipeline 2**: CatBoost с автоматической предобработкой категориальных признаков
- **Pipeline 3**: Простой ансамбль (LightGBM + CatBoost)
- **Pipeline 4**: Автоматическая оптимизация гиперпараметров с Optuna
- **Pipeline 5**: Оптимизированный ансамбль с автоматическим подбором весов

### 5. Выводы и сравнение результатов
- Визуализация сравнения всех моделей
- Детальный текстовый анализ результатов
- Объяснение, какая модель лучше и почему
- Рекомендации для продакшена

## Метрики оценки

Основная метрика: **RMSE** (Root Mean Squared Error)

Дополнительные метрики:
- **MAE** (Mean Absolute Error)
- **R² Score** (коэффициент детерминации)

## Принципы AutoML, реализованные в проекте

1. **Автоматический выбор признаков** - использование SelectKBest и Mutual Information
2. **Автоматическая предобработка** - обработка категориальных признаков и пропусков
3. **Автоматический выбор модели** - сравнение нескольких алгоритмов
4. **Автоматическая оптимизация гиперпараметров** - использование Optuna
5. **Автоматическое ансамблирование** - оптимизация весов ансамбля моделей

## Структура кода

- `src/utils/feature_engineering.py` - функции для генерации признаков и их классификации
- `notebooks/scrabble_rating_solution.ipynb` - основной ноутбук с решением
- `results/` - графики анализа и файл submission.csv

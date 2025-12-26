"""
Модуль для генерации признаков из данных о играх Scrabble.
"""

import pandas as pd
import numpy as np
from typing import Dict, List


def aggregate_turns_features(turns_df: pd.DataFrame) -> pd.DataFrame:
    """
    Агрегирует данные о ходах в признаки на уровне игры.
    
    Parameters
    ----------
    turns_df : pd.DataFrame
        DataFrame с данными о ходах
        
    Returns
    -------
    pd.DataFrame
        DataFrame с агрегированными признаками
    """
    features = []
    
    # Group by game_id and nickname
    for (game_id, nickname), group in turns_df.groupby(['game_id', 'nickname']):
        feature_dict = {
            'game_id': game_id,
            'nickname': nickname,
            'num_turns': len(group),
            'avg_points_per_turn': group['points'].mean(),
            'total_points': group['points'].sum(),
            'max_points_single_turn': group['points'].max(),
            'min_points_single_turn': group['points'].min(),
            'std_points': group['points'].std(),
            'final_score': group['score'].iloc[-1] if len(group) > 0 else 0,
            'num_plays': (group['turn_type'] == 'Play').sum(),
            'num_exchanges': (group['turn_type'] == 'Exchange').sum(),
            'num_passes': (group['turn_type'] == 'Pass').sum(),
            'avg_rack_length': group['rack'].str.len().mean() if 'rack' in group.columns else 0,
        }
        features.append(feature_dict)
    
    return pd.DataFrame(features)


def create_additional_features(
    df: pd.DataFrame,
    games_df: pd.DataFrame,
    turns_features: pd.DataFrame
) -> pd.DataFrame:
    """
    Создает дополнительные признаки для улучшения качества модели.
    
    Parameters
    ----------
    df : pd.DataFrame
        Основной DataFrame
    games_df : pd.DataFrame
        DataFrame с метаданными игр
    turns_features : pd.DataFrame
        DataFrame с агрегированными признаками ходов
        
    Returns
    -------
    pd.DataFrame
        DataFrame с дополнительными признаками
    """
    df = df.copy()
    
    # Merge games data
    if 'game_id' in df.columns:
        df = df.merge(games_df, on='game_id', how='left', suffixes=('', '_game'))
    
    # Merge turns features
    if 'game_id' in df.columns and 'nickname' in df.columns:
        df = df.merge(turns_features, on=['game_id', 'nickname'], how='left', suffixes=('', '_turns'))
    
    # Create time-based features if datetime exists
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        df['hour'] = df['created_at'].dt.hour
        df['day_of_week'] = df['created_at'].dt.dayofweek
        df['month'] = df['created_at'].dt.month
    
    # Create interaction features
    if 'score' in df.columns and 'final_score' in df.columns:
        df['score_diff'] = df['score'] - df['final_score']
    
    # Create ratio features
    if 'num_plays' in df.columns and 'num_turns' in df.columns:
        df['play_ratio'] = df['num_plays'] / (df['num_turns'] + 1)
    
    if 'total_points' in df.columns and 'num_turns' in df.columns:
        df['points_per_turn'] = df['total_points'] / (df['num_turns'] + 1)
    
    return df


def classify_features(df: pd.DataFrame, target_col: str = 'rating') -> Dict[str, List[str]]:
    """
    Классифицирует признаки по типам с учетом кардинальности и смысла признака.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame с данными
    target_col : str
        Название целевой переменной
        
    Returns
    -------
    dict
        Словарь с классификацией признаков
    """
    numeric_features = []
    categorical_features = []
    datetime_features = []
    id_features = []  # ID-подобные признаки (исключаются из моделирования)
    temporal_features = []  # Временные признаки (hour, day_of_week, month)
    
    for col in df.columns:
        if col == target_col:
            continue
        
        # Проверяем на ID-подобные признаки (исключаем из моделирования)
        if 'id' in col.lower() or col.lower().endswith('_id'):
            id_features.append(col)
            continue
        
        # Проверяем на временные признаки (созданные из datetime)
        if col in ['hour', 'day_of_week', 'month', 'day', 'year', 'week']:
            temporal_features.append(col)
            categorical_features.append(col)  # Временные признаки - категориальные
            continue
        
        if df[col].dtype in ['int64', 'float64']:
            # Проверяем кардинальность для int признаков
            unique_count = df[col].nunique()
            total_count = len(df[col].dropna())
            
            # Если уникальных значений мало относительно общего количества - категориальный
            # Порог: менее 20 уникальных значений И менее 10% от общего количества
            if unique_count < 20 and total_count > 0 and unique_count / total_count < 0.1:
                categorical_features.append(col)
            else:
                numeric_features.append(col)
        elif df[col].dtype == 'object':
            # Check if it's datetime
            if 'date' in col.lower() or 'time' in col.lower():
                datetime_features.append(col)
            else:
                categorical_features.append(col)
        elif 'datetime' in str(df[col].dtype):
            datetime_features.append(col)
    
    return {
        'numeric': numeric_features,
        'categorical': categorical_features,
        'datetime': datetime_features,
        'id': id_features,  # Исключаем из моделирования
        'temporal': temporal_features  # Временные признаки (категориальные)
    }


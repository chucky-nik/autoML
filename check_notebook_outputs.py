#!/usr/bin/env python3
"""
Скрипт для проверки наличия outputs в ноутбуке
"""
import json
from pathlib import Path

notebook_path = Path(__file__).parent / "notebooks" / "scrabble_rating_solution.ipynb"

with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

cells_without_outputs = []
cells_with_outputs = []
critical_cells = []

for idx, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'code':
        has_outputs = len(cell.get('outputs', [])) > 0
        execution_count = cell.get('execution_count')
        
        # Проверяем, является ли ячейка критичной
        source = ''.join(cell.get('source', []))
        is_critical = any(keyword in source.lower() for keyword in [
            'pipeline', 'rmse', 'mae', 'r2', 'lama', 'automl', 
            'сравнение', 'выводы', 'результаты', 'model', 'predict'
        ])
        
        if is_critical:
            critical_cells.append({
                'index': idx,
                'has_outputs': has_outputs,
                'execution_count': execution_count,
                'preview': source[:100].replace('\n', ' ')
            })
        
        if not has_outputs and execution_count is not None:
            cells_without_outputs.append({
                'index': idx,
                'execution_count': execution_count,
                'preview': source[:100].replace('\n', ' ')
            })
        elif has_outputs:
            cells_with_outputs.append(idx)

print("=" * 80)
print("ПРОВЕРКА НАЛИЧИЯ OUTPUTS В НОУТБУКЕ")
print("=" * 80)

print(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
print(f"   Всего code ячеек: {len([c for c in notebook['cells'] if c['cell_type'] == 'code'])}")
print(f"   Ячеек с outputs: {len(cells_with_outputs)}")
print(f"   Ячеек без outputs (но с execution_count): {len(cells_without_outputs)}")
print(f"   Критичных ячеек: {len(critical_cells)}")

print(f"\n⚠️  КРИТИЧНЫЕ ЯЧЕЙКИ БЕЗ OUTPUTS:")
critical_without_outputs = [c for c in critical_cells if not c['has_outputs']]
if critical_without_outputs:
    for cell in critical_without_outputs:
        print(f"   Ячейка {cell['index']}: execution_count={cell['execution_count']}")
        print(f"      {cell['preview']}...")
else:
    print("   ✅ Все критичные ячейки имеют outputs!")

print(f"\n✅ КРИТИЧНЫЕ ЯЧЕЙКИ С OUTPUTS:")
critical_with_outputs = [c for c in critical_cells if c['has_outputs']]
for cell in critical_with_outputs[:10]:  # Показываем первые 10
    print(f"   Ячейка {cell['index']}: execution_count={cell['execution_count']}")

if len(critical_with_outputs) > 10:
    print(f"   ... и еще {len(critical_with_outputs) - 10} ячеек")

print(f"\n📝 ЯЧЕЙКИ БЕЗ OUTPUTS (но с execution_count):")
if cells_without_outputs:
    for cell in cells_without_outputs:
        print(f"   Ячейка {cell['index']}: execution_count={cell['execution_count']}")
        print(f"      {cell['preview']}...")
else:
    print("   ✅ Все выполненные ячейки имеют outputs!")

print("\n" + "=" * 80)
if critical_without_outputs:
    print("❌ ОБНАРУЖЕНЫ ПРОБЛЕМЫ: некоторые критичные ячейки не имеют outputs!")
    print("   Рекомендуется перезапустить ноутбук и сохранить все outputs.")
else:
    print("✅ ВСЕ КРИТИЧНЫЕ ЯЧЕЙКИ ИМЕЮТ OUTPUTS!")
print("=" * 80)

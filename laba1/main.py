import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor as Pool

def generate_csv_file():
    for file_num in range(5):
        random_values = np.random.rand(100) * 100
        categories = np.random.choice(['A', 'B', 'C', 'D'], size=100)
        values = random_values
        
        data_frame = pd.DataFrame({
            'Категория': categories,
            'Значение': values
        })
        
        filename = f'data_{file_num}.csv'
        data_frame.to_csv(filename, index=False)

def process_single_file(filename):
    data_frame = pd.read_csv(filename)
    
    result = data_frame.groupby('Категория')['Значение'].agg(['median', 'std']).reset_index()
    
    return result

def process_files_parallel():
    files = [f'data_{i}.csv' for i in range(5)]
    
    with Pool() as executor:
        results = list(executor.map(process_single_file, files))
    
    return results

def calculate_final_statistics(results):
    
    all_results = pd.concat(results, ignore_index=True)
    final_stats = all_results.groupby('Категория')['median'].agg([
        ('медиана_медиан', 'median'),
        ('стандартное_отклонение_медиан', 'std')
    ]).reset_index()
    
    return final_stats

def main():
    generate_csv_file()
    processing_results = process_files_parallel()
    
    for i, result in enumerate(processing_results):
        print(f"\Файл data_{i}.csv:")
        print(result.to_string(index=False))
    
    final_stats = calculate_final_statistics(processing_results)
  
    print(final_stats.to_string(index=False))
    

if __name__ == '__main__':
    main()
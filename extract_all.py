import os
import re
import csv
import glob

def parse_report(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Regex para encontrar a linha "|Total | 0 | 0 | 0 | 43 | 0|"
    match = re.search(r'\|Total\s*\|\s*\d+\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|', content)
    if match:
        return {
            'DSP': match.group(1),
            'FF': match.group(2),
            'LUT': match.group(3)
        }
    return None

def main():
    report_files = glob.glob('build/**/*.rpt', recursive=True)
    report_files = [f for f in report_files if f.endswith('_csynth.rpt') and not os.path.basename(f) == 'csynth.rpt']
    
    if not report_files:
        print("Nenhum relatório de síntese (*_csynth.rpt) encontrado no diretório build/")
        return

    csv_filename = 'metrics_all.csv'
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Multiplier', 'LUT', 'FF', 'DSP'])
        
        for rpt in report_files:
            metrics = parse_report(rpt)
            if metrics:
                basename = os.path.basename(rpt).replace('_csynth.rpt', '')
                writer.writerow([basename, metrics['LUT'], metrics['FF'], metrics['DSP']])
                print(f"Extraído {basename}: LUT={metrics['LUT']}, FF={metrics['FF']}, DSP={metrics['DSP']}")
            else:
                print(f"Não foi possível parsear métricas em {rpt}")
                
    print(f"\nTodas as métricas salvas em {csv_filename}")

if __name__ == '__main__':
    main()


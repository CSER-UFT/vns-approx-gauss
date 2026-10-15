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

def get_threshold(filepath):
    """Extrai o threshold do nome da pasta da solução (vns_solution_<threshold>)."""
    prefix = 'vns_solution_'
    for part in os.path.normpath(filepath).split(os.sep):
        if part.startswith(prefix):
            return part[len(prefix):]
    # Fallback: pasta da solução = 3 níveis acima do .rpt (<solucao>/syn/report/arquivo.rpt)
    return os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(filepath))))

def sort_key(threshold):
    # baseline primeiro, depois T<número> em ordem numérica, depois o resto
    if threshold == 'baseline':
        return (0, 0, threshold)
    m = re.fullmatch(r'T(\d+)', threshold)
    if m:
        return (1, -int(m.group(1)), threshold)
    return (2, 0, threshold)

def main():
    report_files = glob.glob('build/**/*.rpt', recursive=True)
    report_files = [f for f in report_files if f.endswith('gaussian_csynth.rpt')]
    
    if not report_files:
        print("Nenhum relatório de síntese (gaussian_csynth.rpt) encontrado no diretório build/")
        return

    report_files.sort(key=lambda f: sort_key(get_threshold(f)))

    csv_filename = 'configs_encontradas.csv'
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Threshold', 'LUT', 'FF', 'DSP'])
        
        for rpt in report_files:
            metrics = parse_report(rpt)
            threshold = get_threshold(rpt)
            if metrics:
                writer.writerow([threshold, metrics['LUT'], metrics['FF'], metrics['DSP']])
                print(f"Extraído {threshold}: LUT={metrics['LUT']}, FF={metrics['FF']}, DSP={metrics['DSP']}")
            else:
                print(f"Não foi possível parsear métricas em {rpt}")
                
    print(f"\nTodas as métricas salvas em {csv_filename}")

if __name__ == '__main__':
    main()
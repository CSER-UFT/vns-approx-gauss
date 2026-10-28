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
    """Extrai o identificador/threshold do nome da pasta da solução."""
    # A pasta da solução está 3 níveis acima do arquivo: <solucao>/syn/report/gaussian_csynth.rpt
    sol_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(filepath))))
    prefix = 'vns_solution_'
    if sol_name.startswith(prefix):
        return sol_name[len(prefix):]
    return sol_name

def sort_key(threshold):
    # baseline primeiro no grupo, depois T<número> em ordem numérica decrescente, depois o resto
    m = re.match(r'^(?:(.*?)_)?(baseline|T\d+)$', threshold)
    if m:
        prefix = m.group(1) or ''
        tag = m.group(2)
        if tag == 'baseline':
            return (prefix, 0, 0)
        t_num = int(tag[1:])
        return (prefix, 1, -t_num)
    return (threshold, 2, 0)

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
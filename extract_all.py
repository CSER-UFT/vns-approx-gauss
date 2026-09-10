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

def get_csim_results():
    results = {}
    log_files = glob.glob('build/**/*.log', recursive=True)
    for log in log_files:
        if log.endswith('_csim.log'):
            basename = os.path.basename(log).replace('_csim.log', '')
            with open(log, 'r') as f:
                content = f.read()
                match = re.search(r'Resultado = (\d+)', content)
                if match:
                    results[basename] = float(match.group(1))
    return results

def main():
    report_files = glob.glob('build/**/*.rpt', recursive=True)
    report_files = [f for f in report_files if f.endswith('_csynth.rpt') and not os.path.basename(f) == 'csynth.rpt']
    
    if not report_files:
        print("Nenhum relatório de síntese (*_csynth.rpt) encontrado no diretório build/")
        return
        
    csim_results = get_csim_results()
    
    # Encontra o baseline (multExato)
    baseline = 65025.0
    for name, res in csim_results.items():
        if 'exato' in name.lower() or 'exact' in name.lower():
            baseline = res
            break

    csv_filename = 'metrics_all.csv'
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Multiplier', 'LUT', 'FF', 'DSP', 'resultError (%)'])
        
        for rpt in report_files:
            metrics = parse_report(rpt)
            if metrics:
                basename = os.path.basename(rpt).replace('_csynth.rpt', '')
                
                # Match com os resultados do csim
                matched_res = None
                clean_rpt = re.sub(r'^p?_', '', basename)
                for csim_name, res in csim_results.items():
                    clean_csim = re.sub(r'^p?_', '', csim_name)
                    if clean_rpt == clean_csim:
                        matched_res = res
                        break
                
                if matched_res is not None:
                    error = abs(baseline - matched_res) / baseline * 100.0
                    error_str = f"{error:.4f}"
                else:
                    error_str = "N/A"
                    
                writer.writerow([basename, metrics['LUT'], metrics['FF'], metrics['DSP'], error_str])
                print(f"Extraído {basename}: LUT={metrics['LUT']}, FF={metrics['FF']}, DSP={metrics['DSP']}, Error={error_str}%")
            else:
                print(f"Não foi possível parsear métricas em {rpt}")
                
    print(f"\nTodas as métricas salvas em {csv_filename}")

if __name__ == '__main__':
    main()


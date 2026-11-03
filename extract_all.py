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

def parse_solution_name(filepath):
    """Extrai threshold, opt_agg e patience do nome da pasta da solução.
    Exemplo de nome: vns3Media0_T95
    - kernel size: 3 (já extraído separadamente)
    - opt_agg: Media (média), Geom (média geométrica) ou Med (mediana)
    - patience: número inteiro (0, 230, 350)
    - threshold: número após 'T' (ex.: 95)
    """
    # A pasta da solução está 3 níveis acima do arquivo: <solucao>/syn/report/gaussian_csynth.rpt
    sol_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(filepath))))
    # Pattern matches e.g., vns3Media0_T95 or vns5Geom230_T80
    m = re.match(r"vns(?P<k>\d)(?P<agg>Media|GeoMean|Mediana)(?P<patience>\d+)_T(?P<threshold>\d+)", sol_name)
    if not m:
        # Fallback: try generic extraction of threshold after 'T'
        thresh_match = re.search(r"_T(?P<threshold>\d+)", sol_name)
        threshold = thresh_match.group('threshold') if thresh_match else ''
        return {'threshold': threshold, 'opt_agg': '', 'patience': ''}
    agg_map = {'Media': 'media', 'GeoMean': 'geomean', 'Mediana': 'mediana'}
    return {
        'threshold': m.group('threshold'),
        'opt_agg': agg_map.get(m.group('agg'), m.group('agg').lower()),
        'patience': m.group('patience')
    }


def get_kernel_size(filepath):
    """Identifica o tamanho do kernel (3 ou 5) a partir do caminho ou do relatório."""
    path_lower = filepath.lower()
    sol_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(filepath)))).lower()
    proj_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(filepath))))).lower()

    # 1. Verifica pelo nome da solução ou do projeto
    if 'vns3' in sol_name or '3x3' in sol_name or '3x3' in proj_name or 'hls_proj_3' in path_lower:
        return 3
    if 'vns5' in sol_name or '5x5' in sol_name or '5x5' in proj_name or 'hls_proj_5' in path_lower:
        return 5

    # 2. Verifica a largura da FIFO window_stream no gaussian_csynth.rpt
    # 5x5 usa 25 pixels * 8 bits = 200 bits (w200_d2_S)
    # 3x3 usa 9 pixels * 8 bits = 72 bits (w72_d2_S)
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        if 'w200' in content or '200-bits' in content:
            return 5
        if 'w72' in content or '72-bits' in content:
            return 3
    except Exception:
        pass

    # 3. Verifica o relatório de Window2D_csynth.rpt no mesmo diretório
    win_rpt = os.path.join(os.path.dirname(filepath), 'Window2D_csynth.rpt')
    if os.path.exists(win_rpt):
        try:
            with open(win_rpt, 'r') as f:
                win_content = f.read()
            if '200' in win_content and 'window_stream' in win_content:
                return 5
            if '72' in win_content and 'window_stream' in win_content:
                return 3
        except Exception:
            pass

    return 5

def sort_key(item):
    threshold, k_size = item
    m = re.match(r'^(?:(.*?)_)?(baseline|T\d+)$', threshold)
    if m:
        prefix = m.group(1) or ''
        tag = m.group(2)
        if tag == 'baseline':
            return (k_size, prefix, 0, 0)
        t_num = int(tag[1:])
        return (k_size, prefix, 1, -t_num)
    return (k_size, threshold, 2, 0)

def main():
    report_files = glob.glob('build/**/*.rpt', recursive=True)
    report_files = [f for f in report_files if f.endswith('gaussian_csynth.rpt')]
    
    if not report_files:
        print("Nenhum relatório de síntese (gaussian_csynth.rpt) encontrado no diretório build/")
        return

    # Mapeia cada arquivo para seus dados
    parsed_entries = []
    for rpt in report_files:
        metrics = parse_report(rpt)
        if metrics:
            sol_info = parse_solution_name(rpt)
            # Detect baseline solutions and adjust fields accordingly
            sol_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(rpt))))
            if 'baseline' in sol_name.lower():
                sol_info['threshold'] = 'baseline'
                sol_info['opt_agg'] = '---'
                sol_info['patience'] = '---'
            k_size = get_kernel_size(rpt)
            parsed_entries.append({
                'threshold': sol_info.get('threshold', ''),
                'opt_agg': sol_info.get('opt_agg', ''),
                'patience': sol_info.get('patience', ''),
                'k_size': k_size,
                'metrics': metrics,
                'path': rpt
            })
        else:
            print(f"Não foi possível parsear métricas em {rpt}")

    # Ordena por k_size e threshold
    parsed_entries.sort(key=lambda e: sort_key((e['threshold'], e['k_size'])))

    csv_filename = 'configs_encontradas.csv'
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['threshold', 'k_size', 'opt_agg', 'patience', 'LUT', 'FF', 'DSP'])
        
        for entry in parsed_entries:
            threshold = entry['threshold']
            k_size = entry['k_size']
            opt_agg = entry.get('opt_agg', '')
            patience = entry.get('patience', '')
            metrics = entry['metrics']
            writer.writerow([threshold, k_size, opt_agg, patience, metrics['LUT'], metrics['FF'], metrics['DSP']])
            print(f"Extraído {threshold} (k={k_size}, agg={opt_agg}, patience={patience}): LUT={metrics['LUT']}, FF={metrics['FF']}, DSP={metrics['DSP']}")
                
    print(f"\nTodas as métricas salvas em {csv_filename}")

if __name__ == '__main__':
    main()
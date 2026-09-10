cd build
open_project -reset hls_proj

# Define o nome do top level para uso no relatório
set my_top_level "bit1Truncated"
set_top $my_top_level

add_files ../src/bit1Truncated.cpp
add_files -tb ../tb/tb_bit1Truncated.cpp -cflags "-I../src"

open_solution "solution"
set_part xc7s50csga324-1
create_clock -period 10

# Simulação C
csim_design

# Síntese HLS
csynth_design

# Co-simulação RTL
cosim_design

# Exportação para Vivado
export_design -format ip_catalog

exit
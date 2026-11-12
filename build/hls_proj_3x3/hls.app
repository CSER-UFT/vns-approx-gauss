<AutoPilot:project xmlns:AutoPilot="com.autoesl.autopilot.project" projectType="C/C++" name="hls_proj_3x3" top="gaussian">
    <Simulation argv="">
        <SimFlow name="csim" setup="false" optimizeCompile="false" clean="false" ldflags="" mflags=""/>
    </Simulation>
    <files>
        <file name="../../../tb/tb_gaussian_3x3.cpp" sc="0" tb="1" cflags=" -I../../..  -I../../../src -Wno-unknown-pragmas" csimflags=" -Wno-unknown-pragmas" blackbox="false"/>
        <file name="../src/4bitTruncated.cpp" sc="0" tb="false" cflags="" csimflags="" blackbox="false"/>
        <file name="../vns_mapping_3x3.h" sc="0" tb="false" cflags="" csimflags="" blackbox="false"/>
        <file name="../gaussian_vns_3x3.cpp" sc="0" tb="false" cflags="-I.. -I../src" csimflags="" blackbox="false"/>
        <file name="../src/bit3Truncated.cpp" sc="0" tb="false" cflags="" csimflags="" blackbox="false"/>
        <file name="../src/2bitTruncated.cpp" sc="0" tb="false" cflags="" csimflags="" blackbox="false"/>
        <file name="../src/bit4Truncated.cpp" sc="0" tb="false" cflags="" csimflags="" blackbox="false"/>
        <file name="../src/bit2Truncated.cpp" sc="0" tb="false" cflags="" csimflags="" blackbox="false"/>
    </files>
    <solutions>
        <solution name="vns3Media0_T95" status=""/>
        <solution name="vns3GeoMean0_T70" status=""/>
        <solution name="vns3GeoMean0_T75" status=""/>
        <solution name="vns3GeoMean0_T80" status=""/>
        <solution name="vns3GeoMean0_T85" status=""/>
        <solution name="vns3GeoMean0_T90" status=""/>
        <solution name="vns3GeoMean0_T95" status=""/>
        <solution name="vns3GeoMean230_T70" status=""/>
        <solution name="vns3GeoMean230_T75" status=""/>
        <solution name="vns3GeoMean230_T80" status=""/>
        <solution name="vns3GeoMean230_T85" status=""/>
        <solution name="vns3GeoMean230_T90" status=""/>
        <solution name="vns3GeoMean230_T95" status=""/>
        <solution name="vns3GeoMean350_T70" status=""/>
        <solution name="vns3GeoMean350_T75" status=""/>
        <solution name="vns3GeoMean350_T80" status=""/>
        <solution name="vns3GeoMean350_T85" status=""/>
        <solution name="vns3GeoMean350_T90" status=""/>
        <solution name="vns3GeoMean350_T95" status=""/>
        <solution name="vns3Media0_T70" status=""/>
        <solution name="vns3Media0_T75" status=""/>
        <solution name="vns3Media0_T80" status=""/>
        <solution name="vns3Media0_T85" status=""/>
        <solution name="vns3Media0_T90" status=""/>
        <solution name="vns3Mediana230_T70" status=""/>
        <solution name="vns3Mediana230_T75" status=""/>
        <solution name="vns3Mediana230_T80" status=""/>
        <solution name="vns3Mediana230_T85" status=""/>
        <solution name="vns3Mediana230_T90" status=""/>
        <solution name="vns3Mediana230_T95" status=""/>
        <solution name="vns3Media230_T70" status=""/>
        <solution name="vns3Media230_T75" status=""/>
        <solution name="vns3Media230_T80" status=""/>
        <solution name="vns3Media230_T85" status=""/>
        <solution name="vns3Media230_T90" status=""/>
        <solution name="vns3Media230_T95" status=""/>
        <solution name="vns3Media350_T70" status=""/>
        <solution name="vns3Media350_T75" status=""/>
        <solution name="vns3Media350_T80" status=""/>
        <solution name="vns3Media350_T85" status=""/>
        <solution name="vns3Media350_T90" status=""/>
        <solution name="vns3Media350_T95" status=""/>
        <solution name="vns3Mediana0_T70" status=""/>
        <solution name="vns3Mediana0_T75" status=""/>
        <solution name="vns3Mediana0_T80" status=""/>
        <solution name="vns3Mediana0_T85" status=""/>
        <solution name="vns3Mediana0_T90" status=""/>
        <solution name="vns3Mediana0_T95" status=""/>
        <solution name="vns3Mediana350_T70" status=""/>
        <solution name="vns3Mediana350_T75" status=""/>
        <solution name="vns3Mediana350_T80" status=""/>
        <solution name="vns3Mediana350_T85" status=""/>
        <solution name="vns3Mediana350_T90" status=""/>
        <solution name="vns3Mediana350_T95" status=""/>
    </solutions>
</AutoPilot:project>


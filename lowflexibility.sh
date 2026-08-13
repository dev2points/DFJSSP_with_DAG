TO=3600
MO=1400

DATA_DIR=datasets/LowFlexibilityData/AllInstances

RESULTS2_DIR=results/LowFlexibilityResults/2factories
RESULTS3_DIR=results/LowFlexibilityResults/3factories
RESULTS4_DIR=results/LowFlexibilityResults/4factories

mkdir -p $RESULTS2_DIR
mkdir -p $RESULTS3_DIR
mkdir -p $RESULTS4_DIR

./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la01.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la01.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la02.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la02.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la03.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la03.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la04.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la04.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la05.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la05.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la06.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la06.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la07.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la07.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la08.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la08.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la09.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la09.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la10.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la10.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la11.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la11.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la12.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la12.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la13.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la13.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la14.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la14.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la15.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la15.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la16.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la16.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la17.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la17.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la18.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la18.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la19.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la19.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la20.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la20.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la21.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la21.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la22.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la22.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la23.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la23.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la24.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la24.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la25.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la25.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la26.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la26.log    
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la27.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la27.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la28.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la28.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la29.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la29.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la30.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la30.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la31.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la31.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la32.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la32.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la33.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la33.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la34.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la34.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la35.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la35.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la36.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la36.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la37.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la37.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la38.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la38.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la39.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la39.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la40.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la40.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la41.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la41.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la42.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la42.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la43.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la43.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la44.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la44.log    
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la45.fjs --half_transitive 2>&1 | tee $RESULTS2_DIR/la45.log

./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la46.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la46.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la47.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la47.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la48.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la48.log        
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la49.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la49.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la50.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la50.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la51.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la51.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la52.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la52.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la53.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la53.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la54.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la54.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la55.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la55.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la56.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la56.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la57.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la57.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la58.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la58.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la59.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la59.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la60.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la60.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la61.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la61.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la62.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la62.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la63.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la63.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la64.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la64.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la65.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la65.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la66.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la66.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la67.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la67.log    
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la68.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la68.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la69.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la69.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la70.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la70.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la71.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la71.log    
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la72.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la72.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la73.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la73.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la74.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la74.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la75.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la75.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la76.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la76.log        
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la77.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la77.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la78.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la78.log    
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la79.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la79.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la80.fjs --half_transitive 2>&1 | tee $RESULTS3_DIR/la80.log

./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la81.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la81.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la82.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la82.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la83.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la83.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la84.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la84.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la85.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la85.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la86.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la86.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la87.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la87.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la88.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la88.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la89.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la89.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la90.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la90.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la91.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la91.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la92.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la92.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la93.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la93.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la94.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la94.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la95.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la95.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la96.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la96.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la97.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la97.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la98.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la98.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la99.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la99.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la100.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la100.log      
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la101.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la101.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la102.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la102.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la103.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la103.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la104.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la104.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la105.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la105.log  
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la106.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la106.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la107.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la107.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la108.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la108.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la109.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la109.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la110.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la110.log  
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la111.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la111.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la112.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la112.log  
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la113.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la113.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la114.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la114.log
./runlim -r $TO -s $MO python3 main_linear.py --input $DATA_DIR/la115.fjs --half_transitive 2>&1 | tee $RESULTS4_DIR/la115.log


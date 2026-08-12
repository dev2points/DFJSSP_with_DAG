TO=600
MO=14000

NUM_FACTORIES=2

MKDATA_DIR=datasets/brandimarte
LADATA_DIR=datasets/rdata
MKRESULT_DIR=results/test

mkdir -p $MKRESULT_DIR

# ./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK10 --factories $NUM_FACTORIES  2>&1 | tee $MKRESULT_DIR/MK10._defaultlog
# ./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK10 --factories $NUM_FACTORIES  --sb 2>&1 | tee $MKRESULT_DIR/MK10_sb.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK05 --factories $NUM_FACTORIES  --full_transitive 2>&1 | tee $MKRESULT_DIR/MK5_full_transitive.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK05 --factories $NUM_FACTORIES  --sb --full_transitive 2>&1 | tee $MKRESULT_DIR/MK5_sb_full_transitive.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK07 --factories $NUM_FACTORIES  --full_transitive 2>&1 | tee $MKRESULT_DIR/MK7_full_transitive.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK07 --factories $NUM_FACTORIES  --sb --full_transitive 2>&1 | tee $MKRESULT_DIR/MK7_sb_full_transitive.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK08 --factories $NUM_FACTORIES  --full_transitive 2>&1 | tee $MKRESULT_DIR/MK8_full_transitive.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK08 --factories $NUM_FACTORIES  --sb --full_transitive 2>&1 | tee $MKRESULT_DIR/MK8_sb_full_transitive.log

# ./runlim -r $TO -s $MO  python3 -u main.py --input $LADATA_DIR/la11.txt --factories $NUM_FACTORIES  --full_transitive 2>&1 | tee $MKRESULT_DIR/la11_full_transitive.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $LADATA_DIR/la11.txt --factories $NUM_FACTORIES  --sb --full_transitive 2>&1 | tee $MKRESULT_DIR/la11_sb_full_transitive.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $LADATA_DIR/la12.txt --factories $NUM_FACTORIES  --full_transitive 2>&1 | tee $MKRESULT_DIR/la12_full_transitive.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $LADATA_DIR/la12.txt --factories $NUM_FACTORIES  --sb --full_transitive 2>&1 | tee $MKRESULT_DIR/la12_sb_full_transitive.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $LADATA_DIR/la13.txt --factories $NUM_FACTORIES  --full_transitive 2>&1 | tee $MKRESULT_DIR/la13_full_transitive.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $LADATA_DIR/la13.txt --factories $NUM_FACTORIES  --sb --full_transitive 2>&1 | tee $MKRESULT_DIR/la13_sb_full_transitive.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $LADATA_DIR/la14.txt --factories $NUM_FACTORIES  --full_transitive 2>&1 | tee $MKRESULT_DIR/la14_full_transitive.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $LADATA_DIR/la14.txt --factories $NUM_FACTORIES  --sb --full_transitive 2>&1 | tee $MKRESULT_DIR/la14_sb_full_transitive.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $LADATA_DIR/la15.txt --factories $NUM_FACTORIES  --full_transitive 2>&1 | tee $MKRESULT_DIR/la15_full_transitive.log
./runlim -r $TO -s $MO  python3 -u main.py --input $LADATA_DIR/la15.txt --factories $NUM_FACTORIES  --sb --full_transitive 2>&1 | tee $MKRESULT_DIR/la15_sb_full_transitive.log
./runlim -r $TO -s $MO  python3 -u main.py --input $LADATA_DIR/mt20.txt --factories $NUM_FACTORIES  --full_transitive 2>&1 | tee $MKRESULT_DIR/mt20_full_transitive.log
./runlim -r $TO -s $MO  python3 -u main.py --input $LADATA_DIR/mt20.txt --factories $NUM_FACTORIES  --sb --full_transitive 2>&1 | tee $MKRESULT_DIR/mt20_sb_full_transitive.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK10 --factories $NUM_FACTORIES  --full_transitive 2>&1 | tee $MKRESULT_DIR/MK10_full_transitive.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK10 --factories $NUM_FACTORIES  --sb --full_transitive 2>&1 | tee $MKRESULT_DIR/MK10_sb_full_transitive.log




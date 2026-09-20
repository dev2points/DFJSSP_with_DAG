TO=1800
MO=14000
NUM_FACTORIES=2

FMJDATA_DIR=datasets/fmj
MKDATA_DIR=datasets/brandimarte
RDATA_DIR=datasets/rdata


FMJRESULT_DIR=results/2factories/fmj
MKRESULT_DIR=results/2factories/brandimarte
RRESULT_DIR=results/2factories/rdata




mkdir -p $FMJRESULT_DIR
mkdir -p $MKRESULT_DIR
mkdir -p $RRESULT_DIR


./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs01 --sb --factories $NUM_FACTORIES  --half_transitive 2>&1 | tee $FMJRESULT_DIR/mfjs01.log
./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs02 --sb --factories $NUM_FACTORIES  --half_transitive 2>&1 | tee $FMJRESULT_DIR/mfjs02.log
./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs03 --sb --factories $NUM_FACTORIES  --half_transitive 2>&1 | tee $FMJRESULT_DIR/mfjs03.log
./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs04 --sb --factories $NUM_FACTORIES  --half_transitive 2>&1 | tee $FMJRESULT_DIR/mfjs04.log
./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs05 --sb --factories $NUM_FACTORIES  --half_transitive 2>&1 | tee $FMJRESULT_DIR/mfjs05.log
./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs06 --sb --factories $NUM_FACTORIES  --half_transitive 2>&1 | tee $FMJRESULT_DIR/mfjs06.log
./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs07 --sb --factories $NUM_FACTORIES  --half_transitive 2>&1 | tee $FMJRESULT_DIR/mfjs07.log
./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs08 --sb --factories $NUM_FACTORIES  --half_transitive 2>&1 | tee $FMJRESULT_DIR/mfjs08.log
./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs09 --sb --factories $NUM_FACTORIES  --half_transitive 2>&1 | tee $FMJRESULT_DIR/mfjs09.log
./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs10 --sb --factories $NUM_FACTORIES  --half_transitive 2>&1 | tee $FMJRESULT_DIR/mfjs10.log


./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK01 --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $MKRESULT_DIR/MK01.log
./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK02 --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $MKRESULT_DIR/MK02.log
./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK03 --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $MKRESULT_DIR/MK03.log
./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK04 --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $MKRESULT_DIR/MK04.log
./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK05 --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $MKRESULT_DIR/MK05.log
./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK06 --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $MKRESULT_DIR/MK06.log
./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK07 --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $MKRESULT_DIR/MK07.log
./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK08 --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $MKRESULT_DIR/MK08.log
./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK09 --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $MKRESULT_DIR/MK09.log
./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK10 --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $MKRESULT_DIR/MK10.log



./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la01.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la01.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la02.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la02.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la03.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la03.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la04.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la04.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la05.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la05.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la06.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la06.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la07.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la07.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la08.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la08.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la09.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la09.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la10.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la10.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la11.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la11.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la12.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la12.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la13.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la13.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la14.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la14.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la15.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la15.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la16.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la16.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la17.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la17.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la18.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la18.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la19.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la19.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la20.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/la20.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/mt06.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/mt06.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/mt10.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/mt10.log
./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/mt20.txt --sb --factories $NUM_FACTORIES  --half_transitive  2>&1 | tee $RRESULT_DIR/mt20.log


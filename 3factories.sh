TO=600
MO=8000
NUM_FACTORIES=3

# YDATA_DIR=datasets/yfjs
# DADATA_DIR=Datasets/dafjs
FMJDATA_DIR=datasets/fmj
MKDATA_DIR=datasets/brandimarte
RDATA_DIR=datasets/rdata

# YRESULT_DIR=results/yfjs
# DARESULT_DIR=results/dafjs
# FMJRESULT_DIR=results/3factories/fmj
MKRESULT_DIR=results/3factories/brandimarte
RRESULT_DIR=results/3factories/rdata

mkdir -p $YRESULT_DIR
mkdir -p $DARESULT_DIR
mkdir -p $FMJRESULT_DIR
mkdir -p $MKRESULT_DIR
mkdir -p $RRESULT_DIR

# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS01 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS01.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS02 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS02.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS03 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS03.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS04 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS04.log 
# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS05 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS05.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS06 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS06.log 
# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS07 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS07.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS08 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS08.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS09 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS09.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS10 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS10.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS11 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS11.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS12 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS12.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS13 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS13.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS14 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS14.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS15 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS15.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS16 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS16.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS17 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS17.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS18 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS18.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS19 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS19.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $YDATA_DIR/YFJS20 --factories $NUM_FACTORIES  2>&1 | tee $YRESULT_DIR/YFJS20.log

# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS01 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS01.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS02 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS02.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS03 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS03.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS04 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS04.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS05 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS05.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS06 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS06.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS07 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS07.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS08 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS08.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS09 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS09.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS09 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS09.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS10 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS10.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS11 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS11.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS12 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS12.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS13 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS13.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS14 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS14.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS15 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS15.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS16 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS16.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS17 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS17.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS18 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS18.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS19 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS19.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS20 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS20.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS21 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS21.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS22 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS22.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS23 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS23.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS24 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS24.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS25 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS25.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS26 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS26.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS27 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS27.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS28 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS28.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS29 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS29.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS29 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS29.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $DADATA_DIR/DAFJS30 --factories $NUM_FACTORIES  2>&1 | tee $DARESULT_DIR/DAFJS30.log

# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/sfjs01 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/sfjs01.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/sfjs02 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/sfjs02.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/sfjs03 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/sfjs03.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/sfjs04 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/sfjs04.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/sfjs05 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/sfjs05.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/sfjs06 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/sfjs06.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/sfjs07 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/sfjs07.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/sfjs08 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/sfjs08.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/sfjs09 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/sfjs09.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/sfjs10 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/sfjs10.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs01 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/mfjs01.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs02 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/mfjs02.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs03 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/mfjs03.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs04 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/mfjs04.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs05 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/mfjs05.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs06 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/mfjs06.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs07 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/mfjs07.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs08 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/mfjs08.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs09 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/mfjs09.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $FMJDATA_DIR/mfjs10 --factories $NUM_FACTORIES  2>&1 | tee $FMJRESULT_DIR/mfjs10.log

./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK01 --factories $NUM_FACTORIES  2>&1 | tee $MKRESULT_DIR/MK01.log
./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK02 --factories $NUM_FACTORIES  2>&1 | tee $MKRESULT_DIR/MK02.log
./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK03 --factories $NUM_FACTORIES  2>&1 | tee $MKRESULT_DIR/MK03.log
./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK04 --factories $NUM_FACTORIES  2>&1 | tee $MKRESULT_DIR/MK04.log
./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK05 --factories $NUM_FACTORIES  2>&1 | tee $MKRESULT_DIR/MK05.log
./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK06 --factories $NUM_FACTORIES  2>&1 | tee $MKRESULT_DIR/MK06.log
./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK07 --factories $NUM_FACTORIES  2>&1 | tee $MKRESULT_DIR/MK07.log
./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK08 --factories $NUM_FACTORIES  2>&1 | tee $MKRESULT_DIR/MK08.log
./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK09 --factories $NUM_FACTORIES  2>&1 | tee $MKRESULT_DIR/MK09.log
./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK10 --factories $NUM_FACTORIES  2>&1 | tee $MKRESULT_DIR/MK10.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK11 --factories $NUM_FACTORIES  2>&1 | tee $MKRESULT_DIR/MK11.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK12 --factories $NUM_FACTORIES  2>&1 | tee $MKRESULT_DIR/MK12.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK13 --factories $NUM_FACTORIES  2>&1 | tee $MKRESULT_DIR/MK13.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK14 --factories $NUM_FACTORIES  2>&1 | tee $MKRESULT_DIR/MK14.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $MKDATA_DIR/MK15 --factories $NUM_FACTORIES  2>&1 | tee $MKRESULT_DIR/MK15.log


# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la01.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la01.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la02.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la02.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la03.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la03.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la04.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la04.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la05.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la05.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la06.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la06.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la07.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la07.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la08.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la08.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la09.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la09.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la10.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la10.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la11.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la11.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la12.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la12.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la13.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la13.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la14.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la14.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la15.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la15.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la16.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la16.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la17.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la17.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la18.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la18.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la19.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la19.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/la20.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/la20.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/mt06.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/mt06.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/mt10.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/mt10.log
# ./runlim -r $TO -s $MO  python3 -u main.py --input $RDATA_DIR/mt20.txt --factories $NUM_FACTORIES  2>&1 | tee $RRESULT_DIR/mt20.log
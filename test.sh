TO=3600
MO=14000
NUM_FACTORIES=2

# YDATA_DIR=datasets/yfjs
# DADATA_DIR=Datasets/dafjs
FMJDATA_DIR=datasets/fmj
MKDATA_DIR=datasets/brandimarte
RDATA_DIR=datasets/rdata

# YRESULT_DIR=results/yfjs
# DARESULT_DIR=results/dafjs

FMJRESULT_DIR=results/test/2factories/fmj
MKRESULT_DIR=results/test/2factories/brandimarte
RRESULT_DIR=results/test/2factories/rdata

# mkdir -p $YRESULT_DIR
# mkdir -p $DARESULT_DIR
# mkdir -p $FMJRESULT_DIR
# mkdir -p $MKRESULT_DIR
mkdir -p $RRESULT_DIR

./runlim -r $TO -s $MO  python3 -u test.py --input $RDATA_DIR/la11.txt --sb --full_transitive --factories $NUM_FACTORIES  --solver cadical300 2>&1 | tee $RRESULT_DIR/la11_cadical300.log
./runlim -r $TO -s $MO  python3 -u test.py --input $RDATA_DIR/la11.txt --sb --full_transitive --factories $NUM_FACTORIES  --solver glucose4 2>&1 | tee $RRESULT_DIR/la11_glucose4.log
./runlim -r $TO -s $MO  python3 -u test.py --input $RDATA_DIR/la11.txt --sb --full_transitive --factories $NUM_FACTORIES  --solver maplechrono 2>&1 | tee $RRESULT_DIR/la11_maplechrono.log
./runlim -r $TO -s $MO  python3 -u test.py --input $RDATA_DIR/la11.txt --sb --full_transitive --factories $NUM_FACTORIES  --solver minisat22 2>&1 | tee $RRESULT_DIR/la11_minisat22.log



<<<<<<< HEAD

=======
# ./runlim -r $TO -s $MO python3 -u main.py --factories $NUM_FACTORIES --input $MKDATA_DIR/MK05 --sb --full_transitive 2>&1 | tee $MKRESULT_DIR/MK05.log
# ./runlim -r $TO -s $MO python3 -u main.py --factories $NUM_FACTORIES --input $MKDATA_DIR/MK07 --sb --full_transitive 2>&1 | tee $MKRESULT_DIR/MK07.log
# ./runlim -r $TO -s $MO python3 -u main.py --factories $NUM_FACTORIES --input $MKDATA_DIR/MK10 --sb --full_transitive 2>&1 | tee $MKRESULT_DIR/MK10.log
./runlim -r $TO -s $MO python3 -u main.py --factories $NUM_FACTORIES --input $LADATA_DIR/la13.txt --sb --full_transitive 2>&1 | tee $MKRESULT_DIR/la13.log
>>>>>>> 66068d6 (test transitive u->v and v->l so add u->l)




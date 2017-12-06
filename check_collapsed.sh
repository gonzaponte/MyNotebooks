for i in $@
do
    echo $i ----------------------
    grep collapsed $i
done
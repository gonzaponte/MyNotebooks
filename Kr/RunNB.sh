template=$1
run=$2

NB=${template%.*}_${run}.ipynb
cp ${template} ${NB}
perl -pi -e 's/XXX_RUN_NUMBER_XXX/'"$run"'/g' ${NB}
jupyter nbconvert --ExecutePreprocessor.timeout=None --to notebook --execute ${NB} --output ${NB} --allow-errors

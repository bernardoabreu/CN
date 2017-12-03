
BASE="${HOME}/CN/tp3/source/"
mkdir h
mkdir s
mkdir t

ls | grep history | xargs -i{} mv {} h/
ls | grep score | xargs -i{} mv {} s/
ls | grep history | xargs -i{} mv {} h/
ls | grep time | xargs -i{} mv {} t/

mv s/ score
mv h/ history
mv t/ time

mkdir runs
mv yeast_modified_* runs

for i in {0..2}; do
	$BASE/join.sh "history_${i}_acc" history/
	$BASE/join.sh "history_${i}_loss" history/
	$BASE/join.sh "score_${i}_acc" score/
	$BASE/join.sh "score_${i}_loss" score/
	$BASE/join.sh "time_${i}_time" time/
done

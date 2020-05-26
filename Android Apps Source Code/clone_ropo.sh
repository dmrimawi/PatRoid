allRopos=$(cat MoreThan1400AndroidAppRepo.txt)
for line in $allRopos 
do
	repo=$(echo $line | cut -d# -f1)
	git clone $repo
done

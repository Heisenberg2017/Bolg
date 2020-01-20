# push to bolg

msg="rebuilding site $(date)"
if [ -n "$*" ]; then
	msg="$*"
fi
git commit -m "$msg"
cp -r * ../../OpenStackCode/Heisenberg2017.github.io/

cd ../../OpenStackCode/Heisenberg2017.github.io/

git add .

git commit -m "$msg"

git push origin master

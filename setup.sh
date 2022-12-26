# /bin/bash
echo 'Setup...'
if [[ ! -d "input" ]];
then
    echo "Creating input directory"
    mkdir input
fi
if [[ ! -d "out" ]];
then
    echo "Creating out directory"
    mkdir out
fi
if [[ ! -d "tmp_dir" ]];
then
    echo "Creating tmp_dir directory"
    mkdir tmp_dir
fi

echo 'Place input.mp4 in ./input'
echo 'Done!'
sudo apt-get install -y git cmake libboost-python-dev python-pip python-skimage
git clone https://github.com/davisking/dlib.git
cd dlib/python_examples/
mkdir build
cd build
cmake -D USE_SSE4_INSTRUCTIONS:BOOL=ON ../../tools/python 
cmake --build . --config Release --target install  
cd ..
sudo cp dlib.so /usr/local/lib/python2.7/dist-packages/
cd
sudo pip install django
wget http://johnvansickle.com/ffmpeg/builds/ffmpeg-git-64bit-static.tar.xz
tar -xvf ffmpeg-git-64bit-static.tar.xz
sudo cp ffmpeg-git-20150627-64bit-static/ffmpeg /usr/bin/ffmpeg

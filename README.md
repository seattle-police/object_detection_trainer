# object_detection_trainer
This is a web interface for creating histogram-of-oriented-gradient (HOG) based object detectors.

## Installing
You need Dlib's Python interface. See https://github.com/davisking/dlib/blob/master/python_examples/compile_dlib_python_module.bat and http://stackoverflow.com/questions/30042174/how-to-get-python-import-working-with-dlib-using-cmake-and-osx

You also need Django https://www.djangoproject.com/download/ and FFMPEG https://www.ffmpeg.org/

Get at least one video. Create a folder for putting frames and in object_detection_trainer/settings.py change FRAMES_DIR to the new frames folder. Next run `python helper_scripts/convert_videos_to_frames.py [[ folder with the video(s) to convert to frames ]]`


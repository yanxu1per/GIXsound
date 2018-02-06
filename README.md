# GIXsound
This is the sound localization project

### Ubuntu/Raspberry Pi/Pine64

First `apt-get` install `swig`, `sox`, `portaudio` and its Python binding `pyaudio`:

    sudo apt-get install swig3.0 python-pyaudio python3-pyaudio sox
    pip install pyaudio
    
Then install the `atlas` matrix computing library:

    sudo apt-get install libatlas-base-dev
    
Make sure that you can record audio with your microphone:

    rec t.wav

Pip install required library

    cd GIXsound
    pip install -r requirements.txt 


If you need extra setup on your audio (especially on a Raspberry Pi), please see the [full documentation](http://docs.kitt.ai/snowboy).

Run the demo

	python demo.py Help.pmdl

Redefine callback function to play more
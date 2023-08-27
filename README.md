# tr-imview
Trame app for image viewer

An image viewing (slice view and volume rendering) using [trame](https://kitware.github.io/trame/)


## setup 

```bash
python3.9 -m venv venv
source ./venv/bin/activate
python -m pip install --upgrade pip
pip install --upgrade trame
pip install trame-vuetify trame-vtk # Install widgets that we'll be using
pip install "vtk"
```

## run

```bash
source ./venv/bin/activate
python tr-imview/tr-imview/app.py 
```

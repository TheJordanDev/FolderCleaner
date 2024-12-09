Install dependencies
```shell
python -m pip install -r requirements.txt
```

Build exe
```shell
./build.bat
```

If you have erros when building (e.g. The .exe does not compile)

Try making a virtual env [See example here](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)

```shell
python -m venv env

# Activate the env (env/Scripts/activate)

# Reinstall dependencies
pip install -r requirements.txt

# And rebuild with either the build.bat or the first command inside

```
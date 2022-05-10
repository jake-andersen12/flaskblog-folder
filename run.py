# save this as app.py

from flaskblog import app  #pulls from the __init__.py file. You can see we are defining the app variable on that file.

if __name__ == '__main__':
    app.run(debug=True)
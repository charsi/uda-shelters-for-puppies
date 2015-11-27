from puppyApp import app

if __name__ == '__main__':
    # dummy secret key; required only for message flashing
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

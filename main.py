from website import create_app

app = create_app()

if __name__ == '__main__':#Only run the webserver when you run this file
    app.run(debug=True)# run flask and start a webserver: true is whenever you make a change to python code, auto rerun this code
from flask import Flask, render_template, Response
import io
import random
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#from matplotlib.figure import Figure

app = Flask (__name__)

@app.route ("/")
def first_function ():
    return "<html><body><h1 style='color:red'>Default page !!</h1></body> </html>"

@app.route ("/weather")
def weather_page ():
    temperature, humidity = get_weather ()
    return render_template("index.html", temperature = temperature, humidity = humidity)


def get_weather ():
    # here, we're performing the logic to get data from the sensors or reading it in from the file
    
    temperature = 78
    humidity = 30
    return temperature, humidity

'''
@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig
'''

if __name__== "__main__":
    app.run (host = '0.0.0.0', debug=True)

from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import matplotlib.pyplot as plt
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # получаем файл из запроса
    file = request.files['image']
    # читаем изображение с помощью OpenCV
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # получаем порядок каналов из запроса
    order = request.form['order']
    if order == 'rgb':
        pass
    elif order == 'rbg':
        img[:, :, 1], img[:, :, 2] = img[:, :, 2], img[:, :, 1].copy()
    elif order == 'grb':
        img[:, :, 0], img[:, :, 1] = img[:, :, 1], img[:, :, 0].copy()
    elif order == 'gbr':
        img[:, :, 0], img[:, :, 1], img[:, :, 2] = img[:, :, 1], img[:, :, 2], img[:, :, 0].copy()
    elif order == 'brg':
        img[:, :, 0], img[:, :, 2] = img[:, :, 2], img[:, :, 0].copy()
    elif order == 'bgr':
        img[:, :, 0], img[:, :, 1], img[:, :, 2] = img[:, :, 2], img[:, :, 1], img[:, :, 0].copy()


    # получаем графики распределения цветов
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
    histogram_filename = 'histogram.png'
    plt.savefig(f'static/{histogram_filename}')
    plt.clf()

    # получаем графики среднего значения цвета по вертикали и горизонтали
    mean_vertical = np.mean(img, axis=0)
    plt.plot(mean_vertical)
    mean_vertical_filename = 'mean_vertical.png'
    plt.savefig(f'static/{mean_vertical_filename}')
    plt.clf()

    mean_horizontal = np.mean(img, axis=1)
    plt.plot(mean_horizontal)
    mean_horizontal_filename = 'mean_horizontal.png'
    plt.savefig(f'static/{mean_horizontal_filename}')
    plt.clf()

    # сохраняем измененное изображение
    modified_filename = 'modified.png'
    cv2.imwrite(f'static/{modified_filename}', img)

    # перенаправляем на страницу с результатами и передаем параметры графиков в URL
    return redirect(url_for('results', hist=histogram_filename, vert=mean_vertical_filename, hor=mean_horizontal_filename, mod=modified_filename))

@app.route('/results')
def results():
    # получаем параметры графиков из URL
    hist_filename = request.args.get('hist')
    vert_filename = request.args.get('vert')
    hor_filename = request.args.get('hor')
    mod_filename = request.args.get('mod')
    # отображаем графики на странице
    return render_template('result.html', hist=hist_filename, vert=vert_filename, hor=hor_filename, mod=mod_filename)


if __name__ == '__main__':
    app.run(debug=True)

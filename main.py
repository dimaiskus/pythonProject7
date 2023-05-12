from flask import Flask, render_template, request
import cv2
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Получаем файл изображения из формы
    img = request.files['image'].read()
    # Преобразуем байты в массив numpy
    npimg = np.fromstring(img, np.uint8)
    # Декодируем изображение
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    # Получаем порядок цветовых карт из формы
    order = request.form['order']
    # Меняем порядок цветовых карт
    if order == 'rgb':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    elif order == 'gbr':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    elif order == 'brg':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Вычисляем гистограммы распределения цветов
    colors = ('r', 'g', 'b')
    for i, col in enumerate(colors):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
    plt.savefig('static/histogram.png')
    plt.clf()
    # Вычисляем среднее значение цвета по вертикали и горизонтали
    mean_horizontal = np.mean(img, axis=0)
    mean_vertical = np.mean(img, axis=1)
    plt.plot(mean_horizontal)
    plt.savefig('static/mean_horizontal.png')
    plt.clf()
    plt.plot(mean_vertical)
    plt.savefig('static/mean_vertical.png')
    plt.clf()
    # Возвращаем результаты
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
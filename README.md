# Репозиторий команды "Титаник, который смог" с решением кейса "ИИ на страже популяции ненецких моржей"
Данный репозиторий содержит программный код с реализацией решения кейса "ИИ на страже популяции ненецких моржей" Хакатона "Цифровой Прорыв 2022: Дальневосточный федеральный округ"

## Реализация в виде десктопного приложения: 
Представлен удобный и интуитивно понятный интерфейс десктопного приложения, 
предоставляющий возможность загрузки фотографии или папки с фотографиями моржей. 
После загрузки фотографии (папки с фотографиями) происходит подсчёт числа моржей на основе разработанной нейросетевой модели, обученной на предложенном датасете. 
В случае загрузки папки с фотографиями происходит суммирование числа моржей со всех фотографий. 
При этом используется метод склеивания фотографий с наложением.

В качестве результата предоставляется фотография с указанием красных точек, соответствующих каждому из определенных моделью моржей. 
На основе этих точек подсчитывается и выводится общее число выделенных моделью моржей.

## Уникальность: 
Возможность подсчитать число моржей не только на 1 фотографии, но и на нескольких, расположенных в рамках одной папки, 
а также учет возможных повторяющихся фрагментов среди заданного числа фотографий.

## Стек технологий: 
Yolo v5, Flann matcher, pyQT.
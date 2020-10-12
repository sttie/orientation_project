Этот репозиторий - результат работы в рамках альтернативного экзамена по дискретной математике.

Программа в папке path реализует поиск кратчайшего пути от точки А до точки В на полигональной карте с использованием алгоритмов Дейкстры и А*.

Программа в папке coverage реализует *обход* полигональной карты, реализуя алгоритм под названием "бустрофедон".

## ВНИМАНИЕ!

Программа из coverage сохраняет файл dump.txt, в котором содержится информация о введенных Вами полигонах. Если Вы нашли какой-то баг, то, пожалуйста, отправьте этот файл на почту sttiemath@gmail.com или оставьте его в таблице.


## path

Выполнение программы начинается с draw_map.py. Для запуска необходимо установить pygame (pip install pygame).

При запуске программа находится в режиме редактора полигонов. Нарисовали первый полигон - нажали кнопку Q и перешли к отрисовке следующего полигона (при нажатии кнопки Q полигон автоматически строит ребро между последней и первой точками полигона). Закончили с редактированием полигонов - нажимаем E (англ.) и редактор переходит в режим редактирования начальной точки. Поставили точку, где хотим - нажимаем E и переходим к конечной точке (все то же самое). Закончили с конечной точкой - нажали E и после этого программа начнет вычислять кратчайший путь от начальной до конечной точки.

Если путь не отобразился, то пути между данными точками не существует.

Программа после выдачи результата имеет два режима отрисовки - режим отрисовки графа видимости и режим отрисовки кратчайшего пути (А* или Дейкстра). Режимы переключаются кнопкой Z.

При отображении пути красные вершины - это вершины, посещенные текущим алгоритмом.

Робот аппроксимируется восьмиугольником.

Чтобы завершить программу после отображения пути необходимо нажать Q.


## coverage

Инструкция абсолютно аналогична, за исключением режимов отображений. Нарисовали полигоны, нажали Е, подождали обхода карты и нажали Q для выхода.

# Лабораторная работа №2
Выполнила Жулитова Дарья 22ПИ2

dazhulitova@edu.hse.ru

Выполнено на языке python 3.9

# Алгоритм перебора ([BruteForceAlgorithm](brute_force.py#L1))
Отсуствует подготовка данных. При запросе ответа происходит перебор всех прямоугольников и проверяется лежит ли точка в границах текущего прямоугольника.

```python
def preparation(self, rectangles):
    self.rectangles = rectangles
```
Сложность подготовки O(1)
```python
def query(self, x, y):
    k = 0
    for r in self.rectangles:
        if r.x1 <= x < r.x2 and r.y1 <= y < r.y2:
            k += 1
    return k
```
Сложность поиска O(N)

# Алгоритм на карте ([MapAlgorithm](map.py#L4))
Во время подготовки данных происходит сжатие координат и построение карты сжатых прямоугольников
```python
def preparation(self, rectangles):
    if rectangles:
        self.compressed_x, self.compressed_y = compress(rectangles)
        compressed_dict_x, compressed_dict_y = get_dicts(self.compressed_x, self.compressed_y)
        self.map = [[0] * len(self.compressed_y) for _ in range(len(self.compressed_x))]
        for r in rectangles:
            for x in range(compressed_dict_x[r.x1], compressed_dict_x[r.x2]):
                for y in range(compressed_dict_y[r.y1], compressed_dict_y[r.y2]):
                    self.map[x][y] += 1
```
Сложность подготовки O(N^3)

При запросе ответа сначала находим расположение точки на карте сжатых прямоугольников, а затем получаем ответ из карты по полученным индексам.
```python
def query(self, x, y):
    if self.compressed_x:
        x = search(x, self.compressed_x)
        y = search(y, self.compressed_y)
        if x == -1 or y == -1:
            return 0
        else:
            return self.map[x][y]
    else:
        return 0
```
Сложность поиска O(logN)

# Алгоритм на дереве ([PersistentTreeAlgorithm](persistent_segment_tree.py#L4))
Во время подготовки данных происходит сжатие координат, создание и заполненин персистентного дерева отрезков ([PersistentSegmentTree](persistent_segment_tree.py#L32))
```python
def preparation(self, rectangles):
    if rectangles:
        self.compressed_x, self.compressed_y, = compress(rectangles)
        compressed_dict_x, compressed_dict_y = get_dicts(self.compressed_x, self.compressed_y)
        event_list = []
        for r in rectangles:
            event_list.append(Event(compressed_dict_x[r.x1], compressed_dict_y[r.y1], compressed_dict_y[r.y2], 1))
            event_list.append(Event(compressed_dict_x[r.x2], compressed_dict_y[r.y1], compressed_dict_y[r.y2], -1))
        self.tree = PersistentSegmentTree(sorted(event_list, key=lambda e: e.val), len(self.compressed_y))
```
Сложность подготовки O(NlogN)

При запросе ответа находим расположение точки на карте сжатых прямоугольников и выполняем поиск по персистентному дереву отрезков.
```python
def query(self, x, y):
    if self.compressed_x:
        x = search(x, self.compressed_x)
        y = search(y, self.compressed_y)
        if x == -1 or y == -1 or len(self.tree.nodes) <= x:
            return 0
        else:
            return self.tree.find(x, y)
    else:
        return 0
```
Сложность поиска O(logN)

# Сравнение времени подготовки
На графике видно, что алгоритм на карте выигрывает по времени предварительной обработки данных только для очень небольшого количества прямоугольников, в пределах 20. Это связано с высокой асимптотической сложностью построения карты O(N^3), поскольку программе необходимо пройти по всей матрице карты N*N размеров, что требует значительного времени даже для небольших чисел.
Время построения персистентного дерева отрезков сравнимо со временем построения карты на небольшом количестве прямоугольников. Но даже при малом увеличении количества входных данных подготовка данных в алгоритме на дереве выигрывает в разы у алгоритма на карте. Полный перебор не требует предварительной обработки, поэтому время подготовки практически мгновенное.

![](artefacts/Preparation%20time.png)![](artefacts/Preparation%20time%20(log).png)

# Сравнение времени поиска ответа
На графике видно, что при количестве прямоугольников в пределах 10 алгоритм полного перебора даже выигрывает остальные алгоритмы по времени ответа, но при большем количестве он значительно проигрывает. Время ответа алгоритма на карте стабильно занимает немного меньше времени, так как в нем есть только два бинарных поиска, а в алгоритме на дереве к ним добавляется спуск по дереву.

![](artefacts/Query%20time.png)![](artefacts/Query%20time%20(log).png)

# Вывод
Для большого количесва данных лучше всего себя показал алгоритм на персистентном дереве отрезков, но он сложен в реализации. Для малого количества прямоугольников и большого числа запросов лучше использовать алгоритм на карте. Если данные очень малы и нужна очень быстрая реализация то подойдёт обычный перебор.

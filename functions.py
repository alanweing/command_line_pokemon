import _print


def die(message=None):
    if message is not None:
        _print.warning(str(message))
    exit(0)


def _sort(_list, sort_order='crescent', sort_method='selection_sort'):
    if sort_method == 'selection_sort':
        _list = selection_sort(_list)
    elif sort_method == 'insertion_sort':
        _list = insertion_sort(_list)
    elif sort_method == 'merge_sort':
        _list = merge_sort(_list)
    elif sort_method == 'quick_sort':
        _list = quick_sort(_list)
    if sort_order == 'decrescent':
        _list.reverse()
    return _list


def selection_sort(_list):
    for i in range(0, len(_list)):
        _min = {
            'pos': i,
            'value': _list[i]
        }
        for z in range(i, len(_list)):
            if _list[z] < _min['value']:
                _min = {
                    'pos': z,
                    'value': _list[z]
                }
        aux = _list[i]
        _list[i] = _min['value']
        _list[_min['pos']] = aux
    return _list


def insertion_sort(_list):
    for i in range(0, len(_list)):
        value_to_insert = _list[i]
        index = i
        while index > 0 and _list[index - 1] > value_to_insert:
            _list[index] = _list[index - 1]
            index -= 1
        _list[index] = value_to_insert
    return _list


def merge_sort(_list):
    if len(_list) == 1:
        return _list
    left_half = _list[:(len(_list)//2)]
    right_half = _list[(len(_list)//2):]
    merge_sort(left_half)
    merge_sort(right_half)
    i = z = x = 0
    while i < len(left_half) and z < len(right_half):
        if left_half[i] < right_half[z]:
            _list[x] = left_half[i]
            i += 1
        else:
            _list[x] = right_half[z]
            z += 1
        x += 1
    while i < len(left_half):
        _list[x] = left_half[i]
        i += 1
        x += 1
    while z < len(right_half):
        _list[x] = right_half[z]
        z += 1
        x += 1
    return _list


def quick_sort(_list):
    less = []
    equal = []
    greater = []
    if len(_list) > 1:
        pivot = _list[0]
        for value in _list:
            if value < pivot:
                less.append(value)
            if value == pivot:
                equal.append(value)
            if value > pivot:
                greater.append(value)
        return quick_sort(less) + equal + quick_sort(greater)
    else:
        return _list


# def get_vio(_list):
#     vio = []
#     for i in range(0, len(_list)):
#         if len(vio) != 0:
#             _min = {'pos': vio[-1], 'value': _list[vio[-1]]}
#         else:
#             _min = {'pos': 0, 'value': _list[0]}
#         jump = _min['pos']
#         for j in range(0, len(_list)):
#             if j not in vio:
#                 if len(vio) != 0 and _list[j] > _list[vio[-1]]:
#                     if
#                     _min = {'pos': j, 'value': _list[j]}
#                 elif len(vio) == 0 and _list[j] < _min['value']:
#                     _min = {'pos': j, 'value': _list[j]}
#         print(_min)
#         vio.append(_min['pos'])
#     return vio

def get_vio(_list):
    vio = []
    for i in range(0, len(_list)):
        _min = {'pos': 0, 'value': _list[0]}
        for j in range(0, len(_list)):
            if j not in vio:
                if (len(vio) == 0 and _list[j] < _min['value']) or \
                        (len(vio) != 0 and _list[j] > _list[vio[-1]] and
                            _list[j] < _min['value']):
                    _min = {'pos': j, 'value': _list[j]}
                    # print('min:', _min, '\nvio:', vio)
        print(_min)
        vio.append(_min['pos'])
    return vio

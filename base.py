
def get_coords_base(units):
    our_base = units["base"]
    return list(map(lambda t: [t['x'], t['y']], our_base))

def where_can_build_base_using_our_base(units, world):
    coords_our_base = get_coords_base(units)
    # TODO дописать

def where_can_build_base(units, world):
    coords_our_base = get_coords_base(units)
    # TODO дописать




def build_bases(x_lst,y_lst):
    """
    Строит базы в координатах списков x_lst, y_lst
    """

    lst = []
    for x,y in zip(x_lst, y_lst):
        lst.append(build_base(x,y))
    return {'build' : lst}


def build_base(x,y):
    return {'x': 79, 'y': 59}




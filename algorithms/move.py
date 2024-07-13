def check_base(units, move):
    our_base = units.get("base", []) or []
    for cell in our_base:
        if move["x"] == cell["x"] and move["y"] == cell["y"]:
            return True
    return False

def move(units, world, head):
    zpots = world.get("zpots", []) or []
    dx = 0
    dy = 0
    for zpot in zpots:
        if zpot["type"] == "default":
            dx_curr = head["x"] - zpot["x"]
            dy_curr = head["y"] - zpot["y"]
            dx += dx_curr
            dy += dy_curr


    if abs(dy) - abs(dx) > 0:
        if dy > 0:
            move = {"x": head["x"], "y": head["y"] + 1}
            if check_base(units, move):
                return move
            else:
                if dx > 0:
                    move["x"] += 1
                else:
                    move["x"] -= 1
                if check_base(units, move):
                    return move
                else:
                    return None
        else:
            move = {"x": head["x"], "y": head["y"] - 1}
            if check_base(units, move):
                return move
            else:
                if dx > 0:
                    move["x"] += 1
                else:
                    move["x"] -= 1
                if check_base(units, move):
                    return move
                else:
                    return None
    else:
        if dx > 0:
            move = {"x": head["x"] + 1, "y": head["y"]}
            if check_base(units, move):
                return move
            else:
                if dy > 0:
                    move["y"] += 1
                else:
                    move["y"] -= 1
                if check_base(units, move):
                    return move
                else:
                    return None
        else:
            move = {"x": head["x"] - 1, "y": head["y"]}
            if check_base(units, move):
                return move
            else:
                if dy > 0:
                    move["y"] += 1
                else:
                    move["y"] -= 1
                if check_base(units, move):
                    return move
                else:
                    return None

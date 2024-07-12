import json

def base():
    """Алгоритм построения базы."""

    return 1


class Base:
    def __init__(self, priority_building_file='dens5.txt') -> None:
        self._priority_building_file = priority_building_file
        self._curr_len_of_priority = 10


    def update(self, units, world, head):
        return self.update_with_pattern(units, world, head)

    def update_with_pattern(self, units, world, head):
        """
        Строит по возможности клетки баз, проходясь по 
        списку priority_building

        head - координаты головы
        """

        # Вычисляем кол-во золота
        gold = units['player']['gold']
        if gold == 0:
            return []

        # Что может помешать
        our_base = units.get("base", []) or []
        zombies = units.get("zombies", []) or []
        anPlayerBases = units.get("enemyBlocks", []) or []
        zposts = world.get("zpots", []) or []

        # Список для постройки
        to_build = []

        # Подгрузить список приоритета
        with open("build_patterns\\" + self._priority_building_file) as f:
            priority_building = json.load(f)

        for i, next_coords in enumerate(priority_building):

            x = head['x'] + next_coords[0]
            y = head['y'] + next_coords[0]

            # Если здесь наша база
            for base in our_base:
                if x == base['x'] and y == base['y']:
                    continue

                

            # Если зомби
            for zombie in zombies:
                if x == zombie['x'] and y == zombie['y']:
                    continue

            # Если клетка базы игрока
            for anPlayerBase in anPlayerBases:
                if x >= anPlayerBase['x'] - 1 and x <= anPlayerBase['x'] + 1 and \
                        y >= anPlayerBase['y'] - 1 and y <= anPlayerBase['y'] + 1:
                    continue

            # Блок базы нельзя ставить вплотную к клетке спота зомби
            for zpost in zposts:
                distance = abs(zpost['x'] - x) + abs(zpost['y'] - y)
                if distance <= 1:
                    continue    

            # Строим здесь
            to_build.append({'x': x, 'y': y})
            gold -= 1

            # Если золота нет
            if gold == 0:
                break

        return to_build
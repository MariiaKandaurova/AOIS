from var import *


class KMap:
    def __init__(self, table, vars):
        self.vars = vars
        var_len = len(vars)

        if var_len <= 1 or var_len > 4:
            return

        dims = {2: (2, 2, 2), 3: (2, 4, 3), 4: (4, 4, 4)}
        self.xDim, self.ySize, self.var_size = dims.get(var_len, (0, 0, 0))

        self.included_table = [[False] * self.ySize for _ in range(self.xDim)]
        self.map_vars = [[1] * self.ySize for _ in range(self.xDim)]
        self.map = [[False] * self.ySize for _ in range(self.xDim)]

        self.set_map(table)

    def set_map(self, table):
        for row in table:
            dims_coord = {
                4: (
                    str(int(row[0])) + str(int(row[1])),
                    str(int(row[2])) + str(int(row[3])),
                ),
                3: (str(int(row[0])), str(int(row[1])) + str(int(row[2]))),
                2: (str(int(row[0])), str(int(row[1]))),
            }

            x_str, y_str = dims_coord[self.var_size]
            x, y = self.get_coordinate(x_str), self.get_coordinate(y_str)
            self.map[x][y] = row[-1]
            self.map_vars[x][y] = [
                Variable(row[ind], var) for ind, var in enumerate(self.vars)
            ]

    def print_map(self):
        for row in self.map:
            print("".join(f"{checkUnit:<3}" for checkUnit in row))

    def calc_SKNF(self):
        return self._calc_SNF(False, "&")

    def calc_SDNF(self):
        return self._calc_SNF(True, "|")

    def _calc_SNF(self, condition, operator):
        list_regions = self.get_regions(condition)
        final_result = []

        for area_type in list_regions:
            for area in area_type:
                result = [
                    (
                        var.copy()
                        if all(var == area[j][i] for j in range(len(area)))
                        else None
                    )
                    for i, var in enumerate(area[0])
                ]
                result = [var for var in result if var is not None]
                if result:
                    if not condition:
                        for var in result:
                            var.positive = not var.positive
                    final_result.append(result)

        return get_str_from_full_form(final_result, operator)

    def is_suitable(self, area_size):
        return all(
            size <= limit for size, limit in zip(area_size, (self.xDim, self.ySize))
        )

    def get_regions(self, condition):
        return [
            areas
            for area_size in area_sizes
            if self.is_suitable(area_size)
            for areas in [self.find_region(area_size, condition)]
            if areas
        ]

    def find_region(self, area_size, condition):
        return [
            self.obtain_region(x, y, area_size)
            for x in range(len(self.map))
            for y in range(len(self.map[0]))
            if self.detect_region(x, y, area_size, condition)
        ]

    def obtain_region(self, x, y, area_size):
        return [
            self.get_variables(i, j)
            for i in range(x, x + area_size[0])
            for j in range(y, y + area_size[1])
            if self.mark_contained(i, j) or True
        ]

    def mark_contained(self, x, y):
        self.included_table[x % self.xDim][y % self.ySize] = True

    def get_variables(self, x, y):
        return self.map_vars[x % self.xDim][y % self.ySize]

    def detect_region(self, x, y, area_size, find_cond):
        return any(
            not self.is_contained(i, j)
            for i in range(x, x + area_size[0])
            for j in range(y, y + area_size[1])
            if self.is_correct(i, j) == find_cond
        ) and all(
            self.is_correct(i, j) == find_cond
            for i in range(x, x + area_size[0])
            for j in range(y, y + area_size[1])
        )

    def is_correct(self, x, y):
        return self.map[x % self.xDim][y % self.ySize]

    def is_contained(self, x, y):
        return self.included_table[x % self.xDim][y % self.ySize]

    def get_coordinate(self, table_part: str):
        return {"10": 3, "11": 2}.get(table_part, int(table_part, 2))

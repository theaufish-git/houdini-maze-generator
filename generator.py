# Maze generator -- Randomized Prim Algorithm
## Imports
import math
import random

class Maze:
    def __init__(self, wall="w", cell="c", unvisited="u", height=11, width=27, seed=None, data=None, rooms=0, min_room_radius=2, max_room_radius=10, trim_orphan_points=False):
        '''
        height - height of the maze as a number of vertices
        width  - width oof the maze as a number of vertices
        seed   - seed value for the random number generator. this should be set when it is necessary
               - to make subsequent calls that result in the same maze
        data   - when set this value is interpretted as the initial maze state and all 
                 generation steps are skipped. 
               - str  - a string representation of the maze. all whitespace is removed
                        prior to interpretation
               - list - a list of lists where each list contained represents a row
                        in the maze
        rooms  - the number of oval rooms to place on the map. these may overlap 
        min_room_radius - the minimum value to use when randomly determining the size of a room
        max_room_radius - the mazimum value to use when randomly determining the size of a room
        trim_orphan_points - when true all horizontal and vertical lines of length 0 will be
                             cleaned up

        wall - character of wall vertices. should only be set when data is not None.
        cell - character of cell vertices. should only be set when data is not None.
        unvisited - character of unvisited vertices. should only be set when data is not None.
        '''

        if isinstance(data, str):
            lines = data.split("\n")
            data = []
            for l in lines:
                if l == "":
                    continue
                data.append(list(l.replace(" ", "")))

        if isinstance(data, list):
            self._maze = data
            self._wall = wall
            self._cell = cell
            self._unvisited = unvisited
            self.height = len(self._maze)
            self.width = len(self._maze[0])
            return

        if seed is not None:
            random.seed(seed)

        self._wall = wall
        self._cell = cell
        self._unvisited = unvisited
        self.height = height
        self.width = width

        # Denote all cells as unvisited
        self._maze = [list(self._unvisited * self.width) for _ in range(0, self.height)]

        # Randomize starting point and set it a cell
        starting_height = int(random.random() * self.height)
        starting_width = int(random.random() * self.width)
        if starting_height == 0:
            starting_height += 1
        if starting_height == self.height - 1:
            starting_height -= 1
        if starting_width == 0:
            starting_width += 1
        if starting_width == self.width - 1:
            starting_width -= 1

        # Mark it as cell and add surrounding walls to the list
        self._maze[starting_height][starting_width] = self._cell
        walls = []
        walls.append([starting_height - 1, starting_width])
        walls.append([starting_height, starting_width - 1])
        walls.append([starting_height, starting_width + 1])
        walls.append([starting_height + 1, starting_width])

        # Denote walls in maze
        self._maze[starting_height - 1][starting_width] = self._wall
        self._maze[starting_height][starting_width - 1] = self._wall
        self._maze[starting_height][starting_width + 1] = self._wall
        self._maze[starting_height + 1][starting_width] = self._wall

        while walls:
            # Pick a random wall
            rand_wall = walls[int(random.random() * len(walls)) - 1]

            # Check if it is a left wall
            if rand_wall[1] != 0:
                if (
                    self._maze[rand_wall[0]][rand_wall[1] - 1] == self._unvisited
                    and self._maze[rand_wall[0]][rand_wall[1] + 1] == self._cell
                ):
                    # Find the number of surrounding cells
                    s_cells = self._surroundingCells(rand_wall)

                    if s_cells < 2:
                        # Denote the new path
                        self._maze[rand_wall[0]][rand_wall[1]] = self._cell

                        # Mark the new walls
                        # Upper cell
                        if rand_wall[0] != 0:
                            if self._maze[rand_wall[0] - 1][rand_wall[1]] != self._cell:
                                self._maze[rand_wall[0] - 1][rand_wall[1]] = self._wall
                            if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] - 1, rand_wall[1]])

                        # Bottom cell
                        if rand_wall[0] != height - 1:
                            if self._maze[rand_wall[0] + 1][rand_wall[1]] != self._cell:
                                self._maze[rand_wall[0] + 1][rand_wall[1]] = self._wall
                            if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] + 1, rand_wall[1]])

                        # Leftmost cell
                        if rand_wall[1] != 0:
                            if self._maze[rand_wall[0]][rand_wall[1] - 1] != self._cell:
                                self._maze[rand_wall[0]][rand_wall[1] - 1] = self._wall
                            if [rand_wall[0], rand_wall[1] - 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] - 1])

                    # Delete wall
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

                    continue

            # Check if it is an upper wall
            if rand_wall[0] != 0:
                if (
                    self._maze[rand_wall[0] - 1][rand_wall[1]] == self._unvisited
                    and self._maze[rand_wall[0] + 1][rand_wall[1]] == self._cell
                ):
                    s_cells = self._surroundingCells(rand_wall)
                    if s_cells < 2:
                        # Denote the new path
                        self._maze[rand_wall[0]][rand_wall[1]] = self._cell

                        # Mark the new walls
                        # Upper cell
                        if rand_wall[0] != 0:
                            if self._maze[rand_wall[0] - 1][rand_wall[1]] != self._cell:
                                self._maze[rand_wall[0] - 1][rand_wall[1]] = self._wall
                            if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] - 1, rand_wall[1]])

                        # Leftmost cell
                        if rand_wall[1] != 0:
                            if self._maze[rand_wall[0]][rand_wall[1] - 1] != self._cell:
                                self._maze[rand_wall[0]][rand_wall[1] - 1] = self._wall
                            if [rand_wall[0], rand_wall[1] - 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] - 1])

                        # Rightmost cell
                        if rand_wall[1] != width - 1:
                            if self._maze[rand_wall[0]][rand_wall[1] + 1] != self._cell:
                                self._maze[rand_wall[0]][rand_wall[1] + 1] = self._wall
                            if [rand_wall[0], rand_wall[1] + 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] + 1])

                    # Delete wall
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

                    continue

            # Check the bottom wall
            if rand_wall[0] != height - 1:
                if (
                    self._maze[rand_wall[0] + 1][rand_wall[1]] == self._unvisited
                    and self._maze[rand_wall[0] - 1][rand_wall[1]] == self._cell
                ):
                    s_cells = self._surroundingCells(rand_wall)
                    if s_cells < 2:
                        # Denote the new path
                        self._maze[rand_wall[0]][rand_wall[1]] = self._cell

                        # Mark the new walls
                        if rand_wall[0] != height - 1:
                            if self._maze[rand_wall[0] + 1][rand_wall[1]] != self._cell:
                                self._maze[rand_wall[0] + 1][rand_wall[1]] = self._wall
                            if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] + 1, rand_wall[1]])
                        if rand_wall[1] != 0:
                            if self._maze[rand_wall[0]][rand_wall[1] - 1] != self._cell:
                                self._maze[rand_wall[0]][rand_wall[1] - 1] = self._wall
                            if [rand_wall[0], rand_wall[1] - 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] - 1])
                        if rand_wall[1] != self.width - 1:
                            if self._maze[rand_wall[0]][rand_wall[1] + 1] != self._cell:
                                self._maze[rand_wall[0]][rand_wall[1] + 1] = self._wall
                            if [rand_wall[0], rand_wall[1] + 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] + 1])

                    # Delete wall
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

                    continue

            # Check the right wall
            if rand_wall[1] != width - 1:
                if (
                    self._maze[rand_wall[0]][rand_wall[1] + 1] == self._unvisited
                    and self._maze[rand_wall[0]][rand_wall[1] - 1] == self._cell
                ):

                    s_cells = self._surroundingCells(rand_wall)
                    if s_cells < 2:
                        # Denote the new path
                        self._maze[rand_wall[0]][rand_wall[1]] = self._cell

                        # Mark the new walls
                        if rand_wall[1] != self.width - 1:
                            if self._maze[rand_wall[0]][rand_wall[1] + 1] != self._cell:
                                self._maze[rand_wall[0]][rand_wall[1] + 1] = self._wall
                            if [rand_wall[0], rand_wall[1] + 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] + 1])
                        if rand_wall[0] != self.height - 1:
                            if self._maze[rand_wall[0] + 1][rand_wall[1]] != self._cell:
                                self._maze[rand_wall[0] + 1][rand_wall[1]] = self._wall
                            if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] + 1, rand_wall[1]])
                        if rand_wall[0] != 0:
                            if self._maze[rand_wall[0] - 1][rand_wall[1]] != self._cell:
                                self._maze[rand_wall[0] - 1][rand_wall[1]] = self._wall
                            if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] - 1, rand_wall[1]])

                    # Delete wall
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

                    continue

            # Delete the wall from the list anyway
            for wall in walls:
                if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                    walls.remove(wall)

        # Mark the remaining unvisited cells as walls
        self._setUnvisitedAsWalls()

        # Set entrance and exit
        self._setIngressEgress()

        # Add rooms
        for i in range(0, rooms):
            x_r = random.randint(min_room_radius, max_room_radius)
            y_r = random.randint(min_room_radius, max_room_radius)

            x_p = random.randint(1, self.width - 1 - x_r * 2)
            y_p = random.randint(1, self.height - 1 - y_r * 2)

            self.addRoom(x_p, y_p, x_r, y_r)

        # Remove walls that have no neighboring walls
        if trim_orphan_points:
            self._trimOrphanPoints()   
    
    def addRoom(self, x_p, y_p, x_r, y_r):
        '''
        calculates an oval with radii x_r and y_r at the offset
        x_p, y_p and sets all contained points to cell.
        '''
        # create arc buffer
        arc = [list(self._wall * x_r) for _ in range(0, y_r)]
        # paint x,y pairs after solving for y
        for x in range(0, x_r):
            y_f = math.sqrt((1 - x**2 / x_r**2) * y_r**2)
            y = int(y_f+.5) - 1
            arc[y][x] = self._cell
        
        # paint x,y pairs after solving for x
        for y in range(0, y_r):
            x_f = math.sqrt((1 - y**2 / y_r**2) * x_r**2)
            x = int(x_f+.5) - 1
            arc[y][x] = self._cell      

        '''
        calculating the points for an oval by using x and solving for y,
        or vice versa can result in a non-closed shape. this can be avoided
        by overlaying bother calculations on top of each other. due to rounding
        errors this can lead to fragments near the edges of the arcs.        

        done = 0 - not started
             = 1 - started
             = 2 - complete
        '''
        # cleanup x fragments
        for x in range(0, x_r):
            done = 0
            for y in range(0, y_r):
                if arc[y][x] != self._wall:
                    if done == 2:
                        arc[y][x] = self._wall
                    else:
                        done = 1
                elif done == 1:
                    done = 2
                elif done == 0:
                    arc[y][x] = self._cell
        
        # cleanup y fragments
        for y in range(0, y_r):
            done = 0
            for x in range(0, x_r):
                if arc[y][x] != self._wall:
                    if done == 2:
                        arc[y][x] = self._wall
                    else:
                        done = 1
                elif done == 1:
                    done = 2
                elif done == 0:
                    arc[y][x] = self._cell

        # use the arc to generate an oval onto the maze
        for y in range(0, y_r):
            for x in range(0, x_r):
                if arc[y][x] != self._wall:
                    self._maze[y+y_r+y_p][x+x_r+x_p] = self._cell
                    self._maze[y+y_r+y_p][x_r-1-x+x_p] = self._cell
                    self._maze[y_r-y-1+y_p][x+x_r+x_p] = self._cell
                    self._maze[y_r-y-1+y_p][x_r-1-x+x_p] = self._cell

    def addToHoudini(self, hou, units=3):
        '''
        adds the generated map into the houdini node as a series of arcs
        '''
        node = hou.pwd()
        geo = node.geometry()
        
        for (x1,y1),(x2,y2) in self._horizontalEdges():
            curve = geo.createBezierCurve(2, order=2)
            
            invertices = [
                (x1*units,0,y1*units),
                (x2*units,0,y2*units)
            ]
            outvertices = curve.vertices()
            for v in range(0, len(outvertices)):
                outvertices[v].point().setPosition(invertices[v])
            
        for (x1,y1),(x2,y2) in self._verticalEdges():
            curve = geo.createBezierCurve(2, order=2)
            
            invertices = [
                (x1*units,0,y1*units),
                (x2*units,0,y2*units)
            ]
            outvertices = curve.vertices()
            for v in range(0, len(outvertices)):
                outvertices[v].point().setPosition(invertices[v])

    def _horizontalEdges(self):
        '''
        returns a list of all wall edges that can be generated by drawing
        horizontal lines through the given points
        '''
        edges = []

        for row in range(0, self.height):
            s = None
            for col in range(0, self.width):
                if self._maze[row][col] == self._wall:
                    if s == None:
                        s = col
                        continue
                elif self._maze[row][col] == self._cell:
                    if s != None:
                        edges.append(((s, row), (col-1, row)))
                        s = None
            if s != None:
                edges.append(((s, row), (col, row)))

        return edges

    def _verticalEdges(self):
        '''
        returns a list of all wall edges that can be generated by drawing
        vertical lines through the given points
        '''
        edges = []

        for col in range(0, self.width):
            s = None
            for row in range(0, self.height):
                if self._maze[row][col] == self._wall:
                    if s == None:
                        s = row
                        continue
                elif self._maze[row][col] == self._cell:
                    if s != None:
                        edges.append(((col, s), (col, row-1)))
                        s = None
            if s != None:
                edges.append(((col, s), (col, row)))

        return edges

    def _setIngressEgress(self):
        for i in range(0, self.width):
            if self._maze[1][i] == self._cell:
                self._maze[0][i] = self._cell
                break

        for i in range(self.width - 1, 0, -1):
            if self._maze[self.height - 2][i] == self._cell:
                self._maze[self.height - 1][i] = self._cell
                break

    def _setUnvisitedAsWalls(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self._maze[i][j] == self._unvisited:
                    self._maze[i][j] = self._wall

    def _surroundingCells(self, rand_wall):
        '''
        returns the number of surrounding cells
        '''
        s_cells = 0
        if self._maze[rand_wall[0] - 1][rand_wall[1]] == self._cell:
            s_cells += 1
        if self._maze[rand_wall[0] + 1][rand_wall[1]] == self._cell:
            s_cells += 1
        if self._maze[rand_wall[0]][rand_wall[1] - 1] == self._cell:
            s_cells += 1
        if self._maze[rand_wall[0]][rand_wall[1] + 1] == self._cell:
            s_cells += 1

        return s_cells

    def _trimOrphanPoints(self):
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self._maze[y-1][x] != self._wall and self._maze[y+1][x] != self._wall and self._maze[y][x-1] != self._wall and self._maze[y][x+1] != self._wall:
                    self._maze[y][x] = self._cell

maze = Maze(height=64, width=64, seed=14, rooms=7, min_room_radius=3, max_room_radius=5, trim_orphan_points=True)
maze.addToHoudini(hou)

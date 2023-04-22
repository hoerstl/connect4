import turtle
import time


class GameLogic:

    def __init__(self):
        self.logoTurtle = turtle.Turtle()

        self.drawingTurtle = turtle.Turtle()

        self.selectionCursor = turtle.Turtle()


        self.columnnumSelection = 3
        self.cursorY = 162.5
        self.turnInProgress = False
        self.logicInProgress = False
        self.gameboard = None

        # Loser goes first but black starts. Black is Even turn numbers.
        self.playerTurn = 1
        self.gameover = False

        self.beginGame()


    def beginGame(self):
        # Start the game
        self.gameover = False
        self.playerTurn += 1
        # Reset the turtles for drawing and pointing
        self.logoTurtle.reset()
        self.logoTurtle.hideturtle()
        self.logoTurtle.color("black")
        self.logoTurtle.penup()
        self.logoTurtle.goto(0, 230)

        self.drawingTurtle.reset()
        self.drawingTurtle.hideturtle()

        self.selectionCursor.reset()
        self.selectionCursor.hideturtle()
        self.selectionCursor.penup()
        self.selectionCursor.pensize(30)
        self.selectionCursor.seth(270)

        # Create an empty board
        self.gameboard = [[0 for i in range(7)] for j in range(6)]

        # Draw the board and begin the first turn
        self.drawBoard()
        self.beginTurn()


    def drawBoard(self):
        # Draw Connect 4 at the top of the thing
        self.logoTurtle.write("Connect 4!", align="center", move=False,
                                 font=('Arial', 40, 'normal'))

        # Draw outer box
        self.drawingTurtle.speed(0)
        self.drawingTurtle.penup()
        self.drawingTurtle.goto(-262.5, 125)
        self.drawingTurtle.pendown()
        self.drawingTurtle.goto(262.5, 125)
        self.drawingTurtle.goto(262.5, -175)
        self.drawingTurtle.goto(-262.5, -175)
        self.drawingTurtle.goto(-262.5, 125)

        # Draw all empty circles
        self.drawingTurtle.seth(180)
        for rowNum in range(6):
            for columnNum in range(7):
                self.fillInSpace(rowNum, columnNum, self.gameboard[rowNum][columnNum])


    def beginTurn(self):

        self.columnnumSelection = 3
        self.updateCursorPosition()
        self.selectionCursor.color("black" if self.playerTurn % 2 == 0 else "red")
        self.selectionCursor.showturtle()


    def endTurn(self):

        self.selectionCursor.hideturtle()
        self.updateCursorPosition()
        self.playerTurn += 1


    def moveCursorLeft(self):
        if self.logicInProgress:
            return

        self.logicInProgress = True

        if self.columnnumSelection > 0:
            self.columnnumSelection -= 1
        self.updateCursorPosition()

        self.logicInProgress = False


    def moveCursorRight(self):
        if self.logicInProgress:
            return

        self.logicInProgress = True

        if self.columnnumSelection < 6:
            self.columnnumSelection += 1
        self.updateCursorPosition()

        self.logicInProgress = False


    def submitMove(self):
        if self.logicInProgress:
            return

        self.logicInProgress = True

        # Hide the cursor
        self.selectionCursor.hideturtle()

        # Update the self.gameboard with the newly dropped piece
        try:
            self.dropPiece()
        except RuntimeError as err:
            print(err)
            self.selectionCursor.showturtle()
            self.logicInProgress = False
            return

        # Stop here if the game is already over
        if self.gameover:
            # This allows for a fun overkill mode after winning where you place your pieces wherever
            self.logicInProgress = False
            self.selectionCursor.showturtle()
            return

        # check for wins
        if self.checkForWins():
            self.winSequence()
            self.logicInProgress = False
            return

        # end the turn
        self.endTurn()

        # conditional start of a new turn
        self.beginTurn()

        self.logicInProgress = False


    def dropPiece(self):
        """
        Checks every row in the currently selected column bottom up to find an open spot to drop the piece.
        -Finds the lowest spot to drop the game piece in the self.columnnumSelection column
        -Updates self.gameboard with the correct color for that space
        -Calls fillInSpace to draw it to the screen

        :return: None
        """
        playerColorNumber = 1 if self.playerTurn % 2 == 1 else 2
        for rowNumber in range(5, -1, -1):
            if self.gameboard[rowNumber][self.columnnumSelection] == 0:
                self.gameboard[rowNumber][self.columnnumSelection] = playerColorNumber
                self.fillInSpace(rowNumber, self.columnnumSelection, playerColorNumber)
                return

        raise RuntimeError("Column is full of pieces.")


    def fillInSpace(self, row, column, colornumber):
        if colornumber == 0:
            self.drawingTurtle.pencolor("black")
            self.drawingTurtle.fillcolor("white")
        elif colornumber == 1:
            self.drawingTurtle.color("red")
        elif colornumber == 2:
            self.drawingTurtle.color("black")
        else:
            raise ValueError(f"Color number {colornumber} is not 0, 1, or 2")

        if row > 5:
            raise ValueError(f"Row number {row} is too high. Must be < 5.")
        if column > 6:
            raise ValueError(f"Column number {column} is too high. Must be < 6.")


        self.drawingTurtle.penup()
        self.drawingTurtle.goto(-225 + column * 75, 110 + row * -50)
        self.drawingTurtle.pendown()
        self.drawingTurtle.begin_fill()
        self.drawingTurtle.circle(10)
        self.drawingTurtle.end_fill()


    def updateCursorPosition(self):
        self.selectionCursor.goto(-225 + 75 * self.columnnumSelection, self.cursorY)


    def checkForWins(self):
        for rownumber in range(6):
            for columnnumber in range(7):
                hwin = self.checkHorizontalWin(rownumber, columnnumber)
                vwin = self.checkVerticalWin(rownumber, columnnumber)
                drwin = self.checkRightDiagonalWin(rownumber, columnnumber)
                dlwin = self.checkLeftDiagonalWin(rownumber, columnnumber)
                if hwin or vwin or drwin or dlwin:
                    return True
        return False


    def checkHorizontalWin(self, startingrow, startingcolumn):
        if startingcolumn > 3:
            return False

        currentPlayerNumber = 2 if self.playerTurn % 2 == 0 else 1

        for i in range(4):
            if self.gameboard[startingrow][startingcolumn + i] != currentPlayerNumber:
                return False
        return True


    def checkVerticalWin(self, startingrow, startingcolumn):
        if startingrow > 2:
            return False

        currentPlayerNumber = 2 if self.playerTurn % 2 == 0 else 1

        for i in range(4):
            if self.gameboard[startingrow + i][startingcolumn] != currentPlayerNumber:
                return False
        return True


    def checkRightDiagonalWin(self, startingrow, startingcolumn):
        if startingrow > 2 or startingcolumn > 3:
            return False

        currentPlayerNumber = 2 if self.playerTurn % 2 == 0 else 1

        for i in range(4):
            if self.gameboard[startingrow + i][startingcolumn + i] != currentPlayerNumber:
                return False
        return True



    def checkLeftDiagonalWin(self, startingrow, startingcolumn):
        if startingrow > 2 or startingcolumn < 3:
            return False

        currentPlayerNumber = 2 if self.playerTurn % 2 == 0 else 1

        for i in range(4):
            if self.gameboard[startingrow + i][startingcolumn - i] != currentPlayerNumber:
                return False
        return True


    def winSequence(self):
        winningPlayerColor = "black" if self.playerTurn % 2 == 0 else "red"

        self.logoTurtle.clear()
        self.logoTurtle.color(winningPlayerColor)
        self.logoTurtle.write(f"{winningPlayerColor.upper()} Wins!", align="center", move=False, font=('Arial', 30, 'bold'))

        self.selectionCursor.showturtle()

        self.gameover = True


    def startNewGame(self):
        if self.logicInProgress:
            return

        self.logicInProgress = True

        if self.gameover:
            self.beginGame()

        self.logicInProgress = False


def main():
    # Initlize the game screen
    screen = turtle.Screen()
    screen.title("Can you Connect 4?")
    game = GameLogic()
    turtle.onkeypress(game.moveCursorLeft, "Left")
    turtle.onkeypress(game.moveCursorRight, "Right")
    turtle.onkeypress(game.submitMove, "Down")
    turtle.onkeypress(game.startNewGame, "space")
    turtle.listen()
    screen.mainloop()


if __name__ == "__main__":
    main()


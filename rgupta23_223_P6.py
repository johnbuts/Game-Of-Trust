#-------------------------------------------------------------------------------
# Name: Rishab Gupta
# Game of Trust:


class Move:
    def __init__(self, cooperate = True): #The first constructor we have, just creating which move they chose
        self.cooperate = cooperate
    def __str__(self): #For printing the object, . if the opponent co-op, x if they didn't
        if self.cooperate == True:
            return '.'
        else:
            return 'x'
    def __repr__(self):
        return "Move(%r)" % (self.cooperate)
    def __eq__(self, other):#overrides the == function, handy for seeing if a move equals another
        return self.cooperate == other.cooperate
          
    def change(self): #just changes the decision of the opponent
        if self.cooperate == False:
            self.cooperate = True
        else:
            self.cooperate = False
    def copy(self): #Just returning the opponents decision
        return Move(self.cooperate)
class PlayerException(Exception): #Calling this everytime a player exception happens, pretty much when you input two identical 
#players into a function that takes two different ones
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg
    def __repr__(self):
        return "PlayerException(%s)" % ("'" + self.msg + "'")
class Player:
    def __init__(self, style, points = 0, history = None): #Constructor that states the objects history,
# points, and makes sure the input is an actual style
        listOfStyles = ['previous', 'friend' , 'cheater', 'grudger', 'detective']
        if history == None:
            self.history = []
        else:
            self.history = history
        self.points = points
        if style not in listOfStyles:
            raise PlayerException("no style '%s'." % (style))
        else:
            self.style = style
    def __str__(self): #Printing the object nicely
        s = ""
        if self.history == []:
            return "%s(%d)" % (self.style, self.points)
        else:
            for i in self.history:
                if i.cooperate == True:
                    s += "."
                else:
                    s += "x"
            return "%s(%d)%s" % (self.style, self.points, s)
    def __repr__(self):
        return "Player(" + "'" + self.style + "'" + ', ' + str(self.points) + ', ' + str(self.history) + ')'

    def reset_history(self): #Sets the history to empty
        self.history = []
    def reset(self): #Sets history and pts to nothin
        self.history = []
        self.points = 0
    def update_points(self, amount): #updating the points a certain amount
        self.points += amount
    def ever_betrayed(self): #Says if they are ever betrayed in it's history, if theres ever a Move(False)
        if len(self.history) == 0:
            return False
        for i in range(len(self.history)):
            if self.history[i].cooperate == False:
                return True
            if i == len(self.history) - 1:
                return False
    def record_opponent_move(self, move):#appending a move into the history of an object
        self.history.append(move)
    def copy_with_style(self): #copying another objects style
        return Player(self.style)
    def choose_move(self): #The main move logic given a player object
        if self.style == 'friend': #If the objects style is friend it always returns true
            return Move(True) 
        if self.style == 'cheater':#If they are a cheater their move is always false
            return Move(False)
        if self.style == 'previous':
            if len(self.history) == 0: #First Move
                return Move(True) #For previous, the first move is true, and then mocks the opponents last move
            else:
                return self.history[-1]
        if self.style == 'grudger': #Grudger, if it ever has a false in it's history, it returns a false, otherwise it returns true
            for i in self.history:
                if i == Move(False):
                    return Move(False)            
            else:
                return Move(True)
        if self.style == 'detective': #Coded the first 4 moves, and if it's never betrayed, then the detective choses false, but if it
        #is ever betrayed, it mocks the latest move of its opponent
            false_counter = 0
        #First four moves
            if len(self.history) == 0:
                return Move(True)
            if len(self.history) == 1:
                return Move(False)
            if len(self.history) == 2:
                return Move(True)
            if len(self.history) == 3:
                return Move(True)
            for i in range(len(self.history)):
                if self.history[i] == Move(False):
                    false_counter += 1
            if false_counter == 0:
                return Move(False)
            else:
                return self.history[-1]
                
def turn_payouts(move_a, move_b):
#Simple coding here, literally just returning the values based on which player won/lost
    if move_a.cooperate == True and move_b.cooperate == True:
        return (2,2)
    if move_a.cooperate == False and move_b.cooperate == False:
        return (0,0)
    if move_a.cooperate == True and move_b.cooperate == False:
        return (-1,3)
    if move_a.cooperate == False and move_b.cooperate == True:
        return (3,-1)
        
def build_players(initials): 
#This makes inputing into tournament a breeze, it converts a list of integers into a list of objects
#so you just have to input a list of integers, and makes sure your inputs are correct
    listOfStyles = ['previous', 'friend' , 'cheater', 'grudger', 'detective']
    listOfInitials = ['p','f','c','g','d']
    empty = []    
    for i in initials:
        for j in listOfStyles:
            if i == j[0]:
                empty.append(Player(j))
    for i in initials:
        if i not in listOfInitials:
            raise PlayerException("no style with initial " + "'" + i + "'.")
    return empty
def composition(players):
#Rounds up the game nicely, and returns a dict of how many people are remaining in the game
    empty = {}
    #Creating a counter for each style in the players list
    fcounter = 0
    pcounter = 0
    gcounter = 0
    dcounter = 0
    ccounter = 0
    #the first loop adds one to the counter per style
    for i in players:
        if i.style == 'friend':
            fcounter += 1
        if i.style == 'previous':
            pcounter += 1
        if i.style == 'grudger':
            gcounter += 1
        if i.style == 'detective':
            dcounter += 1
        if i.style == 'cheater':
            ccounter += 1
    #The second list is the one actually "appending" the counter values to the "empty" dict
    #Along with the correct key value
    for i in players:
        if i.style == 'friend':
            empty[i.style] = fcounter
        if i.style == 'previous':
            empty[i.style] = pcounter
        if i.style == 'grudger':
            empty[i.style] = gcounter
        if i.style == 'detective':
            empty[i.style] = dcounter
        if i.style == 'cheater':
            empty[i.style] = ccounter
    return empty
    
def run_turn(player_a, player_b):
#Where the game logic comes in, what I did was append the opponents move into the others history
#and added points based on there last move using the logic from turn_payouts. Also doesn't crash when player_a
#is equal to player_b
    z = player_a.choose_move()
    d = player_b.choose_move()
    player_b.history.append(z)
    player_a.history.append(d)
    x = turn_payouts(player_b.history[-1], player_a.history[-1])
    player_a.points += x[0] - 1
    player_b.points += x[1] - 1
    if player_a == player_b:
        raise PlayerException("players must be distinct.")
    
    
def run_game(player_a, player_b, num_turns = 5):
#Just clears both of the players history, and runs run_turn however many
#games you want
    if player_a == player_b:
        return None
    del player_a.history[:]
    del player_b.history[:]
    for i in range(num_turns):
        run_turn(player_a, player_b)
        
def run_tournament(players, num_turns = 10, num_rounds = 5, starting_points = 0, num_replaces = 5):
    for i in players:#gives all players the correct staring_points
        i.points = starting_points
    
    for rounds in range(num_rounds):
        empty = []#resets this list since it stores the new game each time
        min = []#same with empty, needs to be reset for every num_replaces
        max = []#same with min, the winners need to be reset every round
        for i in range(len(players)):
            for j in range(len(players)):
                if i != j:
                    run_game(players[i],players[j], num_turns) # getting all of the scores of the games

        for i in players:
            empty.append(i.points)
        empty.sort()
        min = []
        max = []

        copy = players[:]
        for i in range(num_replaces):        #Geting all of the min values removed from players
            if i < len(empty) - 1:
                min.append(empty[i])
        for i in copy:
            if i.points in min: 
                players.remove(i)
                min.remove(i.points)
        
            

        for b in range(len(empty) - 1, len(empty) - num_replaces - 1, -1): #appending all of the winners back into players
            max.append(empty[b])
        for i in copy:
            if i.points in max:
                players.append(i)
                max.remove(i.points)
    if players == []:
        raise PlayerException("all players died after round %d.") % (round)

    
    return composition(players)
            
        
                
    
        
            
                
                    
            
            
    
     
     
     
     
     
     
     
     
     
    
                    
                    
                
                
                
                
                
                
                
                
    

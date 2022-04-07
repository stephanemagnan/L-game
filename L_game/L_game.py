import numpy as np

class L_game:
    def __init__(self):
        print("Initialising learner...")
        
        self.turn = 0
        self.toplay = 1
        self.phase = 0
        self.board = np.array([[3, 1, 1, 0],
                [0, 2, 1, 0],
                [0, 2, 1, 0],
                [0, 2, 2, 4]])      

        self.get_L_moves()
        self.get_O_moves()

    def get_L_moves(self):        
        #transform to boolean
        self.boolboard = np.logical_or(self.board == 0,self.board == self.toplay)

        positions = np.ones((48, 1), dtype=bool)

        moves = list()

        for this_ind,this_pos  in enumerate(positions): 

            this_L_pos = self.get_L_coords(this_ind)
            # print(this_ind,this_L_pos)

            reuse_cells = 0
            for this_cell in this_L_pos:
                #verify that the exact same move is not allowed
                if self.board[this_cell[1],this_cell[0]]==self.toplay:
                    reuse_cells+=1
                    if reuse_cells == 4:
                        positions[this_ind] = False
                        break
                #verify that there is move does not overlap any other moves
                if not self.boolboard[this_cell[1],this_cell[0]]:
                  positions[this_ind] = False
                  break  
            #print(this_ind,this_L_pos,positions[this_ind])     
            if positions[this_ind]:
                moves.append(this_ind)

        self.L_moves = moves

    def get_O_moves(self):        
        #transform to boolean
        self.boolboard = (self.board == 0)

        positions = np.ones((16, 1), dtype=bool)

        moves = list()

        for this_ind,this_pos  in enumerate(positions): 
  
            this_x = (this_ind)%4
            this_y = (this_ind)//4

            #print(this_ind,this_x,this_y,self.boolboard[this_y,this_x])
            if not self.boolboard[this_y,this_x]:
                positions[this_ind] = False
                
            if positions[this_ind]:
                moves.append(this_ind)
        
        self.O_moves = moves

    def check_status(self):
        #false indicates no valid moves are found
        if len(self.get_moves())==0:
            print("Game over.")
            return False
        else:
            return True


    def move_L(self,position):
        #player is automatically known from "toplay"
        self.board[self.board==self.toplay]=0
        
        this_L_pos = self.get_L_coords(position)

        for this_cell in this_L_pos:
            self.board[this_cell[1],this_cell[0]]=self.toplay

        #increase turn phase 
        self.phase+=1

    def move_O(self,marker,position):
        self.board[self.board==marker]=0
        
        self.board[position//4,position%4]=marker

        #officially turn to next turn
        self.phase=0
        self.toplay=1-(self.toplay-1)+1
        self.turn+=1

    def get_L_coords(self,position):
        #apply transformation to L originally located at NW with vertical stem and nub pointing right
        #order of transformations: shift x, shift y, mirror along XY, mirror along X, mirror along Y

        this_L_pos = np.array([[0,2],[0,1],[0,0],[1,0]])
        this_x = (position)%3
        this_y = (position//3)%2
        this_rxy = (position//24)%2
        this_rx = (position//12)%2
        this_ry = (position//6)%2

        #print(position,this_x,this_y,this_rxy,this_rx,this_ry)

        this_L_pos[:,0]+=this_x
        this_L_pos[:,1]+=this_y

        if this_rxy:
            this_L_pos[:,[0,1]] = this_L_pos[:,[1,0]]

        if this_rx:
            this_L_pos[:,1] = 3-this_L_pos[:,1]
        if this_ry:
            this_L_pos[:,0] = 3-this_L_pos[:,0]
    
        return this_L_pos
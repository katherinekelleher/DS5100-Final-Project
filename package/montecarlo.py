import numpy as np
import pandas as pd
class Die():
    "Takes a NumPy array of faces and creates a die of N sides and W weights. Weights default to 1 for each side but can be updated."   
    def __init__(self, array_faces):
        "Initalize the object by defining the faces on the die. Faces must be all numeric or all text. Weights can be changed after initialization."
        self.array_faces = array_faces
        if isinstance(self.array_faces, np.ndarray) == False:
            raise TypeError("Input value must be of type np array.")
            
        if len(self.array_faces) != len(set(self.array_faces)):
            raise TypeError("Input values must be unique.")
        
        else:
            self.n_sides = len(self.array_faces)
            self.weights = [1] * self.n_sides
            self.my_probs = [i/sum(self.weights) for i in self.weights]
            self.die = pd.DataFrame({
            'side': self.array_faces,
            'weights': self.weights})
            self.die = self.die.set_index(['side'])
            
    def update_die_weight(self, face_value, weight_value):
        "Update weights of die object after initialization. Input is a face value that exists in die object and an integer or float for die weight. Changes weight of die."
        self.face_value = face_value
        self.weight_value = weight_value
        if isinstance(self.weight_value, (int, float)) == False:
                try:
                    self.weight_value = float(self.weight_value)
                except ValueError:
                    raise TypeError("Input weight value must be of type int, float, or coercible.")
        if face_value not in self.die.index:
            raise TypeError("Input face value must be within die array.")
        else: 
            new_side = pd.DataFrame({'side': [self.face_value], 'weights': [self.weight_value]})
            new_side['weights'] = new_side['weights'].astype('Int64')
            self.die = pd.concat([self.die, new_side], ignore_index=True)

    def roll_dice(self, n_rolls=1):
    "Rolling die objects one or more times. Input is integer number of dice rolls and is initialized to 1, but can be changed. Creates series of rolls and values for all die objects."
        results = []
        for i in range(n_rolls):
            result = self.die.sample(weights=self.die.weights).index[0]
            results.append(result)
        return pd.Series(results)
    
class Game():
    "A game consists of rolling of one or more similar dice (Die objects) one or more times."
    def __init__(self, dice_list):
    "Initalize the object by a list of die objects."
        self.dice_list = dice_list
        
    def play(self, n_rolls):
        "Play game by rolling dice (Die objects) one or more times. Input is integer number of dice rolls. Creates data frame of rolls and values for all die objects."
        self.game_play_df = pd.DataFrame()
        for i in range(len(self.dice_list)):
            die = self.dice_list[i]
            self.game_play_df[i+1] = die.roll_dice(n_rolls)
            
        self.game_play_df.index.name = "Roll Number"
    
    def return_play_df(self, form):
        "Return game play from dice rolls in dataframe by entering input value of 'narrow' or 'wide.' Returns dataframe of die object rolls with varied format based on input option."
        self.form = form
        if self.form == "narrow":
            narrow_df = self.game_play_df.stack()
            narrow_df = narrow_df.reset_index()
            narrow_df.columns = ["Roll Number", "Die", "Face Value"]
            return narrow_df
        elif self.form == "wide":
            return self.game_play_df
        else:
            raise ValueError("Input face value must be 'narrow' or 'wide.'")
            
class Analyzer():
    "Takes an Game object and computes various descriptive statistical properties about it."
    def __init__(self, game_obj):
        "Initalize the class with a Game() object."
        self.game = game_obj
        if isinstance(self.game, Game) == False:
            raise ValueError("Input value must be a game object.")
        
    def jackpot(self):
        "Identify any jackpot results in die game."
        self.jackpot_columns = 0
        self.game.play(n_rolls)
        self.df = self.game.return_play_df("wide")
        for col in self.df.columns:
            if self.df[col].nunique() == 1:
                self.jackpot_columns += 1
            return self.jackpot_columns
        
    def face_counts(self):
        "Computes how many times a given face is rolled in each event."
        self.game.play(n_rolls)
        self.df = self.game.return_play_df("wide")
        self.face_count_df = self.df.apply(lambda x: x.value_counts(), axis =1)
        return self.face_count_df
    
    def combo_count(self):
        "Computes the distinct combinations of faces rolled, along with their counts. Transforms Analyzer object's return_play_df('wide')."
        self.df_combo = self.game.return_play_df("wide")
        roll_sorted = self.df_combo.apply(lambda x:tuple(sorted(x)), axis =1)
        distinct_combinations_df = roll_sorted.value_counts(dropna=False).reset_index(name='count')
        return distinct_combinations_df
    
    def perm_count(self):
        "Computes the distinct permutations of faces rolled, along with their counts. Transforms Analyzer object's return_play_df('wide')."
        self.df_perm = self.game.return_play_df("wide")
        distinct_permutations_df = self.df_perm.value_counts(dropna=False).reset_index(name='count')
        return distinct_permutations_df
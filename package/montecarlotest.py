from montecarlo import Die, Game, Analyzer
import unittest
import pandas as pd
import numpy as np

class montecarloTestDie(unittest.TestCase): 
    def test_create_die_structure(self): #test
        faces = np.array([1,2,3,4,5,6])
        die = Die(faces)
        expected_df = pd.DataFrame({
            'weights':[1,1,1,1,1,1],
            'side':faces})
        
        weights_equal = (expected_df['weights'].values == die.die['weights'].values).all()
        faces_equal = (die.die.index.values == expected_df['side'].values).all()
        self.assertEqual(weights_equal, True)
        self.assertEqual(faces_equal, True)
 
    def test_update_die_weight(self): #
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        die.update_die_weight(3, 5)
        
        self.assertEqual(die.die.loc[3, 'weights'], 5)

    def test_play_game_structure(self):
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        game = Game([die, die])
        game.play(5)

        self.assertEqual(game.game_play_df.shape, (5, 2))


    def test_return_play_df(self):
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        game = Game([die, die])
        game.play(5)
        narrow_df = game.return_play_df('narrow')
        wide_df = game.return_play_df('wide')
        
        
        self.assertEqual(narrow_df.shape[0], 10)
        self.assertListEqual(list(narrow_df.columns), ["Roll Number", "Die", "Face Value"])
        self.assertEqual(wide_df.shape, (5, 2))
        
    def test_analyzer_jackpot(self): #check
        faces = np.array([1, 2]) 
        die = Die(faces)
        game = Game([die, die])
        analyzer = Analyzer(game)
        game.play(5)
        jackpot_count = analyzer.jackpot()
        
        self.assertLess(jackpot_count, 6)

    def test_analyzer_face_counts(self): #check
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        game = Game([die])
        analyzer = Analyzer(game)
        game.play(5)
        face_counts_df = analyzer.face_counts()
        self.assertEqual(len(face_counts_df), 5)  # 5 rolls
        self.assertTrue(all(face_counts_df.columns.isin(faces)))  # Columns should be the faces
        
    def test_analyzer_combo_counts(self):
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        game = Game([die, die])
        analyzer = Analyzer(game)
        game.play(5)
        combo_df = analyzer.combo_count()
        
        self.assertEqual(sum(combo_df['count']), 5)
        #self.assertTrue(all(isinstance(x, tuple) for x in combo_df[0]))

 
    def test_perm_count_structure(self):
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        game = Game([die, die])
        analyzer = Analyzer(game)
        game.play(5)
        perm_df = analyzer.perm_count()
        list_in = perm_df[1].isin(faces)
        
        self.assertEqual(sum(perm_df['count']), 5)
        self.assertTrue(len(perm_df[list_in]) == len(perm_df))

                
if __name__ == '__main__':
    
    unittest.main(verbosity=3)
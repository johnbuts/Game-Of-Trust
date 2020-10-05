
#   python3 <thisfile.py> <your_one_file.py>
import unittest
import shutil
import sys
import os
import time


############################################################################
############################################################################
# BEGIN SPECIALIZATION SECTION (the only part you need to modify beyond 
# adding new test cases).

# name all expected definitions; if present, their definition (with correct
# number of arguments) will be used; if not, a decoy complainer function
# will be used, and all tests on that function should fail.
    
REQUIRED_DEFNS = ["Move",
                  "PlayerException",
                  "Player",
                  "turn_payouts",
                  "build_players",
                  "composition",
                  "run_turn",
                  "run_game",
                  "run_tournament",
                 ]

# for method names in classes that will be tested
SUB_DEFNS = [ "change",
              "copy",
              "reset_history",
              "reset",
              "update_points",
              "ever_betrayed",
              "record_opponent_move",
              "copy_with_style",
              "choose_move",
            ]

# definitions that are used for extra credit
EXTRA_CREDIT_DEFNS = []

# how many points are test cases worth?
weight_required = 1
weight_extra_credit = 0

# don't count extra credit; usually 100% if this is graded entirely by tests.
# it's up to you the instructor to do the math and add this up!
# TODO: auto-calculate this based on all possible tests.
total_points_from_tests = 100

# how many seconds to wait between batch-mode gradings? 
# ideally we could enforce python to wait to open or import
# files when the system is ready but we've got a communication
# gap going on.
DELAY_OF_SHAME = 1


# set it to true when you run batch mode... 
CURRENTLY_GRADING = False



# what temporary file name should be used for the student?
# This can't be changed without hardcoding imports below, sorry.
# That's kind of the whole gimmick here that lets us import from
# the command-line argument without having to qualify the names.
RENAMED_FILE = "student"




# END SPECIALIZATION SECTION
############################################################################
############################################################################


# enter batch mode by giving a directory to work on as the only argument.
BATCH_MODE = len(sys.argv)==2 and (sys.argv[1] in ["."] or os.path.isdir(sys.argv[1]))

# This class contains multiple "unit tests" that each check
# various inputs to specific functions, checking that we get
# the correct behavior (output value) from completing the call.
class AllTests (unittest.TestCase):

    ############################################################################
    
    # Move class. 10 tests.
    
    # init, str, repr
    def test_Move_1(self):
        """ Move.__init__ """
        m1 = Move(True)
        self.assertEqual(m1.cooperate, True)
        
        m2 = Move(False)
        self.assertEqual(m2.cooperate, False)
        
    def test_Move_2(self):
        """ Move.__init__ defaults."""
        m = Move()
        self.assertEqual(m.cooperate, True)
    
    def test_Move_3(self):
        """ Move.__str__ """
        m1 = Move(True)
        m2 = Move(False)
        self.assertEqual(str(m1), ".")
        self.assertEqual(str(m2), "x")
    
    def test_Move_4(self):
        """ Move.__repr__ """
        m1 = Move(True)
        m2 = Move(False)
        self.assertEqual(repr(m1), "Move(True)")
        self.assertEqual(repr(m2), "Move(False)")
    
    # eq
    def test_Move_5(self):
        """ Move.__eq__ """
        m1 = Move(True)
        m2 = Move(True)
        m3 = Move(False)
        m4 = Move(False)
        self.assertEqual(m1, m2)
        self.assertNotEqual(m1, m3)
    
    def test_Move_6(self):
        """ Move.__eq__ differences"""
        m1 = Move(True)
        m2 = Move(True)
        m3 = Move(False)
        m4 = Move(False)
        self.assertEqual(m3, m4)
        self.assertNotEqual(m2, m4)
    
    #---------------------------------------------------------------------------
    
    def test_change_1(self):
        """ Move.change """
        m = Move(True)
        self.assertEqual(m.cooperate, True)
        m.change()
        self.assertEqual(m.cooperate, False)
        
    def test_change_2(self):
        """ Move.change, no aliasing"""
        m1 = Move(True)
        m2 = Move(True)
        self.assertEqual(m1.cooperate, True)
        self.assertEqual(m2.cooperate, True)
        m1.change()
        self.assertEqual(m1.cooperate, False)
        # no effect on other Move objects, please.
        self.assertEqual(m2.cooperate, True)
    
    #---------------------------------------------------------------------------
    
    # field check
    def test_copy_1(self):
        """ Move.copy """
        m1 = Move(True)
        m2 = Move(False)
        
        m11 = m1.copy()
        m22 = m2.copy()
        
        self.assertEqual(m11.cooperate, True)
        self.assertEqual(m22.cooperate, False)
    
    # id check
    def test_copy_2(self):
        """ Move.copy, no aliasing"""
        m1 = Move(True)
        m2 = m1.copy()
        self.assertNotEqual(id(m1), id(m2))
    
    ############################################################################
    
    # PlayerException class. 5 tests.
    
    # plain class style tests
    def test_PlayerException_1(self):
        """ PlayerException.__init__ """
        pe1 = PlayerException("message here.")
        pe2 = PlayerException("second message")
        self.assertEqual(pe1.msg, "message here.")
        self.assertEqual(pe2.msg, "second message")
        
    def test_PlayerException_2(self):
        """ PlayerException.__str__ """
        pe = PlayerException("try this")
        self.assertEqual(str(pe),"try this")
        
    def test_PlayerException_3(self):
        """ PlayerException.__repr__ """
        pe = PlayerException("another message")
        self.assertEqual(repr(pe),"PlayerException('another message')")
    
    # canned usages as an exception
    def test_PlayerException_4(self):
        """ PlayerException, raising """
        try:
            raise PlayerException("...")
        except PlayerException:
            return # all good!
        self.fail("if PlayerException were an exception, this line of code wouldn't be reachable.")
    
    def test_PlayerException_5(self):
        """ PlayerException is (Exception) in particular. """
        try:
            raise PlayerException("...")
        except Exception:
            return # all good!
        self.fail("if PlayerException were an Exception type, this line of code wouldn't be reachable.")
        
    
    
    ############################################################################
    
    # Player class. 47 tests.
    # init
    def test_Player_1(self):
        """ Player.__init__ """
        p = Player("friend", 3, [])
        self.assertEqual(p.style, "friend")
        self.assertEqual(p.points, 3)
        self.assertEqual(p.history, [])
    
    def test_Player_2(self):
        """ Player.__init__ non-empty history"""
        p = Player("detective", 0, [Move(True), Move(False), Move(True)])
        self.assertEqual(p.style, "detective")
        self.assertEqual(p.history, [Move(True), Move(False), Move(True)])
    
    def test_Player_3(self):
        """ Player.__init__ defaults"""
        p = Player("grudger")
        self.assertEqual(p.style, "grudger")
        self.assertEqual(p.points, 0)
        self.assertEqual(p.history, [])
        
    def test_Player_4(self):
        """ Player.__init__ default aliasing check"""
        p1 = Player("grudger")
        p1.history.extend( [Move(),Move(),Move()] )
        
        p2 = Player("friend")
        self.assertEqual(p1.history, [Move(),Move(),Move()])
        self.assertEqual(p2.history, [])
    
    
    def test_Player_5(self):
        """ Player.__init__ with bad style """
        try:
            p1 = Player("random") # our project doesn't have them
        except PlayerException as e:
            self.assertEqual(e.msg, "no style 'random'.")
            return
        self.fail("should raise a PlayerException when a bogus style is given.")
    
    # str
    def test_Player_6(self):
        """ Player.__str__ """
        p = Player("friend",6,[])
        self.assertEqual(str(p), "friend(6)")
    
    def test_Player_7(self):
        """ Player.__str__ with history"""
        p = Player("cheater",7,[Move(True), Move(False), Move(False), Move(True)])
        self.assertEqual(str(p), "cheater(7).xx.")
    
    # repr
    def test_Player_8(self):
        """ Player.__repr__ """
        p1 = Player("friend",8,[])
        self.assertEqual(repr(p1), "Player('friend', 8, [])")
        
        p2 = Player("friend",9,[Move(True), Move(False), Move()])
        self.assertEqual(repr(p2), "Player('friend', 9, [Move(True), Move(False), Move(True)])")
    
    #---------------------------------------------------------------------------
    
    def test_reset_history_1(self):
        """ test_reset_history: already empty."""
        p = Player('friend')
        p.reset_history()
        self.assertEqual(p.history,[])
    
    def test_reset_history_2(self):
        """ test_reset_history: nonempty."""
        p = Player('friend',1,[Move(False), Move(True), Move(True)])
        self.assertEqual(p.history,[Move(False), Move(True), Move(True)])
        p.reset_history()
        self.assertEqual(p.history,[])
    
    def test_reset_history_3(self):
        """ test_reset_history: aliasing check."""
        p1 = Player('friend'  , 1, [Move(False), Move(True), Move(True)])
        p2 = Player("previous", 2, [Move(True), Move (False), Move(True)])
        
        self.assertEqual(p1.history,[Move(False), Move(True),  Move(True)])
        self.assertEqual(p2.history,[Move(True),  Move(False), Move(True)])
        p1.reset_history()
        self.assertEqual(p1.history,[])
        # shouldn't affect others' history.
        self.assertEqual(p2.history,[Move(True),  Move(False), Move(True)])
    
    #---------------------------------------------------------------------------
    
    def test_reset_1(self):
        """ reset: changes points. """
        p = Player("friend", 50, [])
        self.assertEqual(p.points, 50)
        p.reset()
        self.assertEqual(p.points, 0)
    
    def test_reset_2(self):
        """ reset: changes history. """
        p = Player("friend", 50, [Move(), Move()])
        self.assertEqual(p.history, [Move(), Move()])
        p.reset()
        self.assertEqual(p.history, [])
    
    def test_reset_3(self):
        """ reset: checking for aliases. """
        p1 = Player("friend", 50, [Move(), Move()])
        p2 = Player("previous", 120, [Move(), Move(),Move(False)])
        
        self.assertEqual(p1.history, [Move(), Move()])
        p1.reset()
        self.assertEqual(p1.history, [])
        
        # make sure p2 didn't get changed at all.
        self.assertEqual(p2.style,"previous")
        self.assertEqual(p2.points, 120)
        self.assertEqual(p2.history, [Move(), Move(),Move(False)])
    
    #---------------------------------------------------------------------------
    
    def test_update_points_1(self):
        """ update_points """
        p = Player("friend", 50)
        p.update_points(3)
        self.assertEqual(p.points, 53)
        
    def test_update_points_2(self):
        """ update_points """
        p = Player("friend", 50)
        p.update_points(0)
        self.assertEqual(p.points, 50)
    
    def test_update_points_3(self):
        """ update_points """
        p = Player("friend", 100)
        p.update_points(-10)
        self.assertEqual(p.points, 90)
    
    #---------------------------------------------------------------------------
    
    def test_ever_betrayed_1(self):
        """ ever_betrayed : empty history"""
        p = Player('friend', 10, [])
        self.assertEqual(p.ever_betrayed(), False)
    
    def test_ever_betrayed_2(self):
        """ ever_betrayed : . """
        p = Player('friend', 10, [Move(True)])
        self.assertEqual(p.ever_betrayed(), False)
    
    def test_ever_betrayed_3(self):
        """ ever_betrayed : x """
        p = Player('friend', 10, [Move(False)])
        self.assertEqual(p.ever_betrayed(), True)
    
    def test_ever_betrayed_4(self):
        """ ever_betrayed : x. """
        p = Player('friend', 10, [Move(False), Move(True)])
        self.assertEqual(p.ever_betrayed(), True)
    
    def test_ever_betrayed_5(self):
        """ ever_betrayed : ..x.. """
        p = Player('friend', 10, [Move(True),  Move(True), Move(False),  Move(True),  Move(True)])
        self.assertEqual(p.ever_betrayed(), True)
    
    def test_ever_betrayed_6(self):
        """ ever_betrayed : xxxxxx """
        p = Player('friend', 10, [Move(False), Move(False), Move(False), Move(False), Move(False)])
        self.assertEqual(p.ever_betrayed(), True)
    
    #---------------------------------------------------------------------------
    
    def test_record_opponent_move_1(self):
        """ record_opponent_move : initially empty """
        p = Player("detective", 100, [])
        self.assertEqual(p.history, [])
        p.record_opponent_move(Move(True))
        self.assertEqual(p.history, [Move(True)])
    
    def test_record_opponent_move_2(self):
        """ record_opponent_move : initially empty """
        p = Player("detective", 100, [])
        self.assertEqual(p.history, [])
        p.record_opponent_move(Move(False))
        self.assertEqual(p.history, [Move(False)])
    
    def test_record_opponent_move_3(self):
        """ record_opponent_move : a couple of calls """
        p = Player("detective", 100, [])
        self.assertEqual(p.history, [])
        p.record_opponent_move(Move(False))
        p.record_opponent_move(Move(True))
        p.record_opponent_move(Move(False))
        self.assertEqual(p.history, [Move(False), Move(True), Move(False)])
    
    def test_record_opponent_move_4(self):
        """ record_opponent_move : adding to existing content """
        p = Player("detective", 100, [Move(True), Move(True)])
        self.assertEqual(p.history, [Move(True), Move(True)])
        p.record_opponent_move(Move(False))
        self.assertEqual(p.history, [Move(True), Move(True), Move(False)])
        p.record_opponent_move(Move(True))
        self.assertEqual(p.history, [Move(True), Move(True), Move(False), Move(True)])
    
    #---------------------------------------------------------------------------
    
    def test_copy_with_style_1(self):
        """ copy_with_style """
        p1 = Player("friend", 1, [Move()])
        p2 = p1.copy_with_style()
        
        self.assertEqual(p2.style, "friend")
        self.assertEqual(p2.points, 0)
        self.assertEqual(p2.history, [])
    
    def test_copy_with_style_2(self):
        """ copy_with_style """
        p1 = Player("detective", 1234, [Move()])
        p2 = p1.copy_with_style()
        
        self.assertEqual(p1.style, "detective")
        self.assertEqual(p1.points, 1234)
        self.assertEqual(p1.history, [Move(True)])
        
        self.assertEqual(p2.style, "detective")
        self.assertEqual(p2.points, 0)
        self.assertEqual(p2.history, [])
    
    def test_copy_with_style_3(self):
        """ copy_with_style : aliasing check"""
        p1 = Player("detective", 1234, [Move()])
        p2 = p1.copy_with_style()
        self.assertNotEqual(id(p1), id(p2))
        self.assertEqual(p2.history, [])
    
    #---------------------------------------------------------------------------
    
    # previous-style
    def test_choose_move_1(self):
        """ Player("previous") - first move"""
        p = Player("previous", 0, [])
        m = p.choose_move()
        self.assertEqual(m, Move(True))
    
    def test_choose_move_2(self):
        """ Player("previous") - second move (.)"""
        p = Player("previous", 0, [Move(True)])
        m = p.choose_move()
        self.assertEqual(m, Move(True))
    
    def test_choose_move_3(self):
        """ Player("previous") - second move (x)"""
        p = Player("previous", 0, [Move(False)])
        m = p.choose_move()
        self.assertEqual(m, Move(False))
    
    def test_choose_move_4(self):
        """ Player("previous") - much history (x..x.)"""
        p = Player("previous", 0, [Move(False), Move(True), Move(True), Move(False), Move(True)])
        m = p.choose_move()
        self.assertEqual(m, Move(True))
    
    def test_choose_move_5(self):
        """ Player("previous") - much history (...xx)"""
        p = Player("previous", 0, [Move(True), Move(True), Move(True), Move(False), Move(False)])
        m = p.choose_move()
        self.assertEqual(m, Move(False))
    
    
    # friend-style
    def test_choose_move_6(self):
        """ Player("friend") - first move"""
        p = Player("friend", 0, [])
        m = p.choose_move()
        self.assertEqual(m, Move(True))
    
    def test_choose_move_7(self):
        """ Player("friend") - second move (.)"""
        p = Player("friend", 0, [Move(True)])
        m = p.choose_move()
        self.assertEqual(m, Move(True))
    
    def test_choose_move_8(self):
        """ Player("friend") - second move (x)"""
        p = Player("friend", 0, [Move(False)])
        m = p.choose_move()
        self.assertEqual(m, Move(True))
    
    def test_choose_move_9(self):
        """ Player("friend") - much history (x.xx.x)"""
        p = Player("friend", 0, [Move(False), Move(True), Move(False), Move(False), Move(True), Move(False)])
        m = p.choose_move()
        self.assertEqual(m, Move(True))
    
    
    # cheater-style
    def test_choose_move_10(self):
        """ Player("cheater") - first move"""
        p = Player("cheater", 0, [])
        m = p.choose_move()
        self.assertEqual(m, Move(False))
    
    def test_choose_move_11(self):
        """ Player("cheater") - second move (.)"""
        p = Player("cheater", 0, [Move(True)])
        m = p.choose_move()
        self.assertEqual(m, Move(False))
    
    def test_choose_move_12(self):
        """ Player("cheater") - second move (x)"""
        p = Player("cheater", 0, [Move(False)])
        m = p.choose_move()
        self.assertEqual(m, Move(False))
    
    def test_choose_move_13(self):
        """ Player("cheater") - much history (x.xx.x)"""
        p = Player("cheater", 0, [Move(False), Move(True), Move(False), Move(False), Move(True), Move(False)])
        m = p.choose_move()
        self.assertEqual(m, Move(False))
    
    
    # grudger-style
    def test_choose_move_14(self):
        """ Player("grudger") - first move"""
        p = Player("grudger", 0, [])
        m = p.choose_move()
        self.assertEqual(m, Move(True))
    
    def test_choose_move_15(self):
        """ Player("grudger") - second move (.)"""
        p = Player("grudger", 0, [Move(True)])
        m = p.choose_move()
        self.assertEqual(m, Move(True))
    
    def test_choose_move_16(self):
        """ Player("grudger") - second move (x)"""
        p = Player("grudger", 0, [Move(False)])
        m = p.choose_move()
        self.assertEqual(m, Move(False))
    
    def test_choose_move_17(self):
        """ Player("grudger") - one betrayal (x..)"""
        p = Player("grudger", 0, [Move(False), Move(True), Move(True)])
        m = p.choose_move()
        self.assertEqual(m, Move(False))
    
    def test_choose_move_18(self):
        """ Player("grudger") - intermittent betrayal (..x.x...)"""
        p = Player("grudger", 0, [Move(True), Move(True), Move(False), Move(True), Move(False), Move(True), Move(True)])
        m = p.choose_move()
        self.assertEqual(m, Move(False))
    
    
    # detective-style
    def test_choose_move_19(self):
        """ Player("detective") - first move"""
        p1 = Player("detective", 0, [])
        m1 = p1.choose_move()
        self.assertEqual(m1, Move(True))
    
    def test_choose_move_19(self):
        """ Player("detective") - second move"""
        p1 = Player("detective", 0, [Move(True)])
        p2 = Player("detective", 0, [Move(False)])
        m1 = p1.choose_move()
        m2 = p2.choose_move()
        
        self.assertEqual(m1, Move(False))
        self.assertEqual(m2, Move(False))
    
    def test_choose_move_20(self):
        """ Player("detective") - third move"""
        p1 = Player("detective", 0, [Move(True),Move(True)])
        p2 = Player("detective", 0, [Move(False),Move(False)])
        m1 = p1.choose_move()
        m2 = p2.choose_move()
        
        self.assertEqual(m1, Move(True))
        self.assertEqual(m2, Move(True))
    
    def test_choose_move_21(self):
        """ Player("detective") - fourth move"""
        p1 = Player("detective", 0, [Move(True),Move(True), Move(True)])
        p2 = Player("detective", 0, [Move(False),Move(False), Move(False)])
        m1 = p1.choose_move()
        m2 = p2.choose_move()
        
        self.assertEqual(m1, Move(True))
        self.assertEqual(m2, Move(True))
    
    def test_choose_move_22(self):
        """ Player("detective") - I choose the 'cheater' life and its consequences"""
        p1 = Player("detective", 0, [Move(True), Move(True), Move(True), Move(True)])
        p2 = Player("detective", 0, [Move(True), Move(True), Move(True), Move(True), Move(True), Move(True), Move(True), Move(True)])
        m1 = p1.choose_move()
        m2 = p2.choose_move()
        
        self.assertEqual(m1, Move(False))
        self.assertEqual(m2, Move(False))
    
    def test_choose_move_23(self):
        """ Player("detective") - I choose the 'previous' life and its consequences"""
        p1 = Player("detective", 0, [Move(False), Move(True),  Move(True),  Move(True) ])
        p2 = Player("detective", 0, [Move(True),  Move(False), Move(True),  Move(True) ])
        p3 = Player("detective", 0, [Move(False), Move(True),  Move(False), Move(True) ])
        p4 = Player("detective", 0, [Move(False), Move(True),  Move(True),  Move(False)])
        m1 = p1.choose_move()
        m2 = p2.choose_move()
        m3 = p3.choose_move()
        m4 = p4.choose_move()
        
        # always choose the previous opponent move.
        self.assertEqual(m1, Move(True))
        self.assertEqual(m2, Move(True))
        self.assertEqual(m3, Move(True))
        self.assertEqual(m4, Move(False))
    
    def test_choose_move_24(self):
        """ Player("detective") - I choose the 'previous' life and its consequences (later edition)"""
        p1 = Player("detective", 0, [Move(False), Move(True),  Move(True),  Move(True) , Move(True), Move(True), Move(True), Move(True)])
        p2 = Player("detective", 0, [Move(False), Move(True),  Move(True),  Move(True) , Move(True), Move(True), Move(True), Move(False)])
        m1 = p1.choose_move()
        m2 = p2.choose_move()
        
        # always choose the previous opponent move.
        self.assertEqual(m1, Move(True))
        self.assertEqual(m2, Move(False))
    
    
    ############################################################################
    
    def test_turn_payouts_1(self):
        """ turn_payouts (..) """
        self.assertEqual(turn_payouts(Move(True), Move(True)), (2,2))

    def test_turn_payouts_2(self):
        """ turn_payouts (xx) """
        self.assertEqual(turn_payouts(Move(False), Move(False)), (0,0))

    def test_turn_payouts_3(self):
        """ turn_payouts (.x) """
        self.assertEqual(turn_payouts(Move(True), Move(False)), (-1,3))

    def test_turn_payouts_4(self):
        """ turn_payouts (x.) """
        self.assertEqual(turn_payouts(Move(False), Move(True)), (3,-1))
    
    #---------------------------------------------------------------------------
    
    def test_build_players_1(self):
        """ build_players - one player """
        ps = build_players("p")
        self.assertEqual(ps[0].style,"previous")
        
        ps = build_players("f")
        self.assertEqual(ps[0].style,"friend")
        
        ps = build_players("c")
        self.assertEqual(ps[0].style,"cheater")
        
        ps = build_players("g")
        self.assertEqual(ps[0].style,"grudger")
        
        ps = build_players("d")
        self.assertEqual(ps[0].style,"detective")
    
    def test_build_players_2(self):
        """ build_players - multiple players"""
        ps = build_players("ppff")
        self.assertEqual(ps[0].style,"previous")
        self.assertEqual(ps[1].style,"previous")
        self.assertEqual(ps[2].style,"friend")
        self.assertEqual(ps[3].style,"friend")
    
    def test_build_players_3(self):
        """ build_players - multiple players, mixed up"""
        ps = build_players("fpfc")
        self.assertEqual(ps[0].style,"friend")
        self.assertEqual(ps[1].style,"previous")
        self.assertEqual(ps[2].style,"friend")
        self.assertEqual(ps[3].style,"cheater")
    
    def test_build_players_4(self):
        """ build_players - bogus initials """
        try:
            build_players("x")
        except PlayerException as e:
            self.assertEqual(e.msg, "no style with initial 'x'.")
            return
        self.fail("should have raised PlayerException due to bogus initial.")
    
    def test_build_players_5(self):
        """ build_players - bogus initials """
        try:
            build_players("ffwf")
        except PlayerException as e:
            self.assertEqual(e.msg, "no style with initial 'w'.")
            return
        self.fail("should have raised PlayerException due to bogus initial.")
    
    #---------------------------------------------------------------------------
    
    def test_composition_1(self):
        """ composition - one of each """
        ps = [Player("friend"), Player("previous"), Player("cheater"), Player("grudger"), Player("detective")]
        c = composition(ps)
        self.assertEqual(c, {'friend':1, 'previous':1, 'cheater':1, 'grudger':1, 'detective':1})
    
    def test_composition_2(self):
        """ composition - some of only one kind"""
        ps = [Player("friend"), Player("friend"), Player("friend")]
        c = composition(ps)
        self.assertEqual(c, {'friend':3})
    
    def test_composition_3(self):
        """ composition - some of a few kinds"""
        ps = [Player("friend"), Player("friend"), Player("friend"), Player("cheater"), Player("previous"), Player("previous")]
        c = composition(ps)
        self.assertEqual(c, {'friend':3, 'cheater':1, 'previous':2})
    
    def test_composition_4(self):
        """ composition - some of a few kinds, mixed up"""
        ps = [Player("friend"), Player("friend"), Player("cheater"), Player("grudger"), Player("friend"), Player("grudger")]
        c = composition(ps)
        self.assertEqual(c, {'friend':3, 'cheater':1, 'grudger':2})
    
    def test_composition_5(self):
        """ composition - empty list"""
        self.assertEqual(composition([]), {})
    
    
    #---------------------------------------------------------------------------
    
    def test_run_turn_1(self):
        """ run_turn -  p vs p, first move"""
        p1 = Player("previous",5, [])
        p2 = Player("previous",5, [])
        
        run_turn(p1, p2)
        
        self.assertEqual(p1.points, 5  -1+2)
        self.assertEqual(p2.points, 5  -1+2)
        
        self.assertEqual(p1.history, [Move(True)])
        self.assertEqual(p2.history, [Move(True)])
    
    def test_run_turn_2(self):
        """ run_turn -  p vs p, later on"""
        p1 = Player("previous",5, [Move(),Move(),Move()])
        p2 = Player("previous",5, [Move(),Move(),Move()])
        
        run_turn(p1, p2)
        
        self.assertEqual(p1.points, 5  -1+2)
        self.assertEqual(p2.points, 5  -1+2)
        
        self.assertEqual(p1.history, [Move(),Move(),Move(),Move()]) # added the 4th?
        self.assertEqual(p2.history, [Move(),Move(),Move(),Move()]) # added the 4th?
    
    def test_run_turn_3(self):
        """ run_turn -  p vs d, no moves yet"""
        p1 = Player("previous",5, [])
        p2 = Player("detective",5, [])
        
        run_turn(p1, p2)
        
        self.assertEqual(p1.points, 5  -1+2)
        self.assertEqual(p2.points, 5  -1+2)
        
        self.assertEqual(p1.history, [Move(True)])
        self.assertEqual(p2.history, [Move(True)])
        
    def test_run_turn_4(self):
        """ run_turn -  p vs d, d's cheat move"""
        p1 = Player("previous", 10, [Move()])
        p2 = Player("detective",10, [Move()])
        
        run_turn(p1, p2)
        
        self.assertEqual(p1.points, 10  -1-1)
        self.assertEqual(p2.points, 10  -1+3)
        
        self.assertEqual(p1.history, [Move(), Move(False)])
        self.assertEqual(p2.history, [Move(), Move()])
    
    def test_run_turn_5(self):
        """ run_turn -  p vs d, after d's cheat move"""
        p1 = Player("previous", 10, [Move(), Move(False)])
        p2 = Player("detective",10, [Move(), Move()])
        
        run_turn(p1, p2)
        
        self.assertEqual(p1.points, 10  -1+3)
        self.assertEqual(p2.points, 10  -1-1)
        
        self.assertEqual(p1.history, [Move(), Move(False), Move()])
        self.assertEqual(p2.history, [Move(), Move(), Move(False)])
    
    def test_run_turn_6(self):
        """ run_turn -  f vs f"""
        p1 = Player("friend", 20, [])
        p2 = Player("friend", 20, [])
        
        run_turn(p1, p2)
        self.assertEqual(p1.points, 20  -1+2)
        self.assertEqual(p2.points, 20  -1+2)
        
        self.assertEqual(p1.history, [Move()])
        self.assertEqual(p2.history, [Move()])
        
        run_turn(p1, p2)
        self.assertEqual(p1.points, 20  -1+2  -1+2)
        self.assertEqual(p2.points, 20  -1+2  -1+2)
        
        self.assertEqual(p1.history, [Move(),Move()])
        self.assertEqual(p2.history, [Move(),Move()])
    
    def test_run_turn_7(self):
        """ run_turn - players witih same id's, should raise exception. """
        
        p1 = Player("friend", 30, [])
        try:
            run_turn(p1, p1)
        except PlayerException as e:
            self.assertEqual(e.msg, "players must be distinct.")
            return
        self.fail("run_turn must look out for players being the same object and raise an exception.")
        
#         self.assertEqual(p1.points, 30  -1+0)
#         self.assertEqual(p2.points, 30  -1+0)
#         
#         self.assertEqual(p1.history, [Move(False)])
#         self.assertEqual(p2.history, [Move(False)])
#         
#         run_turn(p1, p2)
#         self.assertEqual(p1.points, 30  -1+0  -1+0)
#         self.assertEqual(p2.points, 30  -1+0  -1+0)
#         
#         self.assertEqual(p1.history, [Move(False),Move(False)])
#         self.assertEqual(p2.history, [Move(False),Move(False)])
    
    def test_run_turn_8(self):
        """ run_turn -  c vs f"""
        p1 = Player("cheater", 40, [])
        p2 = Player("friend",  40, [])
        
        run_turn(p1, p2)
        self.assertEqual(p1.points, 40  -1+3)
        self.assertEqual(p2.points, 40  -1-1)
        
        self.assertEqual(p1.history, [Move()])
        self.assertEqual(p2.history, [Move(False)])
        
        run_turn(p1, p2)
        self.assertEqual(p1.points, 40  -1+3  -1+3)
        self.assertEqual(p2.points, 40  -1-1  -1-1)
        
        self.assertEqual(p1.history, [Move(),Move()])
        self.assertEqual(p2.history, [Move(False),Move(False)])
    
    def test_run_turn_9(self):
        """ run_turn -  f vs c"""
        p1 = Player("friend",  40, [])
        p2 = Player("cheater", 40, [])
        
        run_turn(p1, p2)
        self.assertEqual(p1.points, 40  -1-1)
        self.assertEqual(p2.points, 40  -1+3)
        
        self.assertEqual(p1.history, [Move(False)])
        self.assertEqual(p2.history, [Move()])
        
        run_turn(p1, p2)
        self.assertEqual(p1.points, 40  -1-1  -1-1)
        self.assertEqual(p2.points, 40  -1+3  -1+3)
        
        self.assertEqual(p1.history, [Move(False),Move(False)])
        self.assertEqual(p2.history, [Move(),Move()])
    
    def test_run_turn_10(self):
        """ run_turn -  g vs g, starting with a cheat move present."""
        p1 = Player("grudger", 50, [Move(True )])
        p2 = Player("grudger", 50, [Move(False)])
        
        # p1 has no grudge yet. p2 does.
        # so p1 cooperates, p2 cheats.
        run_turn(p1, p2)
        self.assertEqual(p1.points, 50  -1-1)
        self.assertEqual(p2.points, 50  -1+3)
        
        self.assertEqual(p1.history, [Move(True ), Move(False)])
        self.assertEqual(p2.history, [Move(False), Move(True )])
        
        # now they both have grudges.
        # Both cheat, and everybody loses out.
        run_turn(p1, p2)
        self.assertEqual(p1.points, 50  -1-1  -1+0)
        self.assertEqual(p2.points, 50  -1+3  -1+0)
        
        self.assertEqual(p1.history, [Move(True ), Move(False), Move(False)])
        self.assertEqual(p2.history, [Move(False), Move(True ), Move(False)])
    
    #---------------------------------------------------------------------------
    
    def test_run_game_1(self):
        """ run_game - c vs f, one turn"""
        c = Player("cheater",0,[])
        f = Player("friend" ,0,[])
        run_game(c,f,num_turns=1)
        self.assertEqual(c.history,[Move(True )])
        self.assertEqual(f.history,[Move(False)])
        self.assertEqual(c.points, 0+(-1+3))
        self.assertEqual(f.points, 0+(-1-1))
    
    def test_run_game_2(self):
        """ run_game - c vs f, five turns"""
        c = Player("cheater",0,[])
        f = Player("friend" ,0,[])
        run_game(c,f) # 5 turns by default
        self.assertEqual(c.history,[Move(True )]*5)
        self.assertEqual(f.history,[Move(False)]*5)
        self.assertEqual(c.points, 0+(-1+3)*5)
        self.assertEqual(f.points, 0+(-1-1)*5)
    
    def test_run_game_3(self):
        """ run_game - p vs p, with history (gets reset first)"""
        p1 = Player("previous",10,[Move(),Move(),Move()])
        p2 = Player("previous",10,[Move(),Move(),Move()])
        run_game(p1,p2,num_turns=2)
        # only the five 
        self.assertEqual(p1.history,[Move(),Move()])
        self.assertEqual(p2.history,[Move(),Move()])
        self.assertEqual(p1.points, 10+(-1+2)*2)
        self.assertEqual(p2.points, 10+(-1+2)*2)
    
    def test_run_game_4(self):
        """ run_game - f vs f, 100 turns """
        c = Player("cheater",50,[])
        f = Player("friend" ,50,[])
        run_game(c,f,100)
        self.assertEqual(c.history,[Move(True )]*100)
        self.assertEqual(f.history,[Move(False)]*100)
        self.assertEqual(c.points, 50 + (-1+3)*100)
        self.assertEqual(f.points, 50 + (-1-1)*100)
    
    def test_run_game_5(self):
        """ run_game - c vs g, ten turns"""
        c = Player("cheater",25,[])
        f = Player("grudger",25,[])
        run_game(c,f,10)
        self.assertEqual(c.history,[Move(True )]+[Move(False)]*9)
        self.assertEqual(f.history,[Move(False)]*10)
        self.assertEqual(c.points, 25 + (-1+3) + (-1+0)*9)
        self.assertEqual(f.points, 25 + (-1-1) + (-1+0)*9)
    
    def test_run_game_6(self):
        """ run_game - same player (handle the exception)"""
        f = Player("friend",30,[])
        # if this next call throws an exception, you'll fail the test directly as a result.
        run_game(f,f)
        self.assertEqual(f.history,[])
        self.assertEqual(f.points, 30)
    
    #---------------------------------------------------------------------------
    
    def test_run_tournament_1(self):
        """ run_tournament - one each (10 turns, 1 rounds, 0 pts, 1 replacement) """
        # replace friend with previous.
        c = run_tournament(build_players("pfcgd"), 10, 1, 0, 1)
        self.assertEqual(c, {'previous':2, 'cheater':1, 'detective':1, 'grudger':1})
        
    def test_run_tournament_2(self):
        """ run_tournament - one each (10 turns, 2 rounds, 0 pts, 1 replacement)"""
        # replace friend with previous
        # replace cheater with previous, also the detective dies (negative score)
        c = run_tournament(build_players(("f"*15)+("c"*5)+("p"*5)), 10, 4, 1000, 5)
        self.assertEqual(c, {'previous':10, 'cheater':15})
        
    def test_run_tournament_3(self):
        """ run_tournament - two each  (10 turns, 3 rounds, 1000 pts, 1 replacement)"""
        # replace friend  with previous
        # replace cheater with previous
        # replace cheater with previous
        # high scores mean nobody was dropped for going negative.
        c = run_tournament(build_players("pfcgd"*2), 10, 3, 1000, 1)
        self.assertEqual(c, {'previous':5, 'friend':1, 'detective':2, 'grudger':2})
        
    def test_run_tournament_4(self):
        """ run_tournament - 15f, 5c, 5p (10 turns, 3 rounds, 1000 pts, 5 replaces)"""
        # replace 5 friends  with 5 cheaters
        # replace 5 friends  with 5 cheaters
        # replace 5 friends  with 5 cheaters
        c = run_tournament(build_players(("f"*15)+("c"*5)+("p"*5)), 10, 3, 1000, 5)
        self.assertEqual(c, {'previous':5, 'cheater':20})
        
    def test_run_tournament_5(self):
        """ run_tournament - 15f, 5c, 5p (10 turns, 4 rounds, 1000 pts, 5 replaces)"""
        # replace 5 friends  with 5 cheaters
        # replace 5 friends  with 5 cheaters
        # replace 5 friends  with 5 cheaters
        # replace 5 cheaters with 5 previouses
        c = run_tournament(build_players(("f"*15)+("c"*5)+("p"*5)), 10, 4, 1000, 5)
        self.assertEqual(c, {'previous':10, 'cheater':15})
        
    def test_run_tournament_6(self):
        """ run_tournament - 15f, 5p, 5c (10 turns, 7 rounds, 1000 pts, 5 replaces)"""
        # replace 5 friends  with 5 cheaters
        # replace 5 friends  with 5 cheaters
        # replace 5 friends  with 5 cheaters
        # replace 5 cheaters with 5 previouses
        # replace 5 cheaters with 5 previouses
        # replace 5 cheaters with 5 previouses
        # replace 5 cheaters with 5 previouses
        c = run_tournament(build_players(("f"*15)+("c"*5)+("p"*5)), 10, 4, 1000, 5)
        self.assertEqual(c, {'previous':10, 'cheater':15})
        
       
    #---------------------------------------------------------------------------
    
    ############################################################################
    ############################################################################

# This class digs through AllTests, counts and builds all the tests,
# so that we have an entire test suite that can be run as a group.
class TheTestSuite (unittest.TestSuite):
    # constructor.
    def __init__(self,wants):
        self.num_req = 0
        self.num_ec = 0
        # find all methods that begin with "test".
        fs = []
        for w in wants:
            for func in AllTests.__dict__:
                # append regular tests
                # drop any digits from the end of str(func).
                dropnum = str(func)
                while dropnum[-1] in "1234567890":
                    dropnum = dropnum[:-1]
                
                if dropnum==("test_"+w+"_") and (not (dropnum==("test_extra_credit_"+w+"_"))):
                    fs.append(AllTests(str(func)))
                if dropnum==("test_extra_credit_"+w+"_") and not BATCH_MODE:
                    fs.append(AllTests(str(func)))
        
#       print("TTS ====> ",list(map(lambda f: (f,id(f)),fs)))
        # call parent class's constructor.
        unittest.TestSuite.__init__(self,fs)

class TheExtraCreditTestSuite (unittest.TestSuite):
        # constructor.
        def __init__(self,wants):
            # find all methods that begin with "test_extra_credit_".
            fs = []
            for w in wants:
                for func in AllTests.__dict__:
                    if str(func).startswith("test_extra_credit_"+w):
                        fs.append(AllTests(str(func)))
        
#           print("TTS ====> ",list(map(lambda f: (f,id(f)),fs)))
            # call parent class's constructor.
            unittest.TestSuite.__init__(self,fs)

# all (non-directory) file names, regardless of folder depth,
# under the given directory 'dir'.
def files_list(dir):
    this_file = __file__
    if dir==".":
        dir = os.getcwd()
    info = os.walk(dir)
    filenames = []
    for (dirpath,dirnames,filez) in info:
#       print(dirpath,dirnames,filez)
        if dirpath==".":
            continue
        for file in filez:
            if file==this_file:
                continue
            filenames.append(os.path.join(dirpath,file))
#       print(dirpath,dirnames,filez,"\n")
    return filenames

def main():
    if len(sys.argv)<2:
        raise Exception("needed student's file name as command-line argument:"\
            +"\n\t\"python3 testerX.py gmason76_2xx_Px.py\"")
    
    if BATCH_MODE:
        print("BATCH MODE.\n")
        run_all()
        return
        
    else:
        want_all = len(sys.argv) <=2
        wants = []
        # remove batch_mode signifiers from want-candidates.
        want_candidates = sys.argv[2:]
        for i in range(len(want_candidates)-1,-1,-1):
            if want_candidates[i] in ['.'] or os.path.isdir(want_candidates[i]):
                del want_candidates[i]
    
        # set wants and extra_credits to either be the lists of things they want, or all of them when unspecified.
        wants = []
        extra_credits = []
        if not want_all:
            for w in want_candidates:
                if w in REQUIRED_DEFNS:
                    wants.append(w)
                elif w in SUB_DEFNS:
                    wants.append(w)
                elif w in EXTRA_CREDIT_DEFNS:
                    extra_credits.append(w)
                else:
                    raise Exception("asked to limit testing to unknown function '%s'."%w)
        else:
            wants = REQUIRED_DEFNS + SUB_DEFNS
            extra_credits = EXTRA_CREDIT_DEFNS
        
        # now that we have parsed the function names to test, run this one file.    
        run_one(wants,extra_credits)    
        return
    return # should be unreachable! 

# only used for non-batch mode, since it does the printing.
# it nicely prints less info when no extra credit was attempted.
def run_one(wants, extra_credits):
    
    has_reqs = len(wants)>0
    has_ec   = len(extra_credits)>0
    
    # make sure they exist.
    passed1 = 0
    passed2 = 0
    tried1 = 0
    tried2 = 0
    
    # only run tests if needed.
    if has_reqs:
        print("\nRunning required definitions:")
        (tag, passed1,tried1) = run_file(sys.argv[1],wants,False)
    if has_ec:
        print("\nRunning extra credit definitions:")
        (tag, passed2,tried2) = run_file(sys.argv[1],extra_credits,True)
    
    # print output based on what we ran.
    if has_reqs and not has_ec:
        print("\n%d/%d Required test cases passed (worth %.1f each)" % (passed1,tried1,weight_required) )
        print("\nScore based on test cases: %.2f/%d (%.2f*%.1f) " % (
                                                                passed1*weight_required, 
                                                                total_points_from_tests,
                                                                passed1,
                                                                weight_required
                                                             ))
    elif has_ec and not has_reqs:
        print("%d/%d Extra credit test cases passed (worth %d each)" % (passed2, tried2, weight_extra_credit))
    else: # has both, we assume.
        print("\n%d / %d Required test cases passed (worth %d each)" % (passed1,tried1,weight_required) )
        print("%d / %d Extra credit test cases passed (worth %d each)" % (passed2, tried2, weight_extra_credit))
        print("\nScore based on test cases: %.2f / %d ( %d * %d + %d * %d) " % (
                                                                passed1*weight_required+passed2*weight_extra_credit, 
                                                                total_points_from_tests,
                                                                passed1,
                                                                weight_required,
                                                                passed2,
                                                                weight_extra_credit
                                                             ))
    if CURRENTLY_GRADING:
        print("( %d %d %d %d )\n%s" % (passed1,tried1,passed2,tried2,tag))

# only used for batch mode.
def run_all():
        filenames = files_list(sys.argv[1])
        #print(filenames)
        
        wants = REQUIRED_DEFNS + SUB_DEFNS
        extra_credits = EXTRA_CREDIT_DEFNS
        
        results = []
        for filename in filenames:
            print(" Batching on : " +filename)
            # I'd like to use subprocess here, but I can't get it to give me the output when there's an error code returned... TODO for sure.
            lines = os.popen("python3 tester1p.py \""+filename+"\"").readlines()
            
            # delay of shame...
            time.sleep(DELAY_OF_SHAME)
            
            name = os.path.basename(lines[-1])
            stuff =lines[-2].split(" ")[1:-1]
            print("STUFF: ",stuff, "LINES: ", lines)
            (passed_req, tried_req, passed_ec, tried_ec) = stuff
            results.append((lines[-1],int(passed_req), int(tried_req), int(passed_ec), int(tried_ec)))
            continue
        
        print("\n\n\nGRAND RESULTS:\n")
        
            
        for (tag_req, passed_req, tried_req, passed_ec, tried_ec) in results:
            name = os.path.basename(tag_req).strip()
            earned   = passed_req*weight_required + passed_ec*weight_extra_credit
            possible = tried_req *weight_required # + tried_ec *weight_extra_credit
            print("%10s : %3d / %3d = %5.2d %% (%d/%d*%d + %d/%d*%d)" % (
                                                            name,
                                                            earned,
                                                            possible, 
                                                            (earned/possible)*100,
                                                            passed_req,tried_req,weight_required,
                                                            passed_ec,tried_ec,weight_extra_credit
                                                          ))
# only used for batch mode.
def run_all_orig():
        filenames = files_list(sys.argv[1])
        #print(filenames)
        
        wants = REQUIRED_DEFNS + SUB_DEFNS
        extra_credits = EXTRA_CREDIT_DEFNS
        
        results = []
        for filename in filenames:
            # wipe out all definitions between users.
            for fn in REQUIRED_DEFNS+EXTRA_CREDIT_DEFNS :
                globals()[fn] = decoy(fn)
                fn = decoy(fn)
            try:
                name = os.path.basename(filename)
                print("\n\n\nRUNNING: "+name)
                (tag_req, passed_req, tried_req) = run_file(filename,wants,False)
                (tag_ec,  passed_ec,  tried_ec ) = run_file(filename,extra_credits,True)
                results.append((tag_req,passed_req,tried_req,tag_ec,passed_ec,tried_ec))
                print(" ###### ", results)
            except SyntaxError as e:
                tag = filename+"_SYNTAX_ERROR"
                results.append((tag,0,len(wants),tag,0,len(extra_credits)))
            except NameError as e:
                tag =filename+"_Name_ERROR"
                results.append((tag,0,len(wants),tag,0,len(extra_credits)))
            except ValueError as e:
                tag = filename+"_VALUE_ERROR"
                results.append((tag,0,len(wants),tag,0,len(extra_credits)))
            except TypeError as e:
                tag = filename+"_TYPE_ERROR"
                results.append((tag,0,len(wants),tag,0,len(extra_credits)))
            except ImportError as e:
                tag = filename+"_IMPORT_ERROR_TRY_AGAIN"
                results.append((tag,0,len(wants),tag,0,len(extra_credits)))
            except Exception as e:
                tag = filename+str(e.__reduce__()[0])
                results.append((tag,0,len(wants),tag,0,len(extra_credits)))
        
#           try:
#               print("\n |||||||||| scrupe: "+str(scruples))
#           except Exception as e:
#               print("NO SCRUPE.",e)
#           scruples = None
        
        print("\n\n\nGRAND RESULTS:\n")
        for (tag_req, passed_req, tried_req, tag_ec, passed_ec, tried_ec) in results:
            name = os.path.basename(tag_req)
            earned   = passed_req*weight_required + passed_ec*weight_extra_credit
            possible = tried_req *weight_required # + tried_ec *weight_extra_credit
            print("%10s : %3d / %3d = %5.2d %% (%d/%d*%d + %d/%d*%d)" % (
                                                            name,
                                                            earned,
                                                            possible, 
                                                            (earned/possible)*100,
                                                            passed_req,tried_req,weight_required,
                                                            passed_ec,tried_ec,weight_extra_credit
                                                          ))

def try_copy(filename1, filename2, numTries):
    have_copy = False
    i = 0
    while (not have_copy) and (i < numTries):
        try:
            # move the student's code to a valid file.
            shutil.copy(filename1,filename2)
            
            # wait for file I/O to catch up...
            if(not wait_for_access(filename2, numTries)):
                return False
                
            have_copy = True
        except PermissionError:
            print("Trying to copy "+filename1+", may be locked...")
            i += 1
            time.sleep(1)
        except BaseException as e:
            print("\n\n\n\n\n\ntry-copy saw: "+e)
    
    if(i == numTries):
        return False
    return True

def try_remove(filename, numTries):
    removed = False
    i = 0
    while os.path.exists(filename) and (not removed) and (i < numTries):
        try:
            os.remove(filename)
            removed = True
        except OSError:
            print("Trying to remove "+filename+", may be locked...")
            i += 1
            time.sleep(1)
    if(i == numTries):
        return False
    return True

def wait_for_access(filename, numTries):
    i = 0
    while (not os.path.exists(filename) or not os.access(filename, os.R_OK)) and i < numTries:
        print("Waiting for access to "+filename+", may be locked...")
        time.sleep(1)
        i += 1
    if(i == numTries):
        return False
    return True

# this will group all the tests together, prepare them as 
# a test suite, and run them.
def run_file(filename,wants=None,checking_ec = False):
    if wants==None:
        wants = []
    
    # move the student's code to a valid file.
    if(not try_copy(filename,"student.py", 5)):
        print("Failed to copy " + filename + " to student.py.")
        quit()
        
    # import student's code, and *only* copy over the expected functions
    # for later use.
    import importlib
    count = 0
    while True:
        try:
#           print("\n\n\nbegin attempt:")
            while True:
                try:
                    f = open("student.py","a")
                    f.close()
                    break
                except:
                    pass
#           print ("\n\nSUCCESS!")
                
            import student
            importlib.reload(student)
            break
        except ImportError as e:
            print("import error getting student... trying again. "+os.getcwd(), os.path.exists("student.py"),e)
            time.sleep(0.5)
            while not os.path.exists("student.py"):
                time.sleep(0.5)
            count+=1
            if count>3:
                raise ImportError("too many attempts at importing!")
        except SyntaxError as e:
            print("SyntaxError in "+filename+":\n"+str(e))
            print("Run your file without the tester to see the details")
            return(filename+"_SYNTAX_ERROR",None, None, None)
        except NameError as e:
            print("NameError in "+filename+":\n"+str(e))
            print("Run your file without the tester to see the details")
            return((filename+"_Name_ERROR",0,1))    
        except ValueError as e:
            print("ValueError in "+filename+":\n"+str(e))
            print("Run your file without the tester to see the details")
            return(filename+"_VALUE_ERROR",0,1)
        except TypeError as e:
            print("TypeError in "+filename+":\n"+str(e))
            print("Run your file without the tester to see the details")
            return(filename+"_TYPE_ERROR",0,1)
        except ImportError as e:            
            print("ImportError in "+filename+":\n"+str(e))
            print("Run your file without the tester to see the details or try again")
            return((filename+"_IMPORT_ERROR_TRY_AGAIN   ",0,1)) 
        except Exception as e:
            print("Exception in loading"+filename+":\n"+str(e))
            print("Run your file without the tester to see the details")
            return(filename+str(e.__reduce__()[0]),0,1)
    
    # make a global for each expected definition.
    for fn in REQUIRED_DEFNS+EXTRA_CREDIT_DEFNS :
        globals()[fn] = decoy(fn)
        try:
            globals()[fn] = getattr(student,fn)
        except:
            if fn in wants:
                print("\nNO DEFINITION FOR '%s'." % fn) 
    
    if not checking_ec:
        # create an object that can run tests.
        runner = unittest.TextTestRunner()
    
        # define the suite of tests that should be run.
        suite = TheTestSuite(wants)
    
    
        # let the runner run the suite of tests.
        ans = runner.run(suite)
        num_errors   = len(ans.__dict__['errors'])
        num_failures = len(ans.__dict__['failures'])
        num_tests    = ans.__dict__['testsRun']
        num_passed   = num_tests - num_errors - num_failures
        # print(ans)
    
    else:
        # do the same for the extra credit.
        runner = unittest.TextTestRunner()
        suite = TheExtraCreditTestSuite(wants)
        ans = runner.run(suite)
        num_errors   = len(ans.__dict__['errors'])
        num_failures = len(ans.__dict__['failures'])
        num_tests    = ans.__dict__['testsRun']
        num_passed   = num_tests - num_errors - num_failures
        #print(ans)
    
    # remove our temporary file.
    os.remove("student.py")
    if os.path.exists("__pycache__"):
        shutil.rmtree("__pycache__")
    if(not try_remove("student.py", 5)):
        print("Failed to remove " + filename + " to student.py.")
    
    tag = ".".join(filename.split(".")[:-1])
    
    
    return (tag, num_passed, num_tests)


# make a global for each expected definition.
def decoy(name):
        # this can accept any kind/amount of args, and will print a helpful message.
        def failyfail(*args, **kwargs):
            return ("<no '%s' definition was found - missing, or typo perhaps?>" % name)
        return failyfail

# this determines if we were imported (not __main__) or not;
# when we are the one file being run, perform the tests! :)
if __name__ == "__main__":
    main()

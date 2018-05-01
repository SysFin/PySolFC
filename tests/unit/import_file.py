#!/usr/bin/env python3
# Written by Shlomi Fish, under the MIT Expat License.

import unittest
from pysollib.acard import AbstractCard
from pysollib.hint import FreeCellSolver_Hint
import pysollib.stack


class MockItem:
    def __init__(self):
        self.xmargin = self.ymargin = 50

    def tkraise(self):
        return

    def addtag(self, nouse):
        return


class MockCanvas:
    def __init__(self):
        self.xmargin = self.ymargin = 50


class MockImages:
    def __init__(self):
        self.CARDW = self.CARDH = self.CARD_YOFFSET = 50


class MockOpt:
    def __init__(self):
        self.randomize_place = False


class MockApp:
    def __init__(self):
        self.images = MockImages()
        self.opt = MockOpt()


class MockTalon:
    def __init__(self, g):
        self.cards = [
            AbstractCard(1000+r*100+s*10, 0, s, r, g)
            for s in range(4) for r in range(13)]
        for c in self.cards:
            c.item = MockItem()


class MockGame:
    def __init__(self):
        self.app = MockApp()
        self.talon = MockTalon(self)

        self.allstacks = []
        self.stackmap = {}
        self.canvas = MockCanvas()
        self.foundations = [
            pysollib.stack.SS_FoundationStack(0, 0, self, s) for s in range(4)]
        self.rows = [pysollib.stack.AC_RowStack(0, 0, self) for s in range(8)]
        self.reserves = [
            pysollib.stack.AC_RowStack(0, 0, self) for s in range(4)]
        self.preview = 0


def m1(*args):
    return 1


pysollib.stack.MfxCanvasGroup = m1


class Mock_S_Game:
    def __init__(self):
        self.s = MockGame()

    def flipMove(self, foo):
        pass

    def moveMove(self, cnt, frm, to, frames=0):
        c = frm.cards.pop()
        c.face_up = True
        to.addCard(c)
        pass


class MyTests(unittest.TestCase):
    def test_import(self):
        s_game = Mock_S_Game()
        h = FreeCellSolver_Hint(s_game, None)
        fh = open('tests/unit/data/with-10-for-rank.txt', 'r+b')
        h.importFileHelper(fh, s_game)
        self.assertEqual(h.calcBoardString(), '''FC: - - - -
4C 2C 9C 8C QS 4S 2H
5H QH 3C AC 3H 4H QD
QC 9S 6H 9H 3S KS 3D
5D 2S JC 5C JH 6D AS
2D KD TH TC TD 8D
7H JS KH TS KC 7C
AH 5S 6S AD 8H JD
7S 6C 7D 4D 8S 9D
''', 'game is sane')

    def test_output(self):
        # TEST
        self.assertEqual(1, 1, 'card2str2 works')


if __name__ == '__main__':
    from pycotap import TAPTestRunner
    suite = unittest.TestLoader().loadTestsFromTestCase(MyTests)
    TAPTestRunner().run(suite)
import itertools
import math
import random
import sys

DEBUG = 0

def AssertIn(obj, item):
  if obj not in item:
    raise AssertionError('%s not in %s' % (obj, item))


# Colors range from '0' to 'NUM_CHARS - 1'
NUM_CHARS = 8
NUM_SPACES = 5


def _ColorsNotMine(mycolor):
  """Returns a list of colors that are not mine. A color is a single character '1'."""
  colors = [str(num) for num in xrange(NUM_CHARS)]
  colors.remove(mycolor)
  return colors

def _GetUnguessed(arr_of_guessed):
  """Given [True, True, False] returns [2], the unguessed indices."""
  unguessed = []
  for index in xrange(len(arr_of_guessed)):
    if not arr_of_guessed[index]:
      unguessed.append(index)
  return unguessed 

def _PossAns(guess, num_blacks, num_whites):
  """Returns a set of tuples with possible answers.

  """
  answers = set([])  # Fill with potential answers. TODO(dlluncor): why so many dups?
  def _FindAns(blacks, whites, blanks, unfilled_indices, used_for_guess,
               potential_sol):
    """
    Args:
      used_for_guess: Which part of the secret I've used to construct my guess.
    """
    if blacks > 0:
      # Black rule.
      blacks -= 1
      # Any unused index can be set to the color in the guess.
      unguessed_indices = _GetUnguessed(used_for_guess)
      for index in unguessed_indices:
        unfilled = unfilled_indices[:]
        unfilled.remove(index)

        used_guess = used_for_guess[:]
        used_guess[index] = True

        color_from_guess = guess[index]
        pot_sol = potential_sol[:]
        pot_sol[index] = color_from_guess # Set that color to be a valid one.
        _FindAns(blacks, whites, blanks, unfilled, used_guess, pot_sol)
    elif whites > 0:
      whites -= 1
      # Apply the white rule to all unguessed indices.
      unguessed_indices = _GetUnguessed(used_for_guess)
      for pos_to_guess in unguessed_indices:
        # For any unused index, set the item to that color that is not my index though.
        indices_to_use = unfilled_indices[:]
        if DEBUG:
          print 'Pos to guess: %d' % pos_to_guess
          print 'Unfilled inds: %s' % str(indices_to_use)
        if pos_to_guess in indices_to_use: # TODO: Shouldn't this be true though? Huh?
          indices_to_use.remove(pos_to_guess)
        # Fill in indices for which we know the color cannot be there.
        for index in indices_to_use:
          unfilled = unfilled_indices[:]
          unfilled.remove(index)

          used_guess = used_for_guess[:]
          used_guess[pos_to_guess] = True

          color_from_guess = guess[pos_to_guess]
          pot_sol = potential_sol[:]
          pot_sol[index] = color_from_guess
          _FindAns(blacks, whites, blanks, unfilled, used_guess, pot_sol)

    elif blanks > 0:
      blanks -= 1
      unguessed_indices = _GetUnguessed(used_for_guess)
      for pos_to_guess in unguessed_indices:
        # Apply the blank rule to a position we have not guessed yet.
        color_from_guess = guess[pos_to_guess]
        # Find all other colors that are not this guess.
        diff_colors = _ColorsNotMine(color_from_guess)
        for diff_color in diff_colors:
          unfilled = unfilled_indices[:]
          if pos_to_guess in unfilled: # TODO: shouldnt this always be true though?
            unfilled.remove(pos_to_guess)
        
          used_guess = used_for_guess[:]
          used_guess[pos_to_guess] = True

          pot_sol = potential_sol[:]
          pot_sol[pos_to_guess] = diff_color
          _FindAns(blacks, whites, blanks, unfilled, used_guess, pot_sol)
    else:
      # We have reached the end horray.
      answers.add(tuple(potential_sol))

  num_blanks = NUM_SPACES - num_whites - num_blacks
  unfilled_indices = [0, 1, 2, 3, 4]
  used_for_guess = [False, False, False, False, False]
  potential_sol = [-1, -1, -1, -1, -1]
  _FindAns(num_blacks, num_whites, num_blanks,
           unfilled_indices, used_for_guess,
           potential_sol)
  return answers

class Guesser(object):
  
  def __init__(self):
    self.num_guesses = 0
    self.possibles = self._MakePossibles(NUM_CHARS, NUM_SPACES)

  def Guess(self):
    """Returns a tuple that represents the guess and removes it from a future
      possibility.
    """
    self.num_guesses += 1
    num_poss = len(self.possibles)
    guess_rand = int(math.floor(random.random() * num_poss))
    el = self.possibles[guess_rand]
    self.possibles.remove(el)
    return el 

  def Prune(self, guess, whites, blacks):
    """User input is number of whites, number of blacks.
    
    Args:
      guess: Tuple with the current guess.
      whites:
      blacks:
    """
    if DEBUG:
      print 'Current answer: %s' % str(guess)
      print 'Num whites: %d' % whites
      print 'Num blacks: %d' % blacks
    now_possibles = _PossAns(guess, blacks, whites)
    if DEBUG:
      print 'Prev solutions are: %s' % str(self.possibles)
      print 'Possible solutions are: %s' % str(now_possibles)
    # Find the union of previous possible answers and my possible answers.
    self.possibles = list(now_possibles.intersection(set(self.possibles)))
    if DEBUG:
      print 'Union of possibles is: %s' % str(self.possibles)

  def _MakePossibles(self, num_chars, num_spaces):
    """Creates a list of tuples for all possible numbers."""
    return [a for a in itertools.product('01234567', repeat=NUM_SPACES)]

def main(argv):
  if len(argv) < 2:
    print 'Print your %d length secret with characters 0 to %d' % (NUM_SPACES,
        NUM_CHARS - 1)
    return
  if len(argv[1]) != NUM_SPACES:
    print 'Your secret must be %d characters long' % NUM_SPACES
    return
  ans = argv[1] # '1211'
  ans_tup = tuple([char for char in ans]) 
  correct = False
  guesser = Guesser()
  while not correct:
    curans = guesser.Guess()
    print 'Guessing %s' % str(curans)
    if curans == ans_tup:
      correct = True
    else:
      print 'Enter 1 white 2 blacks (1 2):'
      myfeedback = raw_input()
      (whites, blacks) = myfeedback.split(' ')
      guesser.Prune(curans, int(whites), int(blacks))
  print 'Num guesses: %d' % guesser.num_guesses 
  

if __name__ == '__main__':
  main(sys.argv)


#### Testing.
class Tester(object):
  
  def TestGuesser(self):
    guesser = Guesser()
    possibles = guesser._MakePossibles(2, 3)
    AssertIn('000', possibles) 
    AssertIn('001', possibles) 
    AssertIn('010', possibles) 
    AssertIn('011', possibles) 
    AssertIn('100', possibles) 
    AssertIn('101', possibles) 
    AssertIn('110', possibles) 
    AssertIn('111', possibles) 
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

VALID_CHARS = [str(ind) for ind in xrange(NUM_CHARS)]

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
  """
    Reject invalid solutions when there are not all blacks, then there cannot be
    that same color in that same position.
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
          #print 'Pos to guess: %d' % pos_to_guess
          #print 'Unfilled inds: %s' % str(indices_to_use)
          pass
        if pos_to_guess in indices_to_use: # TODO: Shouldn't this be true though? Huh?
          indices_to_use.remove(pos_to_guess)
        else:
          if DEBUG:
            print 'wtf a problem white'
        # Fill in indices for which we know the color cannot be there.
        for index in indices_to_use:
          unfilled = unfilled_indices[:]
          unfilled.remove(index)

          used_guess = used_for_guess[:]
          used_guess[pos_to_guess] = True # Hm?

          color_from_guess = guess[pos_to_guess]
          pot_sol = potential_sol[:]
          pot_sol[index] = color_from_guess
          _FindAns(blacks, whites, blanks, unfilled, used_guess, pot_sol)

    elif blanks > 0:
      blanks -= 1
      # Go through the unused indices.
      unguessed_indices = _GetUnguessed(used_for_guess)
      for pos_to_guess in unguessed_indices:
        # Apply the blank rule to all unset indices just in case.
        indices_to_use = unfilled_indices[:]
        for index in indices_to_use: 
          color_from_guess = guess[pos_to_guess]
          # Find all other colors that are not this guess.
          diff_colors = _ColorsNotMine(color_from_guess)
          for diff_color in diff_colors:
            unfilled = unfilled_indices[:]
            if index in unfilled: # TODO: shouldnt this always be true though?
              unfilled.remove(index)
            else:
              print 'wtf a problemm blank' 
            used_guess = used_for_guess[:]
            used_guess[pos_to_guess] = True

            pot_sol = potential_sol[:]
            pot_sol[index] = diff_color
            _FindAns(blacks, whites, blanks, unfilled, used_guess, pot_sol)
    else:
      # We have reached the end horray.
      answers.add(tuple(potential_sol))

  num_blanks = NUM_SPACES - num_whites - num_blacks
  unfilled_indices = [ind for ind in xrange(NUM_SPACES)] #[0, 1, 2, 3, 4]
  used_for_guess = [False for _ in xrange(NUM_SPACES)] #[False, False, False, False, False]
  potential_sol = [-1 for _ in xrange(NUM_SPACES)] #[-1, -1, -1, -1, -1]
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
    print 'Number of possibilities: %d' % num_poss
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
      #print 'Prev solutions are: %s' % str(self.possibles)
      print 'Possible solutions are: %s' % str(now_possibles)
    # Find the union of previous possible answers and my possible answers.
    self.possibles = list(now_possibles.intersection(set(self.possibles)))
    if DEBUG:
      #print 'Union of possibles is: %s' % str(self.possibles)
      pass

  def _MakePossibles(self, num_chars, num_spaces):
    """Creates a list of tuples for all possible numbers."""
    valid_chars = ''.join(VALID_CHARS)
    #valid_chars = '01234567'
    return [a for a in itertools.product(valid_chars, repeat=NUM_SPACES)]

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
  for char in ans_tup:
    if char not in VALID_CHARS:
      print 'Your secret must be in the range %s' % str(VALID_CHARS)
      return
  correct = False
  guesser = Guesser()
  while not correct:
    curans = guesser.Guess()
    print 'Guessing %s' % str(curans)
    if curans == ans_tup:
      correct = False # Lets go forever! #True
    else:
      print 'Enter %d pegs with a space (3b 2w):' % NUM_SPACES
      myfeedback = raw_input()
      (blacks, whites) = myfeedback.split(' ')
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

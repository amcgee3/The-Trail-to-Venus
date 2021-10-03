import random
import time
import os, sys

enter = '\n'
tab = '\t'
blue = "\033[0;34m"
yellow = "\033[0;33m"

def clear(): # Will clear the results box to save space/memory
  os.system('clear')

def sp(message):
  delay = 0.04
  shown_message = message
  for letter in shown_message:
    sys.stdout.write(letter)
    sys.stdout.flush()
    time.sleep(delay)
  print() # Prints out the letters in a string

welcome_text = """
Ever since the first moon landing space has been seen as vast, and full of wonder! 
The year is 2023 and in the wake of Covid, our efforts to explore space are only getting bigger.
Your goal is to travel to Earth's closest neighbor, Venus. You are an astronaut piloting an 
advanced American space exploration craft. You will have to manage your food and health to 
make sure you survive the journey. Not unlike Oregon Trail, you will need to get food outside of what you start with.

However, you will be requesting food from your superiors this time. 
"""

help_text = """
Each turn you can take one of 3 actions:

  travel - moves you randomly between 1000-5000 miles and takes
           3-7 days.
  rest   - increases health by 20 (up to 100 maximum) and takes
           2-5 days.
  request - you request 100 lbs of food and takes 2-5 days.

When prompted for an action, you can also enter one of these
commands without using up your turn:

  status - lists food, health, distance traveled, and day.
  help   - lists all the commands.
  quit   - will end the game.
  
You can also use these shortcuts for commands:

  't', 'r', 'r2', 's', '?', 'q' 
  
  Note: r2 is for request
  
"""

# Global variables

miles_traveled = 0
food_remaining = 500
month = 10
day = 1
player_name = ""
sick = 2

# Constants

min_miles = 1000 #Travel
max_miles = 5000
min_days = 3 # For the sake of the game we will say its 3 days
max_days = 7

min_rest = 2
max_rest = 5
health_per_rest = 20
health = 100

request_food = 100
min_request = 2
max_request = 5
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

daily_rations = 10
distance = 25476219
days_31 = [0, 2, 4, 6, 7, 9, 11] # months
days_30 = [3, 5, 8, 10]
days_28 = [1]

# Gameplay

def game_over():
  if health <= 0:
    sp("Unfortunately you are unable to make it to venus.")
    sp("We hope you enjoyed our game!")
    sp("Game Over.")
    return False
  elif food_remaining <= 0:
    sp("Without food, you are unable to continue your journey.")
    sp("Your only hope now is to turn back.")
    return False
  elif distance < miles_traveled:
    sp("Your mission was successful. America is greatful for your efforts!")
    sp("We hope you enjoyed our game!")
    sp("The end... For now.")
    return False
  else:
    return True

def sickness():
  global day, month, sick, health
  days_remaining = days_in_month(month) - day
  random_day = random.randint(0, days_remaining)
  if random_day <= sick:
    sick -= 1
    print("You got sick")
    health -= 20
  

def date_as_string(m, d):
  print(months[m] + " " + str(d))

def days_in_month(m):
  if m in days_31:
    return 31
  elif m in days_30:
    return 30
  elif m in days_28:
    return 28
  else:
    print("Wrong number")

def month_change():
  global day, month
  if day > days_in_month(month):
    day -= days_in_month(month)
    month += 1
    sick = 2

def status_update():
  date_as_string(month, day)
  miles_remaining()
  print("health: ", health)
  print("Food left", food_remaining)

def travel():
  global day, miles_traveled, food_remaining
  distance_traveled = random.randint(min_miles, max_miles)
  days_traveled = random.randint(min_days, max_days)
  print("You travel", distance_traveled, "miles")
  print("It takes", days_traveled, "days")
  day += days_traveled
  miles_traveled += distance_traveled
  food_remaining -= days_traveled * 5
  month_change()
  sickness()

def rest():
  global day, food_remaining, health
  if health == 100:
    print("You are already fully rested.")
  else:
    days_rested = random.randint(min_rest, max_rest)
    print("You rest for", days_rested, "days")
    health += 20
    day += days_rested
    food_remaining -= days_rested * 5
    month_change()
    sickness()

def miles_remaining():
  global miles_traveled
  print("Distance left: " + str(distance - miles_traveled) + " miles")

def request():
  global day, food_remaining
  days_requesting = random.randint(min_request, max_request)
  print("You request for:", days_requesting, "days")
  day += days_requesting
  food_remaining -= days_requesting * 5
  food_remaining += 100
  month_change()
  sickness()

def help():
  print(help_text)

def intro():
  print(blue)
  sp("==============================================================")
  sp(tab + tab + tab + tab + "The Path to Venus")
  sp("==============================================================")
  print(enter + yellow)
  time.sleep(2.5)
  sp("What is your name?" + enter)
  player_name = input()

def background():
  sp(welcome_text + enter)
  sp(help_text + enter)
  time.sleep(5)

def random_events():
  global health, food_remaining
  events = ['asteroid', 'boarded', 'black hole','falling star', 'supply ship', 'rival', 'nothing']
  event = random.choice(events)
  if event == 'asteroid':
    start_time = time.time()
    response = input("An asteroid approaches your ship! Type bang quickly to stop it!" + enter + "Use all caps or no caps.")
    end_time = time.time()
    elapsed = end_time - start_time
    if elapsed < 5.0 and response == 'bang' or response == 'BANG':
      sp("Your time is: " + str(elapsed))
      sp("You manage to esacpe unharmed! Nice!")
    elif elapsed > 5.0 and response == 'bang' or response == 'BANG':
      sp("Your time is: " + str(elapsed))
      sp("You manage to hit the asteroid, but a piece hits your ship.")
      health = 50
    else:
      sp("Your time is: " + str(elapsed))
      sp('You are unable to stop the asteroid and it destroys your ship.')
      health = 0
  if event == 'boarded':
    sp('A strange slime starts oozing from the walls. Some of it gets on you')
    sp('Press enter 5 times as quickly as possible to get it off')
    start_time = time.time()
    input()
    input()
    input()
    input()
    input()
    end_time = time.time()
    elapsed = end_time - start_time
    if elapsed <= 3.0:
      sp("Your time is: " + str(elapsed))
      sp('You get the slime off just in time, and it dissipates.')
      sp('You notice that the slime ate away at parts of the ship')
    elif elapsed < 5.0:
      sp("Your time is: " +  str(elapsed))
      sp('With some difficulty, you get the goop off of you')
      sp('The slime leaves burn marks in the places it touched.')
      health -= 10
    elif elapsed <= 8.0:
      sp("Your time is: " + str(elapsed))
      sp('You get the seemingly acidic goop off of you but it does a lot of damage.')
      sp('You should probably lay off the travel for a turn.')
      health -= 30
    elif elapsed <= 11.0:
      sp("Your time is: " + str(elapsed))
      sp("You are in agonizing pain because the material has left your bones visible in some places.")
      sp('You will probably survive, but be advised that more is in store.')
      health -= 60
    else:
      sp("Your time is: " + str(elapsed))
      sp('Yikes, that went horribly. Your body was consumed by the goop.')
      health = 0
  if event == 'black hole':
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    rand1 = random.choice(letters)
    rand2 = random.choice(letters)
    rand3 = random.choice(letters)
    rand4 = random.choice(letters)
    rand5 = random.choice(letters)
    sp('You are approaching a black hole.')
    sp('Quickly. Enter the letters as they appear on screen')

    string = rand1 + rand2 + rand3 + rand4 + rand5
    print(string)

    start_time = time.time()
    string2 = input()
    end_time = time.time()
    elapsed = end_time - start_time

    if string2 == string and elapsed < 8.0:
      sp("Your time is: " + str(elapsed))
      sp('You escape, and you also hope that never happens again.')
    elif string2 == string and elapsed < 12.0:
      sp("Your time is: " + str(elapsed))
      sp('You escape, but in your panic you hit your toe under the controls and it HURTS.')
      health -= 10
    elif string2 == string and elapsed < 16.0:
      sp("Your time is: " + str(elapsed))
      sp('You barely escape. Might want to check your pants after that one.')
      health -= 20
    else:
      sp("Your time is: " + str(elapsed))
      sp('You get swallowed by the black hole and are never seen again.')
      health = 0
  if event == 'falling star':
    star = ['left', 'right', 'left', 'right', 'left', 'right']
    fall = random.choice(star)
    sp("A star, beautiful and elegant is flying towards your ship.")
    sp("Which direction will you dodge in? (left, right)")
    dodge = input()

    math = ['6 + 4', '12 - 15', '6 + 20', '15 - 5', '100 - 64', ' 72 + 36', '144 - 12']
    answers = [10, -3, 26, 10, 36, 108, 132]
    roll = [0, 1, 2, 3, 4, 5, 6]
    roll2 = [0, 1, 2, 3, 4, 5, 6]

    pick = random.choice(roll)
    pick2 = random.choice(roll2)

    problem1 = math[pick]
    problem2 = math[pick2]
    check = 0
    check2 = 0

    if fall == dodge:
      sp("Math will save you! Enter the answers!")
      sp("Problem1: " + str(problem1))
      answer1 = input()
      sp("Problem2: " + str(problem2))
      answer2 = input()

      check = answers[pick]
      check2 = answers[pick2]

      if check == answer1 and check2 == answer2:
        sp("Your quick thinking helps you avoid trouble!")
      elif check != answer1 and check2 == answer2:
        sp("You get away, but not without scratches.")
        health -= 25
      elif check == answer1 and check2 != answer2:
        sp("You get away, but not without scratches.")
        health -= 25
      else:
        sp("You aren't sure why you weren't burned to ashes but you are in a lot of pain")
        health -= 50
    elif dodge != 'left' or dodge != right:
      sp('Yikes, if you were at full health you are lucky to be alive.')
      sp("If you aren't I regret to inform you that you did not make it.")
      health -= 90
    else:
      sp("You guess right and are able to avoid the star with ease.")
  if event == 'supply ship':
    sp("You find the wreckage of a ship.")
    sp("Would you like to go inside? (y/n)")
    answer3 = input()
    if answer3 == 'y' or answer3 == 'yes':
      sp('You enter the ship, it is safe enough to walk around but you can see it is still')
      sp('falling apart. Be careful!')
      problems = ['What color is the sky (no caps)', '12/2', 'What planet is closest to the earth? (no caps)', 'Is pluto a planet (y/n)', 'What Mortal Kombat character shares their name with a japanese sword? (spell her name not the sword)', "How many A's are in the word alakazam", "Name the capital of Alabama (no caps)"]
      answers = ['blue', 6, 'venus', 'yes', 'kitana', 4, "montgomery"]
      number = [0, 1, 2, 3, 4, 5, 6]
      number2 = [0, 1, 2, 3, 4, 5, 6]
      pick = random.choice(number)
      pick2 = random.choice(number2)
      question = problems[pick]
      answer = answers[pick]
      question2 = problems[pick2]
      answer2 = answers[pick2]

      sp("You are picking up supplies when you hear debree start falling. Answer 2 questions to get out!")
      sp(question)
      attempt = input()
      sp(question2)
      attempt2 = input()
      if attempt == answer and attempt2 == answer2:
        sp("You get out with your supplies and no damage to yourself. ")
        sp('You get 250 food for your troubles')
        food_remaining += 250
      elif attempt != answer and attempt2 == answer2:
        sp("You get out, but you do get hit with a bit of rubble on the way out.")
        sp("you get 100 food for your troubles.")
        food_remaining += 100
        health -= 25
      elif attempt == answer and attempt2 != answer2:
        sp("You get out, but you do get hit with a bit of rubble on the way out.")
        sp("you get 100 food for your troubles.")
        food_remaining += 100
        health -= 25
      else:
        sp("You get out, but you lose all of the supplies you picked up.")
        sp("You have a nasty run in with a piece of rubble almost crushing you, but you get out")
        health -= 40
    else:
      sp('You do not enter the ship. Thats a shame, could of been some cool stuff in there.')
  if event == 'rival':
    sp("You are able to make out a ship in the distance.")
    sp("You aren't sure what country is from, but you know he isn't with America")
    sp("You both see a nearby abandoned ship floating. Will you go for it? (y/n)")
    answer = input()
    if answer == 'y' or answer == 'yes':
      sp('To claim the prize you must type your name as fast as possible.')
      sp('Your name is: ' + functions.player_name)
      start = time.time()
      name = input()
      end = time.time()
      elapsed = end - start
      
      if name == functions.player_name and elapsed < 3.0:
        sp('You destroy your rival in a race.')
        sp('You find that the ship has a lot of extra supplies but you are a good sport and leave some for him.')
        food_remaining += 325
      elif name == functions.player_name and elapsed < 6.0:
        sp('You win with a somewhat decent lead.')
        sp('You find that the ship has a good few supplies, but you leave some for your rival.')
        food_remaining += 250
      elif name == functions.player_name and elapsed < 9.0:
        sp('You barely win the race, and your rival arrives behind you.')
        sp('Since you won you get first pick of the supplies and decide to split them.')
        food_remaining += 175
      elif name == functions.player_name and elapsed < 12.0:
        sp('You just barely lose the race')
        sp('Your rival takes his fill of supplies and leaves you a few.')
        food_remaining += 100
      else:
        sp('You lose and the race isnt even close')
        sp('Your rival rubs salt in your wounds by hardly leaving you anything.')
        food_remaining += 25
    else:
      sp("You ignore them both and go on your merry way.")
  if event == 'nothing':
    sp("Nothing interesting happens and you decide to take a rest.")
    health += 20
  



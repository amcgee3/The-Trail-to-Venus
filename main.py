import functions

functions.intro()
functions.background()

option = ""
playing = True
count = 0

while playing:
  option = input('What would you like to do?' + functions.enter)

  if option == 'status' or option == 's':
    functions.status_update()
  if option == 'help' or option == '?':
    print(functions.help_text)
  if option == 'travel' or option == 't':
    functions.travel()
  elif option == 'rest' or option == 'r':
    functions.rest()
  elif option == 'request' or option == 'r2':
    functions.request()
  elif option == 'quit' or option == 'q':
    break
  
  functions.random_events()
  playing = functions.game_over()
  continue
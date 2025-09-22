import ui
import stock_ui


while True:
  ui.clear()
  
  print("simple CASHDESK system")
  print("       ^^^^^^^^")
  
  print()
  print()
  
  print("Use one of the commands to proceed:")
  print("  c - open cashdesk system")
  print("  s - manage stock items")
  print("  q - quit program")
  print()
  
  command = input("Enter command: ").strip().lower()
  
  if command == "q":
    exit()
  elif command == "c":
    pass
  elif command == "s":
    stock_ui.stock_loop()
  else:
    print("Unknown command")
    ui.wait_for_enter()

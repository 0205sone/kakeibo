import sys
from PySide6.QtWidgets import QApplication
from household_app import HouseholdApp

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = HouseholdApp()
  window.show()
  sys.exit(app.exec())

import csv
from datetime import datetime
from collections import defaultdict
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
    QFileDialog, QWidget, QComboBox, QDateEdit
)
from PySide6.QtCore import QDate


class HouseholdApp(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("家計簿アプリ")
    self.setGeometry(100, 100, 600, 500)

    # メインウィジェット
    self.central_widget = QWidget()
    self.setCentralWidget(self.central_widget)

    # レイアウト
    self.layout = QVBoxLayout(self.central_widget)

    # 入力フォーム
    self.setup_input_form()

    # テーブル
    self.table = QTableWidget()
    self.table.setColumnCount(3)
    self.table.setHorizontalHeaderLabels(["項目", "金額", "日付"])
    self.layout.addWidget(self.table)

    # CSV操作ボタン
    self.setup_csv_buttons()

    # 月の合計計算UI
    self.setup_month_total_ui()

  def setup_input_form(self):
    # 入力フォームのレイアウト
    self.input_layout = QHBoxLayout()
    self.layout.addLayout(self.input_layout)

    # 項目 (履歴付き)
    self.category_input = QComboBox()
    self.category_input.setEditable(True)
    self.category_input.setPlaceholderText("項目 (例: 食費)")
    self.input_layout.addWidget(self.category_input)

    # 金額
    self.amount_input = QLineEdit()
    self.amount_input.setPlaceholderText("金額 (例: 5000)")
    self.input_layout.addWidget(self.amount_input)

    # 日付選択 (カレンダー付き)
    self.date_input = QDateEdit()
    self.date_input.setCalendarPopup(True)
    self.date_input.setDate(QDate.currentDate())
    self.input_layout.addWidget(self.date_input)

    # 追加ボタン
    self.add_button = QPushButton("追加")
    self.add_button.clicked.connect(self.add_entry)
    self.input_layout.addWidget(self.add_button)

  def setup_csv_buttons(self):
    # CSV保存ボタン
    self.save_button = QPushButton("CSVに保存")
    self.save_button.clicked.connect(self.save_to_csv)
    self.layout.addWidget(self.save_button)

    # CSV読み込みボタン
    self.load_button = QPushButton("CSVを読み込み")
    self.load_button.clicked.connect(self.load_from_csv)
    self.layout.addWidget(self.load_button)

  def setup_month_total_ui(self):
    # 月の合計計算のUI
    self.month_layout = QHBoxLayout()
    self.layout.addLayout(self.month_layout)

    # 日付選択 (月単位)
    self.month_selector = QDateEdit()
    self.month_selector.setCalendarPopup(True)
    self.month_selector.setDisplayFormat("yyyy-MM")  # 年月のみ表示
    self.month_selector.setDate(QDate.currentDate())
    self.month_layout.addWidget(self.month_selector)

    # 合計計算ボタン
    self.calculate_button = QPushButton("合計金額を計算")
    self.calculate_button.clicked.connect(self.calculate_monthly_total)
    self.month_layout.addWidget(self.calculate_button)

    # 合計金額表示ラベル
    self.total_label = QLabel("その月の合計金額: 0円")
    self.layout.addWidget(self.total_label)

  def add_entry(self):
    category = self.category_input.currentText()
    amount = self.amount_input.text()
    date = self.date_input.date().toString("yyyy-MM-dd")

    if category and amount.isdigit():
      row = self.table.rowCount()
      self.table.insertRow(row)
      self.table.setItem(row, 0, QTableWidgetItem(category))
      self.table.setItem(row, 1, QTableWidgetItem(amount))
      self.table.setItem(row, 2, QTableWidgetItem(date))

      if category not in [self.category_input.itemText(i) for i in range(self.category_input.count())]:
        self.category_input.addItem(category)

      self.amount_input.clear()

  def save_to_csv(self):
    path, _ = QFileDialog.getSaveFileName(
        self, "CSVファイルを保存", "", "CSV Files (*.csv)")
    if path:
      with open(path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["項目", "金額", "日付"])
        for row in range(self.table.rowCount()):
          category = self.table.item(row, 0).text()
          amount = self.table.item(row, 1).text()
          date = self.table.item(row, 2).text()
          writer.writerow([category, amount, date])

  def load_from_csv(self):
    path, _ = QFileDialog.getOpenFileName(
        self, "CSVファイルを開く", "", "CSV Files (*.csv)")
    if path:
      with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        self.table.setRowCount(0)
        for row_data in reader:
          row = self.table.rowCount()
          self.table.insertRow(row)
          for column, data in enumerate(row_data):
            self.table.setItem(row, column, QTableWidgetItem(data))

  def calculate_monthly_total(self):
    # ユーザーが選択した年月
    selected_date = self.month_selector.date()
    selected_month = selected_date.toString("yyyy-MM")  # yyyy-MM形式に変換

    total = 0
    for row in range(self.table.rowCount()):
      date_item = self.table.item(row, 2)
      amount_item = self.table.item(row, 1)

      if date_item and amount_item:
        try:
          date = datetime.strptime(date_item.text(), "%Y-%m-%d")
          if date.strftime("%Y-%m") == selected_month:
            total += int(amount_item.text())
        except ValueError:
          continue

    self.total_label.setText(f"その月の合計金額: {total}円")

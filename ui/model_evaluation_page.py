from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QDateEdit, QLineEdit)
from PySide6.QtCore import QDate
from PySide6.QtWebEngineWidgets import QWebEngineView

from database.database_manager import load_sales_data
from analytics.models import train_ai_models

from visulisations.graphs import create_predicted_vs_actual


class EvaluationPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # page title
        title = QLabel("Model Training")
        title.setFixedHeight(30)
        main_layout.addWidget(title)

        #data filter
        filter_row = QHBoxLayout()

        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate(2025, 3, 1))

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate(2025, 10, 31))

        self.file_version = QLineEdit()
        self.file_version.setPlaceholderText("Enter new module version...")


        self.apply_button = QPushButton("Create models")
        self.apply_button.clicked.connect(self.update_model_evaluation)

        filter_row.addWidget(QLabel("Start Date"))
        filter_row.addWidget(self.start_date)
        filter_row.addWidget(QLabel("End Date"))
        filter_row.addWidget(self.end_date)
        filter_row.addWidget(self.file_version)
        filter_row.addWidget(self.apply_button)
        filter_row.addStretch()

        main_layout.addLayout(filter_row)

        # summary cards
        cards_row = QHBoxLayout()
        cards_row.setSpacing(15)

        self.cappuccino_model_acc_card, self.cappuccino_model_acc_value = self.create_card("Cappuccino model accuracy:", "0")
        self.americano_model_acc_card, self.americano_model_acc_value = self.create_card("Americano model accuracy", "0")
        self.croissant_model_acc_card, self.croissant_model_acc_value = self.create_card("Croissant model accuracy", "0")

        cards_row.addWidget(self.cappuccino_model_acc_card)
        cards_row.addWidget(self.americano_model_acc_card)
        cards_row.addWidget(self.croissant_model_acc_card)

        main_layout.addLayout(cards_row)
        
        #chart section
        charts_row = QHBoxLayout()
        charts_row.setSpacing(15)
        
        # Main chart on left side
        self.predicted_vs_actual_chart = self.create_chart_placeholder("Sales Over Time")
        charts_row.addWidget(self.predicted_vs_actual_chart)

        main_layout.addLayout(charts_row)

    def create_card(self, title_text, value_text):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setFixedHeight(120)

        layout = QVBoxLayout(card)

        title = QLabel(title_text)
        value = QLabel(value_text)

        layout.addWidget(title)
        layout.addWidget(value)

        return card, value

    def create_chart_placeholder(self, title_text):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(frame)

        title = QLabel(title_text)
        placeholder = QLabel("Chart will go here")

        layout.addWidget(title)
        layout.addWidget(placeholder)

        return frame
    
    def update_model_evaluation(self):
        
        # get user selected dates
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        file_version = self.file_version.text()

        #load data from specified time period
        data = load_sales_data(start_date, end_date)

        #train models
        results, predictions = train_ai_models(data, file_version)

        #get data for error cards
        cappuccino_model_err = results[results["product"] == "cappuccino"]["mae"].values[0]
        americano_model_err = results[results["product"] =="americano"]["mae"].values[0]
        croissant_model_err = results[results["product"] =="croissant"]["mae"].values[0]

        self.croissant_model_acc_value.setText(f"{croissant_model_err}%")
        self.cappuccino_model_acc_value.setText(f"{cappuccino_model_err}%")
        self.americano_model_acc_value.setText(f"{americano_model_err}%")

        #create prediction vs actual sales grph
        predicted_vs_actual_graph = create_predicted_vs_actual(predictions)
        #display chart
        self.show_chart(self.predicted_vs_actual_chart, predicted_vs_actual_graph)

        

        


    def show_chart(self, container, figure):

        html = figure.to_html(include_plotlyjs = "cdn")


        layout = container.layout()

        while layout.count() > 1:
            item = layout.takeAt(1)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        view = QWebEngineView()
        view.setHtml(html)
        layout.addWidget(view)

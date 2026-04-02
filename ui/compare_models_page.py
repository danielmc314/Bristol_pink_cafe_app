from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QDateEdit, QLineEdit, QComboBox, )
from PySide6.QtCore import QDate, Qt
from PySide6.QtWebEngineWidgets import QWebEngineView

from database.database_manager import load_sales_data
from analytics.models import predict_future_sales

from visulisations.graphs import create_model_comparison_chart


class CompareModelsPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 8, 10, 8)
        main_layout.setSpacing(4)

        # page title
        title = QLabel("Model Training")
        title.setFixedHeight(30)
        main_layout.addWidget(title)

        #----------filter card------------
        filter_card = QFrame()
        filter_card.setObjectName("filterCard")
        filter_card_layout = QVBoxLayout(filter_card)
        filter_card_layout.setContentsMargins(10, 0, 10, 0)
        filter_card_layout.setSpacing(3)
        
        #-------first row of filter card--------
        form_row = QHBoxLayout()
        form_row.setSpacing(12)
        
        #standerdize widths and hights of input forms
        field_width = 180
        field_height = 32
        
        #start date selector
        start_layout = QVBoxLayout()
        start_layout.setSpacing(2)
        start_layout.setContentsMargins(0, 0, 0, 0)
        
        start_label = QLabel("Start Date")
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate(2025, 3, 1))
        self.start_date.setFixedWidth(field_width)
        self.start_date.setFixedHeight(field_height)

        start_layout.addWidget(start_label)
        start_layout.addWidget(self.start_date)

        # end date selector
        end_layout = QVBoxLayout()
        end_layout.setSpacing(2)
        end_layout.setContentsMargins(0, 0, 0, 0)

        end_label = QLabel("End Date")
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setFixedWidth(field_width)
        self.end_date.setFixedHeight(field_height)

        end_layout.addWidget(end_label)
        end_layout.addWidget(self.end_date)

        # model virsion imput field
        model_1_layout = QVBoxLayout()
        model_1_layout.setSpacing(2)
        model_1_layout.setContentsMargins(0, 0, 0, 0)
        
        model_1_label = QLabel("Select First Model")
        self.model_1_selection = QComboBox()
        self.model_1_selection.setFixedWidth(220)


        model_1_layout.addWidget(model_1_label)
        model_1_layout.addWidget(self.model_1_selection)

          # model virsion imput field
        model_2_layout = QVBoxLayout()
        model_2_layout.setSpacing(2)
        model_2_layout.setContentsMargins(0, 0, 0, 0)
        
        model_2_label = QLabel("Select Second Model")
        self.model_2_selection = QComboBox()
        self.model_2_selection.setFixedWidth(220)


        model_2_layout.addWidget(model_2_label)
        model_2_layout.addWidget(self.model_2_selection)


        #create model button
        self.create_models_button = QPushButton("Create Models")
        self.create_models_button.clicked.connect(self.update_model_evaluation)
        self.create_models_button.setFixedWidth(180)
        self.create_models_button.setFixedHeight(field_height)
    

        

        #add elemements to form row
        form_row.addLayout(start_layout)
        form_row.addLayout(end_layout)
        form_row.addLayout(model_1_layout)
        form_row.addLayout(model_2_layout)
        form_row.addWidget(self.create_models_button, alignment=Qt.AlignBottom)
        form_row.addStretch()

        
        # Add rows to card
        filter_card_layout.addLayout(form_row)
        
        
        #add filter card and contents to main layout with top alignement
        main_layout.addWidget(filter_card, 0, Qt.AlignTop)
        
        

        

        # summary cards
        cards_row = QHBoxLayout()
        cards_row.setSpacing(15)

        self.model_1_acc_card, self.model_1_acc_value = self.create_card("model 1 accuracy:", "0")
  
        self.cmodel_2_acc_card, self.model_2_acc_value = self.create_card("model 2 accuracy", "0")

        cards_row.addWidget(self.model_1_acc_card)
        cards_row.addWidget(self.model_2_acc_card)

        main_layout.addLayout(cards_row, 1)
        
        #chart section
        charts_row = QHBoxLayout()
        charts_row.setSpacing(15)
        
        # Main chart on left side
        self.model_1_vs_model_2 = self.create_chart_placeholder("Sales Over Time")
        charts_row.addWidget(self.model_1_vs_model_2)

        main_layout.addLayout(charts_row, 3)

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
        
        # get user selected variables for model training
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        model_1 = self.model_1_selection.currentData()
        model_2 = self.model_2_selection.currentData()
        
        train_ratio = self.get_train_split_ratio()
        test_ratio = 1 - train_ratio


        #load data from specified time period
        data = load_sales_data(start_date, end_date)

        #train models
        model_1_predictions, predictions_long  = predict_future_sales(data, model_1,)
        model_2_predictions,  predictions_long= predict_future_sales(data, model_2,)

        actual_sales  = load_sales_data(start_date, end_date)
        actual_df = actual_sales.pivot(index="date", columns="product", values="sales")


        #get data for error cards
        #model_1_err = model_1_results[model_1_results["product"] == "cappuccino"]["mae"].values[0]
        #model_2_err = model_2_results[model_2_results["product"] =="americano"]["mae"].values[0]
        
        #self.model_1_acc_value.setText(f"Model 1 err: {model_1_err}")
        #self.model_2_acc_value.setText(f"Model 2 err: {model_2_err}")
        #create prediction vs actual sales grph
        model_vs_model_graph = create_model_comparison_chart(actual_df, model_1_predictions, model_2_predictions, model_1, model_2)
        #display chart
        self.show_chart(self.model_1_vs_model_2, model_vs_model_graph)

        

        


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

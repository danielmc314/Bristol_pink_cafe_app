from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QDateEdit, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import QDate
from PySide6.QtWebEngineWidgets import QWebEngineView

from analytics.models import predict_future_sales

from database.database_manager import get_models

from visulisations.graphs import (
    create_predicted_sales_chart
)

class PredictionPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # page title
        title = QLabel("Predictions")
        title.setFixedHeight(30)
        main_layout.addWidget(title)

        #data filter
        filter_row = QHBoxLayout()

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate(2025, 10, 31))

        self.model_selection = QComboBox()
        



        self.apply_button = QPushButton("Apply Filter")
        self.apply_button.clicked.connect(self.update_dashboard)

        
        filter_row.addWidget(QLabel("End Date"))
        filter_row.addWidget(self.end_date)
        filter_row.addWidget(self.model_selection)
        filter_row.addWidget(self.apply_button)
        filter_row.addStretch()

        main_layout.addLayout(filter_row)

        # summary cards
        cards_row = QHBoxLayout()
        cards_row.setSpacing(15)

        self.total_sales_card, self.total_sales_value = self.create_card("Total Predicted Sales", "0")
        self.coffee_sales_card, self.coffee_sales_value = self.create_card("Coffee Predicted Sales", "0")
        self.food_sales_card, self.food_sales_value = self.create_card("Food predicted Sales", "0")

        cards_row.addWidget(self.total_sales_card)
        cards_row.addWidget(self.coffee_sales_card)
        cards_row.addWidget(self.food_sales_card)

        main_layout.addLayout(cards_row)
        
        #chart section
        charts_row = QHBoxLayout()
        charts_row.setSpacing(15)
        
        # Main chart on left side
        self.predicted_sales_chart = self.create_chart_placeholder("Predicted sales")
        
        #table for predicted sales
        self.predicted_sales_table = QTableWidget()
        self.predicted_sales_table.setColumnCount(3)
        self.predicted_sales_table.setHorizontalHeaderLabels(
            ["Date", "Product", "Sales"]
        )

        self.predicted_sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.predicted_sales_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.predicted_sales_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.predicted_sales_table.setAlternatingRowColors(True)


        #add to main chart row
        charts_row.addWidget(self.predicted_sales_chart, 3)
        charts_row.addWidget(self.predicted_sales_table, 2)



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
    
    def update_dashboard(self):
        
        selected_model_version = self.model_selection.currentText()
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        
        future_sales, future_sales_long_formate = predict_future_sales(end_date, selected_model_version)
        
        #convert datafram to list
        future_sales_long_formate = future_sales_long_formate.values.tolist()

        # run querys using user selected dates
        predicted_coffee_sales = (
            future_sales["cappuccino"].sum() +
            future_sales["americano"].sum()
        )
        predicted_food_sales = future_sales["croissant"].sum()
        predicted_total_sales = predicted_coffee_sales + predicted_food_sales

     
        #set values for top 3 cards on dashboard
        self.total_sales_value.setText(f"{predicted_total_sales}")
        self.coffee_sales_value.setText(f"{predicted_coffee_sales}")
        self.food_sales_value.setText(f"{predicted_food_sales}")

        # create chart and table using results from querys
        line_chart = create_predicted_sales_chart(future_sales)
        self.populate_table(future_sales_long_formate)
    



        
        # display charts
        self.show_chart(self.predicted_sales_chart, line_chart)
        
    

    #displayes charts in application
    def show_chart(self, container, figure):
        
        #plotly generates HTML and javascript code origianlly
        html = figure.to_html(include_plotlyjs = "cdn")


        layout = container.layout()
        
        #delete previousely displayed charts to prevent stacking of graphs in ui
        while layout.count() > 1:
            item = layout.takeAt(1)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        
        #qwebengine is needed as pyside 6 cannot render plotly graphs nativly 
        #qwebengine creates an embedded browser which allows plotly to run like a webpage
        view = QWebEngineView()
        view.setHtml(html)
        layout.addWidget(view)
    
    #need to refresh dropdown box when changes are made to models database
    def refresh_model_dropdown(self):
        self.model_selection.clear()
        self.model_selection.addItems(get_models())

    def populate_table(self, data):
        #make sure table is clear before loading new predictions
        self.predicted_sales_table.clearContents()
        self.predicted_sales_table.setRowCount(len(data))

        for row_index, row in enumerate(data):
            for col_index, value in enumerate(row):
                self.predicted_sales_table.setItem(row_index, col_index, QTableWidgetItem(str(value)))
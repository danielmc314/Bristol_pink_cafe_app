from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QDateEdit)
from PySide6.QtCore import QDate
from PySide6.QtWebEngineWidgets import QWebEngineView

from analytics.analysis import (
    get_total_sales,
    get_coffee_sales,
    get_food_sales,
    get_sales_by_product,
    get_sales_by_weekday,
    get_sales_by_date
)

from visulisations.graphs import (
    create_sales_line_chart,
    create_sales_by_product_chart,
    create_sales_by_weekday_chart
)

class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # page title
        title = QLabel("Dashboard")
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

        self.apply_button = QPushButton("Apply Filter")
        self.apply_button.clicked.connect(self.update_dashboard)

        filter_row.addWidget(QLabel("Start Date"))
        filter_row.addWidget(self.start_date)
        filter_row.addWidget(QLabel("End Date"))
        filter_row.addWidget(self.end_date)
        filter_row.addWidget(self.apply_button)
        filter_row.addStretch()

        main_layout.addLayout(filter_row)

        # summary cards
        cards_row = QHBoxLayout()
        cards_row.setSpacing(15)

        self.total_sales_card, self.total_sales_value = self.create_card("Total Sales", "£0")
        self.coffee_sales_card, self.coffee_sales_value = self.create_card("Coffee Sales", "£0")
        self.food_sales_card, self.food_sales_value = self.create_card("Food Sales", "£0")

        cards_row.addWidget(self.total_sales_card)
        cards_row.addWidget(self.coffee_sales_card)
        cards_row.addWidget(self.food_sales_card)

        main_layout.addLayout(cards_row)
        
        #chart section
        charts_row = QHBoxLayout()
        charts_row.setSpacing(15)
        
        # Main chart on left side
        self.sales_over_time_chart = self.create_chart_placeholder("Sales Over Time")
        

        # Bottom charts
        right_charts = QVBoxLayout()
        right_charts.setSpacing(15)

        self.sales_by_product_chart = self.create_chart_placeholder("Sales by Product")
        self.sales_by_weekday_chart = self.create_chart_placeholder("Sales by Weekday")

        right_charts.addWidget(self.sales_by_product_chart)
        right_charts.addWidget(self.sales_by_weekday_chart)

        #add to main chart row
        charts_row.addWidget(self.sales_over_time_chart, 2)
        charts_row.addLayout(right_charts, 1)


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
        
        # get user selected dates
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")

        # run querys using user selected dates
        total_sales = get_total_sales(start_date, end_date)
        coffee_sales = get_coffee_sales(start_date, end_date)
        food_sales = get_food_sales(start_date, end_date)

        sales_by_date = get_sales_by_date(start_date, end_date)
        sales_by_product = get_sales_by_product(start_date, end_date)
        sales_by_weekday = get_sales_by_weekday(start_date, end_date)

        #debugging
        print("total_sales:", total_sales)
        print("coffee_sales:", coffee_sales)
        print("food_sales:", food_sales)
        
        #set values for top 3 cards on dashboard
        self.total_sales_value.setText(f"£{total_sales}")
        self.coffee_sales_value.setText(f"£{coffee_sales}")
        self.food_sales_value.setText(f"£{food_sales}")

        # create charts using results from querys
        line_chart = create_sales_line_chart(sales_by_date)
        product_chart = create_sales_by_product_chart(sales_by_product)
        weekday_chart = create_sales_by_weekday_chart(sales_by_weekday)

        # display charts
        self.show_chart(self.sales_over_time_chart, line_chart)
        self.show_chart(self.sales_by_product_chart, product_chart)
        self.show_chart(self.sales_by_weekday_chart, weekday_chart)

    

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

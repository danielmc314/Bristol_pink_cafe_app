from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QStackedWidget
)

from ui.dashboard_page import DashboardPage
from ui.data_managment_page import DataManagmentPage
from ui.predictions_page import PredictionPage
from ui.model_evaluation_page import EvaluationPage
#from ui.compare_models_page import CompareModelsPage


class AppWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pink Cafe Dashboard")
        self.resize(1200, 800)
        

        main_layout = QHBoxLayout(self)

        # Sidebar
        sidebar_layout = QVBoxLayout()
        title = QLabel("Pink Cafe")
        dashboard_button = QPushButton("Dashboard")
        data_button = QPushButton("Data Management")
        prediction_button = QPushButton("Prediction")
        evaluation_button = QPushButton("Model Training")
        #compare_button   = QPushButton("Compare Models")

        sidebar_layout.addWidget(title)
        sidebar_layout.addWidget(dashboard_button)
        sidebar_layout.addWidget(data_button)
        sidebar_layout.addWidget(prediction_button)
        sidebar_layout.addWidget(evaluation_button)
        #sidebar_layout.addWidget(compare_button)
        sidebar_layout.addStretch()

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setFixedWidth(200)

        sidebar_widget.setStyleSheet("""
                                     background-color: black;
                                     border-radius: 12px;
                                     color: white;
                                     """)

        # Pages
        self.pages = QStackedWidget()
        self.dashboard_page = DashboardPage()
        self.data_managment_page = DataManagmentPage()
        self.predictions_page = PredictionPage()
        self.model_evaluation_page = EvaluationPage()
        #self.compare_models_page = CompareModelsPage()

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.data_managment_page)
        self.pages.addWidget(self.predictions_page)
        self.pages.addWidget(self.model_evaluation_page)
        #self.pages.addWidget(self.compare_models_page)

        self.pages.setCurrentWidget(self.dashboard_page)

        dashboard_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.dashboard_page)
        )
        data_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.data_managment_page)
        )
        prediction_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.predictions_page)
        )
        evaluation_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.model_evaluation_page)
        )
        #compare_button.clicked.connect(
        #    lambda: self.pages.setCurrentWidget(self.compare_models_page)
        #)

        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.pages)
        
        self.pages.currentChanged.connect(self.on_page_changed)

    ##update dropdown selector for models when predictions page is visited
    def on_page_changed(self, index):
        if self.pages.widget(index) == self.predictions_page:
            self.predictions_page.refresh_model_dropdown()
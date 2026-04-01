from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QDateEdit, QFileDialog, QLineEdit, QMessageBox, QTableWidget,
    QTableWidgetItem, QHeaderView)
from PySide6.QtCore import QDate

from database.data_loader import clean_combined_data, single_data_set
from database.database_manager import insert_dataset, insert_sales, load_datasets, delete_dataset, load_all_datasets





class DataManagmentPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # page title
        title = QLabel("Data Managment")
        title.setFixedHeight(10)
        main_layout.addWidget(title)

        #---------------- select files row -------------------#

        select_files_row = QVBoxLayout()
        select_files_row.setSpacing(15)
        
        #select food file row
        select_food_file_row = QHBoxLayout()
        select_food_file_row.setSpacing(15)

        #input field for file
        self.food_file = None
        self.food_file_path_input = QLineEdit()
        self.food_file_path_input.setPlaceholderText("Food data file")
        self.food_file_path_input.setReadOnly(True)

        # upload file button
        self.select_food_file_button = QPushButton("select file")
        self.select_food_file_button.clicked.connect(self.select_food_file)
        
        select_food_file_row.addWidget(self.food_file_path_input)
        select_food_file_row.addWidget(self.select_food_file_button)
        
        #select coffee file
        select_coffee_file_row = QHBoxLayout()
        select_coffee_file_row.setSpacing(15)

        #input field for file
        self.coffee_file = None
        self.coffee_file_path_input = QLineEdit()
        self.coffee_file_path_input.setPlaceholderText("Coffee data file")
        self.coffee_file_path_input.setReadOnly(True)

        # upload file button
        self.select_coffee_file_button = QPushButton("select file")
        self.select_coffee_file_button.clicked.connect(self.select_coffee_file)
        
        select_coffee_file_row.addWidget(self.coffee_file_path_input)
        select_coffee_file_row.addWidget(self.select_coffee_file_button)

        select_files_row.addLayout(select_food_file_row)
        select_files_row.addLayout(select_coffee_file_row)
        
        main_layout.addLayout(select_files_row)

        #upload files row
        upload_files_row = QVBoxLayout()
        upload_files_row.setSpacing(15)

        self.upload_files_button = QPushButton("Upload Files")
        self.upload_files_button.clicked.connect(self.upload_files)
        
        upload_files_row.addWidget(self.upload_files_button)

        main_layout.addLayout(upload_files_row)

        #-----------------------manage database row-------------------

        manage_database_row = QVBoxLayout()
        manage_database_row.setSpacing(15)

        #filter database row
        filter_row = QHBoxLayout()


        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate(2025, 3, 1))

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate(2025, 10, 31))

        self.apply_button = QPushButton("Apply Filter")
        self.apply_button.clicked.connect(self.filter_datasets)
        
        filter_row.addWidget(QLabel("Minimum upload date"))
        filter_row.addWidget(self.start_date)
        filter_row.addWidget(QLabel("Maximum upload date"))
        filter_row.addWidget(self.end_date)
        filter_row.addWidget(self.apply_button)
        filter_row.addStretch()

        main_layout.addLayout(filter_row)

        #-------------table row---------------
        dataset_table_row = QVBoxLayout
        

        self.datasets_table = QTableWidget()
        self.datasets_table.setColumnCount(4)
        self.datasets_table.setHorizontalHeaderLabels(
            ["Dataset ID", "Dataset Name", "Upload Date", "delete"]
        )

        self.datasets_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.datasets_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.datasets_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.datasets_table.setAlternatingRowColors(True)

        main_layout.addWidget(self.datasets_table)




        
        
        main_layout.addStretch()

  


    def select_food_file(self):
        #open file selection window
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select files",
            "",
            "CSV Files (*.csv);;All Files (*)"
            )

        if file_path:
            #display selected file path in input box
            self.food_file_path_input.setText(file_path)
            #save path to variable
            self.food_file = file_path
          

    def select_coffee_file(self):
        #open file selection window
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select files",
            "",
            "CSV Files (*.csv);;All Files (*)"
            )

        if file_path:
            #display selected file path in input box
            self.coffee_file_path_input.setText(file_path)
            #save path to variable
            self.coffee_file = file_path

    def upload_files(self):
        
        #check if food and coffee files have been uploaded or both
        if self.food_file and self.coffee_file:
            sales_data, dataset_name = clean_combined_data(self.food_file, self.coffee_file)
        elif self.food_file:
            sales_data, dataset_name = single_data_set(self.food_file)
        elif self.coffee_file:
            sales_data, dataset_name = single_data_set(self.coffee_file)

        #add new sales data and dataset to database
        dataset_id = insert_dataset(dataset_name)
        insert_sales(sales_data, dataset_id)

        #send popup message to page letting user no upload was successful
        QMessageBox.information(
            self,
            "Upload Successful",
            "sales data and dataset successfully added to database"

        )

        #clear input boxes and file variables
        self.food_file_path_input.clear()
        self.coffee_file_path_input.clear()
        self.food_file = None
        self.coffee_file = None

        

    def filter_datasets(self):
        #get variables from imput fields
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")

        #get datasets that satisfy variables
        data = load_datasets(start_date, end_date)
        self.populate_table(data)




    def populate_table(self, data):
        #make sure table is clear before loading new datasets
        self.datasets_table.clearContents()
        self.datasets_table.setRowCount(len(data))

        for row_index, row in enumerate(data):
            for col_index, value in enumerate(row):
                self.datasets_table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

                row_dataset_id = row[0]

                #create delete button
                delete_button = QPushButton("Delete")

                # connect button with row-specific action
                delete_button.clicked.connect(
                    lambda checked, dataset_id = row_dataset_id: self.delete_dataset_from_db(dataset_id)
                )

                # add button to last column
                self.datasets_table.setCellWidget(row_index, 3, delete_button)




    def delete_dataset_from_db(self, dataset_id):
        delete_dataset(dataset_id)

        data = load_all_datasets()
        self.populate_table(data)

    


        



  
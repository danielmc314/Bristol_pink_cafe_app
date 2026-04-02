from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QDateEdit, QFileDialog, QLineEdit, QMessageBox, QTableWidget, QComboBox,
    QTableWidgetItem, QHeaderView, QStackedWidget)
from PySide6.QtCore import QDate, Qt

from database.data_loader import clean_combined_data, single_data_set
from database.database_manager import insert_dataset, insert_sales, load_datasets, delete_dataset, load_all_datasets, load_models, delete_model, load_all_models





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

        manage_database_row = QHBoxLayout()
        manage_database_row.setSpacing(15)


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

        database_selection_layout = QVBoxLayout()

        database_selection_label = QLabel("Delect Database:")
        self.database_selection_dropdown = QComboBox()
        self.database_selection_dropdown.setFixedWidth(field_width)
        self.database_selection_dropdown.setFixedHeight(field_height)
        self.database_selection_dropdown.addItem("Models", "models")
        self.database_selection_dropdown.addItem("Datasets", "datasets")

        database_selection_layout.addWidget(database_selection_label)
        database_selection_layout.addWidget(self.database_selection_dropdown)

        self.apply_button = QPushButton("Apply Filter")
        self.apply_button.setFixedWidth(field_width)
        self.apply_button.setFixedHeight(field_height)
        self.apply_button.clicked.connect(self.filter_datasets)
        
        manage_database_row.addLayout(start_layout)
        manage_database_row.addLayout(end_layout)
        manage_database_row.addLayout(database_selection_layout)
        manage_database_row.addWidget(self.apply_button, alignment=Qt.AlignBottom)
        manage_database_row.addStretch()

        manage_database_row.addStretch()

        main_layout.addLayout(manage_database_row)

        #-------------table row---------------

        dataset_table_row = QVBoxLayout()
        
        #create a tablew stack containing models table and dataset table
        self.table_stack = QStackedWidget()

        self.datasets_table = QTableWidget()
        self.datasets_table.setColumnCount(4)
        self.datasets_table.setHorizontalHeaderLabels(
            ["Dataset ID", "Dataset Name", "Upload Date", "delete"]
        )

        self.datasets_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.datasets_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.datasets_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.datasets_table.setAlternatingRowColors(True)

        self.models_table = QTableWidget()
        self.models_table.setColumnCount(5)
        self.models_table.setHorizontalHeaderLabels(
            ["Model_id", "generated on", "model_name", "mae", "delete"]
        )

        self.models_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.models_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.models_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.models_table.setAlternatingRowColors(True)

        self.table_stack.addWidget(self.datasets_table)
        self.table_stack.addWidget(self.models_table)

        main_layout.addWidget(self.table_stack)




        
        
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
    
    #sets which table to be viewable dependent on the selection in database_selection_dropdown
    def switch_table(self):
        selected = self.database_selection_dropdown.currentData()

        if selected == "datasets":
            self.table_stack.setCurrentWidget(self.datasets_table)
        else:
            self.table_stack.setCurrentWidget(self.models_table)
        

    def filter_datasets(self):
        #get variables from imput fields
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        database = self.database_selection_dropdown.currentData()

        #set the correct table in table_stack for data 
        self.switch_table()

        #get datasets that satisfy variables
        if database == "datasets":
            data = load_datasets(start_date, end_date)
        elif database == "models":
            data = load_models(start_date, end_date)
        
        self.populate_table(data, database)




    def populate_table(self, data, database):
        #make sure table is clear before loading new datasets
        if database == "datasets":
            table = self.datasets_table
        else:
            table = self.models_table

        table.clearContents()
        table.setRowCount(len(data))

        for row_index, row in enumerate(data):
            for col_index, value in enumerate(row):

                if database == "datasets":
                    self.datasets_table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

                    row_dataset_id = row[0]

                    #create delete button
                    delete_button = QPushButton("Delete")
    
                    # connect button with row specific action
                    delete_button.clicked.connect(
                        lambda checked, dataset_id = row_dataset_id: self.delete_dataset_from_db(dataset_id)
                    )

                    # add button to last column
                    self.datasets_table.setCellWidget(row_index, 3, delete_button)
                elif database == "models":
                    self.models_table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

                    row_model_id = row[0]

                    #create delete button
                    delete_button = QPushButton("Delete")

                    #connect button with row specific action
                    delete_button.clicked.connect(
                        lambda checked, model_id = row_model_id: self.delete_model_from_db(model_id)
                    )

                    #add button to last column
                    self.models_table.setCellWidget(row_index, 4, delete_button)




    def delete_dataset_from_db(self, dataset_id):
        delete_dataset(dataset_id)

        data = load_all_datasets()
        self.populate_table(data, "datasets")

    def delete_model_from_db(self, model_id):
        delete_model(model_id)

        data = load_all_models()
        self.populate_table(data, "models")

    


        



  
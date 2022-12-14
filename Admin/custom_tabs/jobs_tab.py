from PySide6.QtWidgets import (QTreeView, QAbstractItemView,QHeaderView, QVBoxLayout, QMenu, QApplication)
from PySide6.QtCore import (Qt, QRect, QModelIndex, QItemSelectionModel, QAbstractItemModel)
from PySide6.QtGui import (QStandardItemModel, QStandardItem, QColor, QPalette, QBrush, QFont, QPainter, QKeySequence)
from consts import JobStatus
import uuid
import ast

from collections import defaultdict
from tabulate import tabulate
from .ui_classes import TreeView, StandardItem

class JobView(QVBoxLayout):
    def __init__(self, db_conn, db_cur, main, parent=None):
        super(JobView, self).__init__(parent)

        # Create a model
        self.tree_view = TreeView()

        self.tree_model = QStandardItemModel()
        self.tree_model
        label_type = StandardItem('Type',10,False)
        label_projectid = StandardItem('Project ID',10,False)
        label_version= StandardItem('Version',10,False)
        label_remaining = StandardItem('Remaining',10,False)
        label_count = StandardItem('Total',10,False)
        label_assigner = StandardItem('Assigner',10,False)
        label_priority = StandardItem('Priority',10,False)
        label_status = StandardItem('Status',10,False)
        label_starttime = StandardItem('Start Time',10,False)
        label_uuid = StandardItem('UUID',10,False)
        label_endtime = StandardItem('Finish Time',10,False)
        label_workers = StandardItem('Workers',10,False)
        #add label to tree model
        self.tree_model.setHorizontalHeaderItem(0, label_type)
        self.tree_model.setHorizontalHeaderItem(1, label_projectid)
        self.tree_model.setHorizontalHeaderItem(2, label_version)
        self.tree_model.setHorizontalHeaderItem(3, label_remaining)
        self.tree_model.setHorizontalHeaderItem(4, label_count)
        self.tree_model.setHorizontalHeaderItem(5, label_assigner)
        self.tree_model.setHorizontalHeaderItem(6, label_priority)
        self.tree_model.setHorizontalHeaderItem(7, label_status)
        self.tree_model.setHorizontalHeaderItem(8, label_starttime)
        self.tree_model.setHorizontalHeaderItem(9, label_endtime)
        self.tree_model.setHorizontalHeaderItem(10,label_workers)
        self.tree_model.setHorizontalHeaderItem(11, label_uuid)

        self.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)
        self.tree_view.setFixedWidth(1020)
        self.tree_view.setFixedHeight(570)
        self.tree_view.setRootIsDecorated(False)
        
        # Get the jobs
        self.db_cur = db_cur
        self.db_conn = db_conn
        self.main = main

        # self.hide_columns()
        self.tree_view.sortByColumn(8, Qt.SortOrder.DescendingOrder)

        self.tree_view.setModel(self.tree_model)
        self.hide_columns()
        self.addWidget(self.tree_view)

        # Create a right click item on standard item
        self.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.right_click_menu)

        # Bind ctrl+v to copy job uuid
        self.tree_view.keyPressEvent = self.keyPressEvent


    def keyPressEvent(self, event):
        """This function is used to bind ctrl+v to copy job uuid"""
        if event.matches(QKeySequence.Copy):
            self.copy_selected_job_uuid()


    def refresh(self):
        # This hides the columns uuid and workers

        if self.main.admin is None:
            return

        if self.tree_view.selectionModel():
            self.tree_view.selectionModel().selectionChanged.connect(self.main.selection_of_workers_for_job)

        self.remove_deleted_jobs()

        # We don't want to get data column
        # TODO maybe there is a better way of getting all columns except one
        self.db_cur.execute("""SELECT type, project_id, version, status, remaining, count, assigner, priority, start_time, job_uuid, end_time, workers FROM "Jobs" """)
        jobs = self.db_cur.fetchall()

        for job in jobs:
            job_uuid = job["job_uuid"]

            # Update the remaining column
            job_type = job["type"]
            job_projid = job["project_id"]
            job_version = job["version"]
            job_remaining = job["remaining"]
            job_count = job["count"]
            job_assigner = job["assigner"]
            job_priority = job["priority"]
            job_starttime = job["start_time"]
            job_status = job["status"]
            job_endtime = job["end_time"]
            job_workers = job["workers"]

            display_color = None

            if job_status == JobStatus.CANCELLED.value:
                display_color = QColor(82, 92, 104)
            elif job_status == JobStatus.COMPLETED.value:
                display_color = QColor(87, 148, 61)
            elif job_status == JobStatus.INPROGRESS.value:
                display_color = QColor(34, 166, 179)
            elif job_status == JobStatus.PAUSED.value:
                display_color = QColor(255, 190, 118)
            elif job_status == JobStatus.FAILED.value:
                display_color = QColor(235, 77, 75)
            elif job_status == JobStatus.NOTSTARTED.value:
                display_color = QColor(0, 102, 102)
            else:
                display_color = QColor(0, 0, 0)

            # Make colors darker
            if display_color is not None:
                display_color = display_color.darker(135)

            item_type = StandardItem(job_type, set_background_color=display_color)
            item_projid = StandardItem(job_projid, set_background_color=display_color)
            item_version = StandardItem(job_version, set_background_color=display_color)
            item_remaining = StandardItem(job_remaining, set_background_color=display_color)
            item_count = StandardItem(job_count, set_background_color=display_color)
            item_assigner = StandardItem(job_assigner, set_background_color=display_color)
            item_priority = StandardItem(job_priority, set_background_color=display_color)
            item_status = StandardItem(job_status, set_background_color=display_color)
            item_starttime = StandardItem(job_starttime, set_background_color=display_color)
            item_uuid = StandardItem(job_uuid, set_background_color=display_color)
            item_endtime = StandardItem(job_endtime, set_background_color=display_color)
            item_workers = StandardItem(job_workers, set_background_color=display_color)

            found = False
            for row in range(self.tree_model.rowCount()):
                rowuuid = self.tree_model.item(row, 11)


                if rowuuid.text() == str(job_uuid):
                    found = True
                    self.tree_model.setItem(row, 0, item_type)
                    self.tree_model.setItem(row, 1, item_projid)
                    self.tree_model.setItem(row, 2, item_version)
                    self.tree_model.setItem(row, 3, item_remaining)
                    self.tree_model.setItem(row, 4, item_count)
                    self.tree_model.setItem(row, 5, item_assigner)
                    self.tree_model.setItem(row, 6, item_priority)
                    self.tree_model.setItem(row, 7, item_status)
                    self.tree_model.setItem(row, 8, item_starttime)
                    self.tree_model.setItem(row, 9, item_endtime)
                    self.tree_model.setItem(row, 10, item_workers)
                    self.tree_model.setItem(row, 11, item_uuid)

            if not found:
                print("Adding new row")
                self.tree_model.appendRow([item_type, item_projid, item_version, item_remaining, item_count, item_assigner, item_priority,item_status, item_starttime, item_endtime, item_workers, item_uuid])
            self.addWidget(self.tree_view)


    def get_selected_jobs(self):
        selected_uuids = []
        selected_indexes = self.tree_view.selectedIndexes()

        jobs = defaultdict(list)
        
        if len(selected_indexes) > 0:
            for index in selected_indexes:
                job_uuid = self.tree_model.item(index.row(), 11).text()
                if uuid.UUID(job_uuid) not in selected_uuids:
                    # Convert the string to a UUID
                    selected_uuids.append(uuid.UUID(job_uuid))
                    jobs["type"].append(self.tree_model.item(index.row(), 0).text())
                    jobs["projid"].append(self.tree_model.item(index.row(), 1).text())
                    jobs["ver"].append(self.tree_model.item(index.row(), 2).text())



        tabular_job = tabulate(jobs, headers="keys", tablefmt="github")

        jobinfo = f"```{tabular_job}```"
        
        return selected_uuids, jobinfo
    
    def get_selected_jobs_workers(self):
        selected_indexes = self.tree_view.selectedIndexes()        
        
        sel_workers = []
        if len(selected_indexes) > 0:
            for index in selected_indexes:
                row_workers_str = self.tree_model.item(index.row(), 10).text()
                
                if row_workers_str:
                    row_workers = ast.literal_eval(row_workers_str)
                    if row_workers:
                        row_workers = [x.strip() for x in row_workers]
                        sel_workers.extend(row_workers)          
        else:
            return []

        return list(set(sel_workers))

    def hide_columns(self):
        self.tree_view.setColumnHidden(10, True)
        self.tree_view.setColumnHidden(11, True)
    
    def clear_job_history(self):
        if self.main.admin is not None:
            CLEAR_JOBS = """DELETE FROM "Jobs" WHERE status=%s or status=%s or status=%s"""
            self.db_cur.execute(CLEAR_JOBS, (JobStatus.COMPLETED.value, JobStatus.CANCELLED.value, JobStatus.FAILED.value))
            self.db_conn.commit()
            self.refresh()
        else:
            self.main.open_rusure("You must be an admin to clear the job history")

    def remove_deleted_jobs(self):
        to_remove = []
        for row in range(self.tree_model.rowCount()):
            rowuuid = self.tree_model.item(row, 11)
            CHECK_JOB_EXITST = """SELECT job_uuid FROM "Jobs" WHERE job_uuid = %s"""
            self.db_cur.execute(CHECK_JOB_EXITST, (rowuuid.text(),))
            job_exists = self.db_cur.fetchone()
            if job_exists is None or len(job_exists) == 0:
                print("JOB DOESNT EXIST", job_exists)
                to_remove.append(row)

        for row in to_remove:
            self.tree_model.removeRow(row)

        return
    def right_click_menu(self, position):
        menu = QMenu()
        menu.addAction("Copy Job UUID", self.copy_selected_job_uuid)

        menu.exec_(self.tree_view.viewport().mapToGlobal(position))

    def copy_selected_job_uuid(self):
        selected_indexes = self.tree_view.selectedIndexes()
        job_uuids = []
        if len(selected_indexes) > 0:
            for index in selected_indexes:
                job_uuid = self.tree_model.item(index.row(), 11).text()
                job_uuids.append(job_uuid)

        QApplication.clipboard().setText(", ".join(set(job_uuids)))

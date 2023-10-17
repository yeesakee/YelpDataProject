import sys
import psycopg2
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap


qtCreatorFile = "milestone3.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone1(QMainWindow):
    def __init__(self):
        super(milestone1, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # first load list of states
        self.loadStateList()

        # if stateList changes, update business table based on chosen state
        self.ui.stateList.currentTextChanged.connect(self.selectedState)

        # if cityList changes, update business table based on chosen city
        self.ui.cityList.itemSelectionChanged.connect(self.selectedCity)

        # if categoryList changes, update business tabled based on chosen category
        self.ui.categoryList.itemSelectionChanged.connect(self.getCategoryBusiness)

        self.ui.zipcodeList.itemSelectionChanged.connect(self.getAllZipData)

    def executeQuery(self, sql_str):
        try:
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='postgres'")
        except:
            print('Unable to connect to database')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        # clear items in combo box initially
        self.ui.stateList.clear()
        sql_str = "select distinct state_id from city ORDER BY state_id ASC;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("state query failed")
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def selectedState(self):
        # clear items in combo box initially
        self.ui.cityList.clear()
        state = self.ui.stateList.currentText()
        # only execute if there is a state loaded/selected in the statelist object
        if (self.ui.stateList.currentIndex() >= 0):
            sql_str = "SELECT distinct city_name FROM city WHERE city.state_id ='" + state + "' ORDER BY city_name;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("city query failed")
            
            # remove all content from businesstable
            for i in reversed (range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            sql_str = "select distinct business.name, business.address, city.city_name, business.stars, business.review_count, business.reviewrating, business.numcheckins FROM business, city, state WHERE city.state_id = '" + state + "' AND business.city_id = city.city_id AND city.state_id = state.state_id ORDER BY name;"
            self.businessTableUpdate(sql_str)
    
    def selectedCity(self):
        if (self.ui.stateList.currentIndex() >= 0 and (len(self.ui.cityList.selectedItems()) > 0)):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            sql_str = "select distinct business.name, business.address, city.city_name, business.stars, business.review_count, business.reviewrating, business.numcheckins FROM business, city, state WHERE city.state_id = '" + state + "' AND city.city_name = '" + city + "' AND business.city_id = city.city_id AND city.state_id = state.state_id ORDER BY name;"
            self.businessTableUpdate(sql_str)
            self.getBusinessCategories(state, city)
            self.getZipCodes(state+city)

    def businessTableUpdate(self, sql_str):
        try:
            results = self.executeQuery(sql_str)
            style = "::section {""background-color: #f3f3f3; }"
            self.ui.businessTable.horizontalHeader().setStyleSheet(style)
            self.ui.businessTable.setColumnCount(len(results[0]))
            self.ui.businessTable.setRowCount(len(results))
            self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', 'Number of Checkins'])
            self.ui.businessTable.resizeColumnsToContents()
            self.ui.businessTable.setColumnWidth(0, 200)
            self.ui.businessTable.setColumnWidth(1, 120)
            self.ui.businessTable.setColumnWidth(2, 50)
            currentRowCount = 0
            for row in results:
                for col in range(0, len(results[0])):
                    data = row[col]
                    if (type(data) == float):
                        data = round(data, 2)
                    data = str(data)
                    self.ui.businessTable.setItem(currentRowCount, col, QTableWidgetItem(data))
                currentRowCount += 1
        except:
            print("business query failed")
    
    def getBusinessCategories(self, state, city):
        self.ui.categoryList.clear()
        sql_str = "select distinct businesscategory.category_name FROM business, businesscategory, city WHERE business.bid = businesscategory.bid AND business.city_id = city.city_id AND city.city_name = '" + city + "' AND city.state_id = '" + state + "' ORDER BY category_name"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.categoryList.addItem(row[0])
        except:
            print("business category query failed")
    
    def getCategoryBusiness(self):
        if (self.ui.stateList.currentIndex() >= 0 and (len(self.ui.cityList.selectedItems()) > 0) and (len(self.ui.categoryList.selectedItems()) > 0)):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            category = self.ui.categoryList.selectedItems()[0].text()
            sql_str = "select distinct business.name, business.address, city.city_name, business.stars, business.review_count, business.reviewrating, business.numcheckins FROM business, city, state, businesscategory WHERE city.state_id = '" + state + "' AND city.city_name = '" + city + "' AND businesscategory.category_name = '" + category + "' AND business.city_id = city.city_id AND city.state_id = state.state_id AND businesscategory.bid = business.bid ORDER BY name;"
            self.businessTableUpdate(sql_str)
    
    def getZipCodes(self, city_id):
        self.ui.zipcodeList.clear()
        sql_str = "select distinct zid FROM cityzip WHERE cityzip.city_id = '" + city_id + "' ORDER BY zid ASC"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.zipcodeList.addItem(str(row[0]))
        except:
            print("zipcodes query failed")
    
    def getAllZipData(self):
        if (len(self.ui.zipcodeList.selectedItems()) > 0):
            zid = self.ui.zipcodeList.selectedItems()[0].text()
            sql_str = "select distinct business.name, business.address, city.city_name, business.stars, business.review_count, business.reviewrating, business.numcheckins FROM business, city, state WHERE business.zipcode_id = '" + zid + "' AND business.city_id = city.city_id AND city.state_id = state.state_id ORDER BY name;"
            self.businessTableUpdate(sql_str)
            self.getBusinessCount(zid)
            self.getTotalPop(zid)
            self.getAvgIncome(zid)
            self.getTopCategories(zid)
            self.getPopularBusinesses(zid)
            self.getSuccessfulBusiness(zid)

    def getBusinessCount(self, zid):
        self.ui.numBusinesses.clear()
        sql_str = "select COUNT(*) FROM business WHERE business.zipcode_id = '" + zid + "'"
        try:
            results = self.executeQuery(sql_str)
            self.ui.numBusinesses.setText(str(results[0][0]))
        except:
            print("# of business query failed")
    
    def getTotalPop(self, zid):
        self.ui.totalPop.clear()
        sql_str = "select zipcode_data.population from zipcode_data, cityzip where cityzip.zid = zipcode_data.zid AND cityzip.zid = '" + zid + "'"
        try:
            results = self.executeQuery(sql_str)
            self.ui.totalPop.setText(str(results[0][0]))
        except:
            print("total population zip query failed")

    def getAvgIncome(self, zid):
        self.ui.avgIncome.clear()
        sql_str = "select zipcode_data.mean_income from zipcode_data, cityzip where cityzip.zid = zipcode_data.zid AND cityzip.zid = '" + zid + "'"
        try:
            results = self.executeQuery(sql_str)
            self.ui.avgIncome.setText(str(results[0][0]))
        except:
            print("average income zip query failed")

    def getTopCategories(self, zid):
        sql_str = "SELECT COUNT(*), businesscategory.category_name FROM business, businesscategory WHERE business.bid = businesscategory.bid AND business.zipcode_id = '" + zid + "' GROUP BY businesscategory.category_name ORDER BY COUNT(*) DESC;"
        try:
            results = self.executeQuery(sql_str)
            style = "::section {""background-color: #f3f3f3; }"
            self.ui.topCategories.horizontalHeader().setStyleSheet(style)
            self.ui.topCategories.setColumnCount(len(results[0]))
            self.ui.topCategories.setRowCount(len(results))
            self.ui.topCategories.setHorizontalHeaderLabels(['# of Business', 'Category'])
            self.ui.popularTable.setColumnWidth(0, 80)
            self.ui.popularTable.setColumnWidth(1, 130)
            currentRowCount = 0
            for row in results:
                for col in range(0, len(results[0])):
                    data = str(row[col])
                    self.ui.topCategories.setItem(currentRowCount, col, QTableWidgetItem(data))
                currentRowCount += 1
        except:
            print("top categories zip query failed")
        
    def getPopularBusinesses(self, zid):
        sql_str = "select distinct name, stars, review_count, numcheckins from business where business.zipcode_id = '" + zid + "' ORDER BY business.numcheckins DESC"
        try:
            results = self.executeQuery(sql_str)
            results = self.filterPopularBusiness(results)
            style = "::section {""background-color: #f3f3f3; }"
            self.ui.popularTable.horizontalHeader().setStyleSheet(style)
            self.ui.popularTable.setColumnCount(len(results[0]))
            self.ui.popularTable.setRowCount(len(results))
            self.ui.popularTable.setHorizontalHeaderLabels(['Business Name', 'Stars', '# of Reviews', '# of Checkins'])
            self.ui.popularTable.resizeColumnsToContents()
            self.ui.popularTable.setColumnWidth(0, 130)
            
            currentRowCount = 0
            for row in results:
                for col in range(0, len(results[0])):
                    data = row[col]
                    if (type(data) == float):
                        data = round(data, 2)
                    data = str(data)
                    self.ui.popularTable.setItem(currentRowCount, col, QTableWidgetItem(data))
                currentRowCount += 1
        except:
            print("popular businesses query failed.")
    
    def getSuccessfulBusiness(self, zid):
        sql_str = "select distinct name, stars, review_count, reviewrating, numcheckins from business where business.zipcode_id = '" + zid + "' ORDER BY business.numcheckins DESC"
        try:
            results = self.executeQuery(sql_str)
            results = self.filterSuccessfulBusiness(results)
            style = "::section {""background-color: #f3f3f3; }"
            self.ui.successTable.horizontalHeader().setStyleSheet(style)
            self.ui.successTable.setColumnCount(len(results[0]))
            self.ui.successTable.setRowCount(len(results))
            self.ui.successTable.setHorizontalHeaderLabels(['Business Name', 'Stars', '# of Reviews', 'Avg Review Rating', '# of Checkins'])
            self.ui.successTable.resizeColumnsToContents()
            self.ui.successTable.setColumnWidth(0, 130)
            
            currentRowCount = 0
            for row in results:
                for col in range(0, len(results[0])):
                    data = row[col]
                    if (type(data) == float):
                        data = round(data, 2)
                    data = str(data)
                    self.ui.successTable.setItem(currentRowCount, col, QTableWidgetItem(data))
                currentRowCount += 1
        except:
            print("success businesses query failed.")
    
    def filterPopularBusiness(self, results):
        # filter for top 50% businesses with highest checkins
        results = results[:len(results)//2]
        popular = []
        avg_reviews = 0
        for business in results:
            # review_count is at index 2
            avg_reviews += business[2]
        avg_reviews = avg_reviews // len(results)
        for business in results:
            if (business[2] < avg_reviews and business[3] != None):
                popular.append(business)
        if (len(popular) == 0):
            popular = results[:len(results)//2]
        return popular

    def filterSuccessfulBusiness(self, results):
        # filter for top 50% businesses with highest checkins
        results = results[:len(results)//2]
        success = []
        avg_reviews = 0
        avg_reviewrating = 0
        for business in results:
            # review_count is at index 2
            avg_reviews += business[2]

            # review_rating is at index 3
            avg_reviewrating += business[3]

        avg_reviews = avg_reviews // len(results)
        avg_reviewrating = avg_reviewrating // len(results)

        for business in results:
            if (business[2] > avg_reviews and business[3] > avg_reviewrating and business[4] != None):
                success.append(business)
        if (len(success) == 0):
            success = results[:len(results)//2]
        return success
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone1()
    window.show()
    sys.exit(app.exec_())
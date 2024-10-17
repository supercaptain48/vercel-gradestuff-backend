from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

headers = {
    "Host": "hac.friscoisd.org",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0",
    'X-Requested-With': 'XMLHttpRequest',
    "Origin": "https://hac.friscoisd.org",
}


loginurl = ('https://hac.friscoisd.org/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f')
studentInfo = ('https://hac.friscoisd.org/HomeAccess/Content/Student/Registration.aspx')
transcripturl = ('https://hac.friscoisd.org/HomeAccess/Content/Student/Transcript.aspx')
scheduleurl = ("https://hac.friscoisd.org/HomeAccess/Content/Student/Classes.aspx")
assignmentsurl = ("https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx")

app = Flask(__name__)


def get_session(username, password):
    with requests.session() as s:
        r = s.get(loginurl).text
        html = BeautifulSoup(r, 'html.parser')
        token = html.find('input', {'name': '__RequestVerificationToken'}).attrs['value']
        custom3 = html.find('input', {'name': 'SCKTY00328510CustomEnabled'}).attrs['value']
        custom4 = html.find('input', {'name': 'SCKTY00436568CustomEnabled'}).attrs['value']
        database = html.find('input', {'name': 'Database'}).attrs['value']
        verification = html.find('input', {'name': 'VerificationOption'}).attrs['value']
    
    payload = {
        '__RequestVerificationToken': token,
        # 'SCKTY00328510CustomEnabled': custom3,
        # 'SCKTY00436568CustomEnabled': custom4,
        'Database': database,
        'VerificationOption': verification,
        'LogOnDetails.UserName': username,
        'LogOnDetails.Password': password
    }

    res = s.post(loginurl, data=payload, headers=headers)

    return s


def get_name(s):
    r = s.get(studentInfo)
    soup = BeautifulSoup(r.content, 'html.parser')

    name = soup.find(id='plnMain_lblRegStudentName').text

    return name


def scrape_studentInfo(s):
    r = s.get(studentInfo)
    soup = BeautifulSoup(r.content, 'html.parser')

    name = soup.find(id='plnMain_lblRegStudentName').text
    grade = soup.find(id='plnMain_lblGrade').text

    dict = {
        "name": name,
        "grade": grade
    }

    return dict


def scrape_assignments(s, quarter):
    r = s.get(assignmentsurl)
    soup = BeautifulSoup(r.content, 'html.parser')

    viewstate = soup.find('input', {'name': '__VIEWSTATE'}).attrs['value']
    validation = soup.find('input', {'name': '__EVENTVALIDATION'}).attrs['value']
    payload = {
        "__EVENTTARGET": "ctl00$plnMain$btnRefreshView",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": viewstate,
        "__VIEWSTATEGENERATOR": "B0093F3C",
        "__EVENTVALIDATION": validation,
        "ctl00$plnMain$hdnValidMHACLicense": "Y",
        "ctl00$plnMain$hdnIsVisibleClsWrk": "N",
        "ctl00$plnMain$hdnIsVisibleCrsAvg": "N",
        "ctl00$plnMain$hdnJsAlert": "Averages+cannot+be+displayed+when++Report+Card+Run+is+set+to+(All+Runs).",
        "ctl00$plnMain$hdnTitle": "Classwork",
        "ctl00$plnMain$hdnLastUpdated": "Last+Updated",
        "ctl00$plnMain$hdnDroppedCourse": "+This+course+was+dropped+as+of+",
        "ctl00$plnMain$hdnddlClasses": "(All+Classes)",
        "ctl00$plnMain$hdnddlCompetencies": "(All+Classes)",
        "ctl00$plnMain$hdnCompDateDue": "Date+Due",
        "ctl00$plnMain$hdnCompDateAssigned": "Date+Assigned",
        "ctl00$plnMain$hdnCompCourse": "Course",
        "ctl00$plnMain$hdnCompAssignment": "Assignment",
        "ctl00$plnMain$hdnCompAssignmentLabel": "Assignments+Not+Related+to+Any+Competency",
        "ctl00$plnMain$hdnCompNoAssignments": "No+assignments+found",
        "ctl00$plnMain$hdnCompNoClasswork": "Classwork+could+not+be+found+for+this+competency+for+the+selected+report+card+run.",
        "ctl00$plnMain$hdnCompScore": "Score",
        "ctl00$plnMain$hdnCompPoints": "Points",
        "ctl00$plnMain$hdnddlReportCardRuns1": "(All+Runs)",
        "ctl00$plnMain$hdnddlReportCardRuns2": "(All+Terms)",
        "ctl00$plnMain$hdnbtnShowAverage": "Show+All+Averages",
        "ctl00$plnMain$hdnShowAveragesToolTip": "Show+all+student's+averages",
        "ctl00$plnMain$hdnPrintClassworkToolTip": "Print+all+classwork",
        "ctl00$plnMain$hdnPrintClasswork": "Print+Classwork",
        "ctl00$plnMain$hdnCollapseToolTip": "Collapse+all+courses",
        "ctl00$plnMain$hdnCollapse": "Collapse+All",
        "ctl00$plnMain$hdnFullToolTip": "Switch+courses+to+Full+View",
        "ctl00$plnMain$hdnViewFull": "Full+View",
        "ctl00$plnMain$hdnQuickToolTip": "Switch+courses+to+Quick+View",
        "ctl00$plnMain$hdnViewQuick": "Quick+View",
        "ctl00$plnMain$hdnExpand": "Expand+All",
        "ctl00$plnMain$hdnExpandToolTip": "Expand+all+courses",
        "ctl00$plnMain$hdnChildCompetencyMessage": "This+competency+is+calculated+as+an+average+of+the+following+competencies",
        "ctl00$plnMain$hdnCompetencyScoreLabel": "Grade",
        "ctl00$plnMain$hdnAverageDetailsDialogTitle": "Average+Details",
        "ctl00$plnMain$hdnAssignmentCompetency": "Assignment+Competency",
        "ctl00$plnMain$hdnAssignmentCourse": "Assignment+Course",
        "ctl00$plnMain$hdnTooltipTitle": "Title",
        "ctl00$plnMain$hdnCategory": "Category",
        "ctl00$plnMain$hdnDueDate": "Due+Date",
        "ctl00$plnMain$hdnMaxPoints": "Max+Points",
        "ctl00$plnMain$hdnCanBeDropped": "Can+Be+Dropped",
        "ctl00$plnMain$hdnHasAttachments": "Has+Attachments",
        "ctl00$plnMain$hdnExtraCredit": "Extra+Credit",
        "ctl00$plnMain$hdnType": "Type",
        "ctl00$plnMain$hdnAssignmentDataInfo": "Information+could+not+be+found+for+the+assignment",
        "ctl00$plnMain$ddlReportCardRuns": f"{quarter}-2025",
        "ctl00$plnMain$ddlClasses": "ALL",
        "ctl00$plnMain$ddlCompetencies": "ALL",
        "ctl00$plnMain$ddlOrderBy": "Class"
    }
    payload2={"ctl00$plnMain$ddlReportCardRuns": "6-2025"}

    # Get student's classes and grades
    s.get(assignmentsurl)
    if int(quarter) > 0:
        r = s.post(assignmentsurl, data=payload, headers=headers)
        print(r.status_code)
        soup = BeautifulSoup(r.content, 'html.parser')
    else:
        r = s.get(assignmentsurl)
        soup = BeautifulSoup(r.content, 'html.parser')

    courseList = []

    quarter = soup.find("option", {"selected": "selected"}).text.strip()

    courses = soup.find_all("div", {"class": "AssignmentClass"})

    string = "abcd"
    string[2:]

    for course in courses:
        dict = {}
        dict["name"] = course.find("a", {"class": "sg-header-heading"}).text.strip()
        index = dict["name"].find("  ")
        dict["name"] = dict["name"][index:]
        while dict["name"][0] == " ":
            dict["name"] = dict["name"][1:]
        
        dict["grade"] = course.find("span", {"class": "sg-header-heading sg-right"}).text.strip().replace("Student Grades ", "").replace("%", "")

        dict["assignments"] = []
        assignments = course.find_all("tr", {"class": "sg-asp-table-data-row"})
        #print(assignments)
        for assignment in assignments:
            try:
                tds = assignment.find_all("td")
                assignmentName = assignment.find("a").text.strip()
                assignmentCategory = tds[3].text.strip()
                assignmentGrade = tds[4].text.strip()
                dict["assignments"].append({
                    "name": assignmentName,
                    "category": assignmentCategory,
                    "score": assignmentGrade
                })
            except:
                pass

        courseList.append(dict)
    
    return {"grades": courseList, "quarter": quarter}


def scrape_transcript(s):
    r = s.get(transcripturl)
    soup = BeautifulSoup(r.content, 'html.parser')

    transcript = []

    years = soup.find_all("td", {"class": "sg-transcript-group"})
    for i, year in enumerate(years):
        dict = {}

        dict["gradeLevel"] = soup.find(id=f'plnMain_rpTranscriptGroup_lblGradeValue_{i}').text.strip()
        dict["courses"] = []

        courses = year.find_all("tr", {"class": "sg-asp-table-data-row"})
        for course in courses:
            tds = course.find_all("td")
            courseName = tds[1].text.strip()
            sem1Grade = tds[2].text.strip()
            sem2Grade = tds[3].text.strip()
            dict["courses"].append({
                "courseName": courseName,
                "sem1Grade": sem1Grade,
                "sem2Grade": sem2Grade
            })
        
        transcript.append(dict)

    return transcript


def get_schedule(s):
    r = s.get(scheduleurl)
    soup = BeautifulSoup(r.content, 'html.parser')

    courseList = []

    courses = soup.find_all("tr", {"class": "sg-asp-table-data-row"})
    for course in courses:
        dict = {}

        tds = course.find_all("td")

        if len(tds) > 3:
            courseName = tds[1].text.strip()
            periods = tds[2].text.strip()
            teacher = tds[3].text.strip()
            room = tds[4].text.strip()
            days = tds[5].text.strip()

            dict["courseName"] = courseName
            dict["periods"] = periods
            dict["teacher"] = teacher
            dict["room"] = room
            dict["days"] = days

            courseList.append(dict)

    return courseList


@app.route("/")
def home():
    return "Backend for gradestuff app"


@app.route("/startup-username=<username>&password=<password>/")
def get_user(username, password):
    # Login to HAC and create a dictionary to hold all scraped data
    s = get_session(username, password)
    data = {}

    data["name"] = get_name(s)
    data["class"] = scrape_assignments(s, 0)
    data["transcript"] = scrape_transcript(s)
    data["schedule"] = get_schedule(s)

    return jsonify(data), 200


@app.route("/studentinfo-username=<username>&password=<password>/")
def get_info(username, password):
    s = get_session(username, password)
    data = scrape_studentInfo(s)

    return jsonify(data), 200


@app.route("/gpa-username=<username>&password=<password>/")
def get_gpa(username, password):
    s = get_session(username, password)
    assignments = []

    assignments.append(scrape_assignments(s, 0))
    transcript = scrape_transcript(s)

    while int(assignments[-1]["quarter"]) > 1:
        assignments.append(scrape_assignments(s, int(assignments[-1]["quarter"]) - 1))

    data = {"current": assignments, "transcript": transcript}

    return jsonify(data), 200


@app.route("/assignments-username=<username>&password=<password>/")
def get_assignments(username, password):
    s = get_session(username, password)

    quarter = request.args.get("quarter")
    if quarter:
        data = scrape_assignments(s, quarter)
    else:
        data = scrape_assignments(s, 0)

    return jsonify(data), 200


@app.route("/transcript-username=<username>&password=<password>/")
def get_transcript(username, password):
    s = get_session(username, password)
    data = scrape_transcript(s)

    return jsonify(data), 200


if __name__ == "__main__":
    app.run(debug=True)


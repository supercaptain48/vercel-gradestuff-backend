from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
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


def get_assignments(s):
    payload = {
        "__EVENTTARGET": "ctl00$plnMain$btnRefreshView",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": "LrwyU5yvYWT289iRj/pNNwKZo2O+X8qP/hQ8LiPPlKbn5kpP642NF+6ouiPmZ59iZBEpbmk/Y5PZ2ovVtvcsI+da4vo8CJLh7oJKSCYXiTGc8Av88+cVihwOjQT6RELHYNgD8OU3B3uwxpTDdqcn4fyAuEkpQI+u9CEpYVqW3pJ4CdbN6AhhtYVi3ZwGqI/2uhthxYVLRDrxkoUMqQ4IHhgdYlCL5GKBQJkkzkCadlGgbOd1e1ZyQP/zcrADZXyTRV72Zs+Ky7V0GtdB5xVay5AD39My0OjQkNHKOanilrh0nN49tAIY1iV51cd9H40k01hNg+pAP98dfxsY5wG+AJjxTMc+qnimG2f+QGjGwhZOnn6+0PceapFMxP/7Ov70dYdbhprm6kvzyhw+0BE11yS8e35LMDyJI6/X1uhwwsEEkPQjKLnK2yZZzGxXL4grlVgAuAsRmPEJGlyRAnNMbQp9d5VU0AzJnGeqds9MqaRCxOBiafya8ZOY4TZFswdGSo+R0MmFeRwdUydfcXpgSZcgi6P2RGvIT6eKTXbmLiWAU3n/VB6Nz8xw2sCdH/pX1PPFwyzj/V+laZpgNCN5lfsnvfkJ2fW4Alv8nnWV087x/ki8TnxWEsZnDH+J5V2DwicbavJMW9rpYbrvdMVYoK7yzf3SJVOyekK6xGa9R3b5ea5MO6jMYgmOhG6Xi/Pi9TQnwjLNbtl4FaBBHP8aSbeIvHJmXtDKiBY4Ku3N432I8XgLuCd5d6AsZjh9DsZQqwsK+eSkU8Jeaos9HYgmzV6pT9/nm7+AbX3g0LzXqxSLWMiAYhl0T7cTVE92NO+i+A5915ejzaFCXPqxV7FSg5eyPS8R9l5lp7KquFAzPvCKKiHbffBd5OrPJqlwUjea+wjMi/wZX/dYuig1T08YadbK7ulzTSCmLtTmRHcMacpwGUBh2m/GSkrdrqC/KrfNlQQqQuQx/2ZYe48yMtg1ENxz3fI9NIW2HBfIyJ0lYJ9hW+wy2bmBvGnISCfWZRv7aXR9ekWaefXShMjpBrhcLqeDGgeBdMs8+ETaI+TZNhVIkg4eapmKKl8scvc0PP94G4qb58HNVN4MZg1pc3I5SsvfGSuTB2yk0Q7QJrrqPTpKxw1jo6KmBDejFzZbwlehQca6xUL6ijdVlDwm7eEF8VpjkD4cYCQO681MTofAAnYnLt96JDJETwNyHE73miEDPxEu4Ux1I7RcnIE+7vlDcyizSES1tLBi3OeFnZx3NiUcDD1G2PfVTVb0DH3XYlZ23eBzrZTFG8xjiDF1Y6cw+17wVukgHF+VE9lxbPghG6gRYDZ+/yfCefnKJQFQfpjrsBoDj9y/sOo6ydI1dT7aXIoOlqYhs+L4hxDfQI66Frs8s0ZADI9vor4zSWkf/Wjm1MN+ECFJCZb5Yw70Y+ePSqbsOAl7Q6MAG40wojjDjdjKd8RabvZ2ablNqmW1fu15pNte3i3xEYjhRsYkMQSrjfvm9KpCF0710c9XMKD9YTU=",
        "__VIEWSTATEGENERATOR": "B0093F3C",
        "__EVENTVALIDATION": "QZRbcthpynGiSmCxn7L1/IR7cCCDnwC9mLHizdX7DxflirHr4cXQ0mPg3hlqfFU9KNe0SMHIrG4QNqAR5ek8NvMcpQTdgFizII6o5EldpRec93IT6yzgiqyex8FBuviaM1J5p+Duar580PiMoERIrQ/+j9ZVE0n9OfF2dQxDV5LI+Rt5U53bnMRPgi29h0yW9VmfxhSQlV3LjqchFv7z0kGoaNuG8SEQ9a/qWBVdd1nsGWx55cBFfqAdVaOBcwe9DtwlP6SgBcj98AoGGP9OVMErk3Si0gcDLG4349O4QYQ+Kcxoi0ZNGCDHctDgMMnVrxWHxz0RvuwWmdKQ9VhO950DRgza9y8Qs3zSS4Yu6MB3Pfr0uz1XcZ4MkJlcn4QufnhtbQCZYGXkuUscPRE3Wc50yM0v0zP7e5YRogUxjVwtQSp+GVQ9376mmo4XM6VuVLOi9vncSYZj9Qc4MM8ZC3C0XucKJNPXU6XUTTFkqFechq4goUGy9OX24aItH/Fe5QR6jAsdlrI2kGJceqqWUhpQZlcALt5fhpjDGIoixeh0PtGOkT2kr98R0p2yY7Ut/MfZVIfPLyoE0EsYcjpXJPb6jyZ9pyEvv6/auJmwT4cXlVmpT3A2t9810y/VGmHeooSFujZSlYssqCx1YIsHfGasAhDYGYIPTy65u/lRWzyOlL9bMAkCkuHVOFFRfWAwFnm4oGYnr5MqideEwJAXaqxg1HoNh7HDJ4kabaFF711oPhOsXy5EhqtFz25nvrim6cw3Gc6wLW7Pw4WMXdhdXxlloX3v+GtsYSxM9Yw0GpfigH2dOoNkPjxsgF91qajYwI6J6rIygumV77NhOjs19TDL3Ec4B/jXTisW0VRevu+kkRHlyjH1PaW7yRAEXNYVve18THmlsi/g9QUJsVb6TIGEIq1qV3SBRaIcuvjC2Pe35S5nD9S2FY/NUxXGIMdkDsZWWI3PelsmYmnrGehHrrjUG+2CChNIvTtSRSB+FC+fY5th2VOfxv1fPWaj31jGwVbYCCCWHOYUWtwgTbIyTV9PtjvOm2+wI7KNFLynOt3cawNVvcTy2RuUqYE8hIHzWpk0wrSKIeFlyOfeUx5FP6oMiO5gRk6aoH2IZelTslt+9iPSV/XrfIFbJW0MLiFLlJXgs9ZUjRNyvMUETBYckr9200La897V7fkWZeHZ+EtKcac0/ZAEenK+FGuk1gscqBF6jwa7mnDnS7WYxYkSZFpXtQzhol+g1mVNpr03C9j1sbYYKKwLBEsxWTmZHVPsgoROYU7rXejoWaPMflq93zuWWifI0QMNtdCiBmFfYa88tlOvMddB7SmmwcUWh2chNYWSmsfM5gNhENRvPuVNOF6nBWcc/nExhsG/PCP75yn6frgS08wOdzcN5BGok2IBE5fOodCE0uLgMJXyZ4GIlbhGxwlLAY+aEq4qqQ7CYSkg//Feqsk2fqXUMuzB10naj/hJDBgcXlQVkJT/ZrE2rYXX53cm9Oz+ufeaz/mu8qla23WK5EQSJktFx5sgD/KFFnKcn2HYVQCjOBafH3A0Ig==",
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
        "ctl00$plnMain$ddlReportCardRuns": "2-2025",
        "ctl00$plnMain$ddlClasses": "ALL",
        "ctl00$plnMain$ddlCompetencies": "ALL",
        "ctl00$plnMain$ddlOrderBy": "Class"
    }

    # Get student's classes and grades
    r = s.get(assignmentsurl, data=payload, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    courseList = []

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
                    "grade": assignmentGrade
                })
            except:
                pass

        courseList.append(dict)
    
    return courseList


def get_transcript(s):
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
    data["class"] = get_assignments(s)
    data["transcript"] = get_transcript(s)
    data["schedule"] = get_schedule(s)

    return jsonify(data), 200


if __name__ == "__main__":
    app.run(debug=True)


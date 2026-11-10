var schoolNames = {
"University of Wisconsin-Madison": "Wisconsin",
"James Madison University": "James Madison",
"Coastal Carolina University": "Coastal Carolina",
"University of South Alabama": "South Alabama",
"University of Massachusetts, Amherst": "Massachusetts",
"University of California, Los Angeles": "UCLA",
"Arizona State University": "Arizona State",
"University of Houston": "Houston",
"Oregon State University": "Oregon State",
"East Carolina University": "East Carolina",
"Clemson University": "Clemson",
"Virginia Commonwealth University": "VCU",
"University of Nevada, Reno": "Nevada",
"California State University, Fresno": "Fresno State",
"University of Wyoming": "Wyoming",
"University of Georgia": "Georgia",
"U.S. Naval Academy": "Navy",
"University at Buffalo, the State University": "Buffalo",
"University of Utah": "Utah",
"University of South Florida": "South Florida",
"University of Iowa": "Iowa",
"Mississippi State University": "Mississippi State",
"University of Texas at San Antonio": "UTSA",
"Western Kentucky University": "Western Kentucky",
"University of Tennessee, Knoxville": "Tennessee",
"Northern Illinois University": "Northern Illinois",
"University of Cincinnati": "Cincinnati",
"University of Louisville": "Louisville",
"University of Michigan": "Michigan",
"University of Alabama": "Alabama",
"University of Minnesota, Twin Cities": "Minnesota",
"University of Hawaii, Manoa": "Hawaii",
"Georgia Southern University": "Georgia Southern",
"Marshall University": "Marshall",
"Miami University (Ohio)": "Miami (Ohio)",
"University of Kansas": "Kansas",
"Pennsylvania State University": "Penn State",
"Colorado State University": "Colorado State",
"Purdue University": "Purdue",
"Old Dominion University": "Old Dominion",
"Boise State University": "Boise State",
"Florida State University": "Florida State",
"New Mexico State University": "New Mexico State",
"Arkansas State University": "Arkansas State",
"University of Texas at El Paso": "UTEP",
"University of Akron": "Akron",
"University of Maryland, College Park": "Maryland",
"University of Nevada, Las Vegas": "UNLV",
"Louisiana Tech University": "Louisiana Tech",
"University of Alabama at Birmingham": "UAB",
"Florida International University": "FIU",
"Middle Tennessee State University": "Middle Tennessee",
"University of North Carolina, Chapel Hill": "North Carolina",
"Indiana University, Bloomington": "Indiana", 
"Oklahoma State University": "Oklahoma State",
"Ohio University": "Ohio",
"Texas State University": "Texas State",
"University of Florida": "Florida",
"University of California, Berkeley": "California",
"Utah State University": "Utah State",
"University of Arkansas, Fayetteville": "Arkansas",
"University of Connecticut": "Connecticut",
"Texas A&M University, College Station": "Texas A&M",
"University of Mississippi": "Ole Miss",
"University of South Carolina, Columbia": "South Carolina",
"Appalachian State University": "App State",
"University of Washington": "Washington",
"University of New Mexico": "New Mexico",
"Auburn University": "Auburn",
"University of Texas at Austin": "Texas",
"West Virginia University": "West Virginia",
"University of Memphis": "Memphis",
"University of Central Florida": "UCF",
"Ball State University": "Ball State",
"Florida Atlantic University": "FAU",
"Washington State University": "Washington State",
"University of Louisiana at Monroe": "Louisiana, Monroe",
"University of Virginia": "Virginia",
"University of Louisiana at Lafayette": "Louisiana, Lafayette",
"Virginia Polytechnic Institute and State": "Virginia Tech",
"Kansas State University": "Kansas State",
"The Ohio State University": "Ohio State",
"University of North Texas": "North Texas",
"University of Oregon": "Oregon",
"Bowling Green State University": "Bowling Green",
"Georgia Institute of Technology": "Georgia Tech",
"University of Colorado, Boulder": "Colorado",
"Rutgers, The State University of New": "Rutgers",
"Texas Tech University": "Texas Tech",
"North Carolina State University": "NC State",
"San Jose State University": "San Jose State",
"Georgia State University": "Georgia State",
"University of Kentucky": "Kentucky",
"University of Nebraska, Lincoln": "Nebraska",
"University of Missouri, Columbia": "Missouri",
"University of Oklahoma": "Oklahoma",
"Central Michigan University": "Central Michigan",
"Western Michigan University": "Western Michigan",
"Iowa State University": "Iowa State",
"University of Toledo": "Toledo",
"Louisiana State University": "LSU",
"The University of North Carolina at": "Charlotte",
"The University of Southern Mississippi": "Southern Mississippi",
"Eastern Michigan University": "Eastern Michigan",
"University of Illinois Urbana-Champaign": "Illinois",
"University of Arizona": "Arizona",
"Michigan State University": "Michigan State",
"San Diego State University": "San Diego State",
"Kent State University": "Kent State",
"Air Force": "Air Force",
"Pittsburgh": "Pittsburgh",
"Troy University": "Troy",
"Temple": "Temple",
"U.S. Military Academy": "Army",
"Kennesaw State University":"Kennesaw State"
}

var conferences = {
"Air Force": "Mountain West",
"James Madison University": "Sun Belt",
"Pittsburgh": "ACC",
"Troy University": "Sun Belt",
"Temple": "AAC",
"University of Wisconsin-Madison": "Big Ten",
"University of Massachusetts, Amherst": "Independent",
"University of California, Los Angeles": "Big Ten",
"Arizona State University": "Big 12",
"University of Houston": "Big 12",
"Oregon State University": "Pac-12",
"East Carolina University": "AAC",
"Clemson University": "ACC",
"Virginia Commonwealth University": "Atlantic 10",
"University of Nevada, Reno": "Mountain West",
"California State University, Fresno": "Mountain West",
"University of Wyoming": "Mountain West",
"University of Georgia": "SEC",
"U.S. Naval Academy": "AAC",
"University at Buffalo, the State University": "MAC",
"University of Utah": "Big 12",
"University of South Florida": "AAC",
"University of Iowa": "Big Ten",
"Mississippi State University": "SEC",
"University of Texas at San Antonio": "AAC",
"Western Kentucky University": "C-USA",
"University of Tennessee, Knoxville": "SEC",
"University of Cincinnati": "Big 12",
"University of Louisville": "ACC",
"University of Michigan": "Big Ten",
"University of Alabama": "SEC",
"University of Minnesota, Twin Cities": "Big Ten",
"University of Hawaii, Manoa": "Mountain West",
"Georgia Southern University": "Sun Belt",
"Marshall University": "Sun Belt",
"Miami University (Ohio)": "MAC",
"University of Kansas": "Big 12",
"Pennsylvania State University": "Big Ten",
"Colorado State University": "Mountain West",
"Purdue University": "Big Ten",
"Old Dominion University": "Sun Belt",
"Boise State University": "Mountain West",
"Florida State University": "ACC",
"New Mexico State University": "C-USA",
"Arkansas State University": "Sun Belt",
"University of Texas at El Paso": "C-USA",
"University of Akron": "MAC",
"University of Maryland, College Park": "Big Ten",
"University of Nevada, Las Vegas": "Mountain West",
"Louisiana Tech University": "C-USA",
"University of Alabama at Birmingham": "AAC",
"Florida International University": "C-USA",
"Middle Tennessee State University": "C-USA",
"University of North Carolina, Chapel Hill": "ACC",
"Indiana University, Bloomington": "Big Ten", 
"Oklahoma State University": "Big 12",
"Ohio University": "MAC",
"Texas State University": "Sun Belt",
"University of Florida": "SEC",
"University of California, Berkeley": "ACC",
"Utah State University": "Mountain West",
"University of Arkansas, Fayetteville": "SEC",
"University of Connecticut": "Independent",
"Texas A&M University, College Station": "SEC",
"University of Mississippi": "SEC",
"University of South Carolina, Columbia": "SEC",
"Appalachian State University": "Sun Belt",
"University of Washington": "Big Ten",
"University of New Mexico": "Mountain West",
"Auburn University": "SEC",
"University of Texas at Austin": "SEC",
"West Virginia University": "Big 12",
"University of Memphis": "AAC",
"University of Central Florida": "Big 12",
"Ball State University": "MAC",
"Florida Atlantic University": "AAC",
"Washington State University": "Pac-12",
"University of Louisiana at Monroe": "Sun Belt",
"University of Virginia": "ACC",
"University of Louisiana at Lafayette": "Sun Belt",
"Virginia Polytechnic Institute and State": "ACC",
"Kansas State University": "Big 12",
"The Ohio State University": "Big Ten",
"University of North Texas": "AAC",
"University of Oregon": "Big Ten",
"Bowling Green State University": "MAC",
"Georgia Institute of Technology": "ACC",
"University of Colorado, Boulder": "Big 12",
"Rutgers, The State University of New": "Big Ten",
"Texas Tech University": "Big 12",
"North Carolina State University": "ACC",
"San Jose State University": "Mountain West",
"Georgia State University": "Sun Belt",
"University of Kentucky": "SEC",
"University of Nebraska, Lincoln": "Big Ten",
"University of Missouri, Columbia": "SEC",
"University of Oklahoma": "SEC",
"Central Michigan University": "MAC",
"Western Michigan University": "MAC",
"Iowa State University": "Big 12",
"University of Toledo": "MAC",
"Louisiana State University": "SEC",
"The University of North Carolina at": "AAC",
"The University of Southern Mississippi": "Sun Belt",
"Eastern Michigan University": "MAC",
"University of Illinois Urbana-Champaign": "Big Ten",
"University of Arizona": "Big 12",
"Michigan State University": "Big Ten",
"San Diego State University": "Mountain West",
"Kent State University": "MAC",
"Northern Illinois University": "MAC",
"University of South Alabama":"Sun Belt",
"Coastal Carolina University":"Sun Belt",
"U.S. Military Academy":"AAC",
"Kennesaw State University":"C-USA"
}

var allSports = ['Football', "Men's Basketball", "Women's Basketball", "Men's Fencing", "Women's Fencing", "Men's Golf", "Women's Golf", 
				"Men's Gymnastics", "Women's Gymnastics", "Men's Ice Hockey", "Women's Ice Hockey", "Men's Lacrosse", "Women's Lacrosse", 
				"Men's Skiing", "Women's Skiing", "Men's Soccer", "Women's Soccer", "Men's Swimming and Diving", "Women's Swimming and Diving", 
				"Men's Tennis", "Women's Tennis", "Men's Track and Field, X-Country", "Women's Track and Field, X-Country", 
				"Men's Volleyball", "Women's Volleyball", "Men's Water Polo", "Women's Water Polo", "Men's Wrestling", "Women's Wrestling",   
				'Baseball', "Women's Beach Volleyball", "Women's Bowling", "Women's Equestrian", "Women's Field Hockey", 'Rifle', "Women's Rowing", 
				'Softball', "Women's Triathlon"]

var categoryNames = {
					'Excess (Deficiencies) of Revenues Over (Under) Expenses': 'Profit/Deficit',
					'Direct State or Other Government Support': "Local, State and Fed Gov't Appropriations",
					'Direct Institutional Support':'Direct Funds from Institution',
					'Less - Transfers to Institution':'Funds from Athletics to Institution',
					'Indirect Institutional Support - Athletic Facilities Debt Service, Lease and Rental Fees': 'Indirect Support for Facilities',
					'Guarantees': 'Away-Game Guarantees',
					'Contributions': 'Donations',
					'In-Kind': 'In-Kind Contributions',
					'Compensation and Benefits provided by a third party': 'Benefits Provided By Third Party',
					'Conference Distributions (Non Media and Non Bowl)': 'Conference Distributions (non-Media Rights)',
					'Guarantees (Expenses)': 'Home-Game Guarantees',
					'Coaching Salaries, Benefits and Bonuses paid by the University and Related Entities': 'Coaching Staff Compensation',
					'Coaching Salaries, Benefits and Bonuses paid by a Third Party': 'Coaching Staff Compensation Paid by Third Party',
					'Support Staff/ Administrative Compensation, Benefits and Bonuses paid by the University and Related Entities': 'Support Staff, Admin Compensation',
					'Support Staff/ Administrative Compensation, Benefits and Bonuses paid by Third Party': 'Support Staff, Admin Compensation Paid by Third Party',
					'Fund Raising, Marketing and Promotion':'Fundraising and Marketing',
					'Direct Overhead and Administrative Expenses':'Overhead and Administrative Expenses',
					'Bowl Expenses - Coaching Compensation/Bonuses': 'Bowl Game Coaching Compensation',
					'Excess Transfers to Institution': 'Additional Transfers to Institution',
					'Total Athletics Related Debt': 'Outstanding Athletics Debt',
					'Total Institutional Debt': 'Outstanding Institutional Debt',
					'Institutional Endowments': 'Institution Endowments',
					'Athletically-Related Facilities Annual Debt Service':'Annual Athletic Debt Service',
					"Institution's Annual Debt Service":'Annual Institution Debt Service',
					"Institution's Education and General Expenses":"Institution Education & General (E&G) Expenses",
					"Average Cost of Full Grant-in-Aid - In-State": 'In-State Grant in Aid',
					"Average Cost of Full Grant-in-Aid - Out-of-State": "Out-of-State Grant in Aid",
					"Average Cost of Attendance - In-State":"In-State Cost of Attendance",
					"Average Cost of Attendance - Out-of-State":"Out-of-State Cost of Attendance",
					"Enhanced Educational Benefits (Alston or other)":"Alston Payments"
				}

var ratios = {
		"Texas": 1.6,
		"LSU": 2.3,
		"TCU":2,
		"Florida":1.2,
		"Iowa":1.4,
		"Georgia":1.4,
		"Washington":1.3,
		"Minnesota":1.5,
		"Illinois":.7,
		"Arkansas":2.3,
		"Nebraska":1.7,
		"UCLA":2,
		"Missouri":1.7,
		"Arizona State":.4
}

var notIncluded2025 = {}
var notIncluded2024 = {'Excess Transfers to Institution':['UTSA','Oklahoma State'],
					'Conference Realignment Expenses':['UTSA','Oklahoma State'],
					'Athletics Dedicated Endowments':['UTSA'],
					'Total Athletics Related Debt':['UTSA'],
					'Total Institutional Debt':['UTSA'],
					'Athletics Dedicated Endowments':['UTSA','Oklahoma State'],
					'Institutional Endowments':['UTSA','Oklahoma State'],
					'Athletics Related Capital Expenditures':['UTSA'],
					'Institutional Expenses':['UTSA'],
					'Athletically-Related Facilities Annual Debt Service':['UTSA'],
					"Institution's Annual Debt Service":['UTSA'],
					"Institution's Education and General Expenses":['UTSA'],
					"Average Cost of Full Grant-in-Aid - In-State": ['UTSA'],
					"Average Cost of Full Grant-in-Aid - Out-of-State": ['UTSA'],
					"Average Cost of Attendance - In-State":['UTSA'],
					"Average Cost of Attendance - Out-of-State":['UTSA'],
					'Expenses Dedicated to Compliance':['UTSA']
				}
var notIncluded2023 = {}
var notIncluded2022 = {}
var notIncluded2021 = {}
var notIncluded2020 = {'Excess Transfers to Institution':['Akron','Alabama','App State','Arizona','Boise State','Clemson','FIU',
													'Kansas State','Louisville','Marshall','Miami (Ohio)','Minnesota','Missouri',
													'New Mexico','North Texas','Oklahoma State','Oregon State','Penn State',
													'San Diego State','South Alabama','South Florida','Southern Mississippi',
													'Texas Tech','Toledo','UCLA','UTEP'],
					'Conference Realignment Expenses':['Akron','Alabama','App State','Arizona','Boise State','Clemson','FIU',
													'Indiana','Kansas','Kansas State','Louisville','Marshall','Miami (Ohio)',
													'Minnesota','Missouri','New Mexico','North Texas','Ohio State','Oklahoma State',
													'Oregon State','Penn State','San Diego State','South Alabama','South Florida',
													'Southern Mississippi','Texas Tech','Toledo','UCLA','UTEP','Wyoming'],
					'Athletics Dedicated Endowments':['Nevada','Oklahoma State','Toledo'],
					'Institutional Endowments':['Nevada','Oklahoma State','Penn State'],
					'Athletics Related Capital Expenditures':['Nevada','Penn State','Texas Tech','Louisville'],
					'Expenses Dedicated to Compliance':['Penn State','Oklahoma State','Toledo','Kent State','South Alabama','Ball State']
				}

var notInlcuded2019 = {'Excess Transfers to Institution':['Akron','UAB','Arizona','Boise State','UCF','Clemson','FIU',
													'Georgia Southern','Kansas','Kansas State','Miami (Ohio)','Missouri',
													'Ohio','Oklahoma State','Oregon State','Penn State',
													'San Diego State','Southern Mississippi',"Massachusetts",
													'Texas Tech','Toledo','UCLA','UTEP'],
					'Conference Realignment Expenses':['Akron','Alabama','UAB','Arizona','Boise State','Clemson','FIU',"Florida",
													'Georgia Southern','Indiana','Kansas','Kansas State','Miami (Ohio)',
													'Michigan','Missouri','Ohio','Oklahoma State',
													'Oregon State','Penn State','San Diego State',"Massachusetts",
													'Southern Mississippi','Texas Tech','Toledo','UCLA','UTEP'],
					'Athletics Dedicated Endowments':['Boise State','Nevada','Oklahoma State','Toledo'],
					'Institutional Endowments':['Boise State','Georgia Southern','Nevada','Oklahoma State','Penn State','Toledo'],
					'Athletics Related Capital Expenditures':['Toledo','Penn State','Texas Tech','Louisville'],
					'Expenses Dedicated to Compliance':['Arizona','Oklahoma State','Oregon State','Toledo','Kent State','Georgia Southern','Ball State']
				}

var notInlcuded2018 = {'Excess Transfers to Institution':['Akron','App State','Arizona','Ball State','Boise State','Clemson','FAU',
													'Georgia Southern','Kansas','Kansas State','Marshall','Memphis','Miami (Ohio)',
													'Missouri','New Mexico','Oklahoma State','Oregon State','Penn State',
													'Southern Mississippi',"Massachusetts",'Virginia','Western Michigan',
													'Texas Tech','Toledo','UCLA','UTEP','Wyoming','Kent State','Northern Illinois'],
					'Conference Realignment Expenses':['Akron','App State','Arizona','Ball State','Boise State','Clemson',"Florida",
													'Georgia','Georgia Southern','Indiana','Kansas','Kansas State','Marshall',
													'Memphis','Miami (Ohio)','Missouri','New Mexico','Oklahoma State',
													'Oregon State','Penn State',"Massachusetts",'Virginia','Western Michigan','Wyoming',
													'Southern Mississippi','Texas Tech','Toledo','UCLA','UTEP','Kent State','Northern Illinois'],
					'Athletics Dedicated Endowments':['Ball State','Georgia','Boise State','Massachusetts','Kent State','Oklahoma State','Toledo'],
					'Institutional Endowments':['Ball State','Boise State','Georgia','Georgia Southern','Nevada','Oklahoma State','Penn State',
													'Toledo','South Carolina','Massachusetts','Kent State'],
					'Athletics Related Capital Expenditures':['Toledo','Penn State','Texas Tech','Louisville','Kent State'],
					'Expenses Dedicated to Compliance':['App State','Arizona','Arkansas State','Oklahoma State','Oregon State','Toledo','Kent State','Georgia Southern',
													'Ball State','East Carolina','FIU','New Mexico','Massachusetts'],
					'Total Athletics Related Debt':['Kent State'],
					'Total Institutional Debt':['Kent State'],
					'Athletically-Related Facilities Annual Debt Service':['Kent State'],
					"Institution's Annual Debt Service":['Kent State'],
					"Institution's Education and General Expenses":['Kent State'],
					"Average Cost of Full Grant-in-Aid - In-State": ['Kent State'],
					"Average Cost of Full Grant-in-Aid - Out-of-State": ['Kent State'],
					"Average Cost of Attendance - In-State":['Kent State'],
					"Average Cost of Attendance - Out-of-State":['Kent State']
				}

var notIncluded = {"2018":notInlcuded2018,"2019":notInlcuded2019,"2020":notIncluded2020,"2021":notIncluded2021,"2022":notIncluded2022,"2023":notIncluded2023,"2024":notIncluded2024,"2025":notIncluded2025}


/*
var corrections {
Athletic Student Aid Guarantees
Guarantees Coaching Salaries, Benefits
Coaching Salaries, Benefits and Bonuses paid by the University and Related Entities Coaching Salaries, Benefits
Coaching Salaries, Benefits and Bonuses paid by a Third Party Support Staff/Administrative
Support Staff/Administrative Compensation, Benefits and Bonuses paid by the University and Related Entities Support Staff/Administrative
Support Staff/Administrative Compensation, Benefits and Bonuses paid by Third Party Severance Payments
Severance Payments Recruiting
Recruiting Team Travel
Team Travel Sports Equipment, Uniforms
Sports Equipment, Uniforms and Supplies Game Expenses
Game Expenses Fund Raising, Marketing and
Fund Raising, Marketing and Promotion Sports Camp Expenses
Sports Camp Expenses Spirit Groups
Spirit Groups Athletic Facilities Debt
Athletic Facilities Debt Service, Leases and Rental Fee Direct Overhead and
Direct Overhead and Administrative Expenses Indirect Institutional Support
Indirect Institutional Support Medical Expenses and
Medical Expenses and Insurance Memberships and Dues
Memberships and Dues
 Student-Athlete Meals (non-
Student-Athlete Meals (non- travel) Other Operating Expenses
Other Operating Expenses Bowl Expenses
Bowl Expenses Total Operating Expenses
Total Operating Expenses Excess (Deficiencies) of Revenues Over (Under) Expenses
}

Guarantees Coaching Salaries, Benefits
Coaching Salaries, Benefits and Bonuses paid by the University and Related Entities Coaching Salaries, Benefits
Coaching Salaries, Benefits and Bonuses paid by a Third Party Support Staff/Administrative
Support Staff/Administrative Compensation, Benefits and Bonuses paid by the University and Related Entities Support Staff/Administrative
Support Staff/Administrative Compensation, Benefits and Bonuses paid by Third Party Severance Payments
Severance Payments Recruiting
Recruiting Team Travel
Team Travel Sports Equipment, Uniforms
Sports Equipment, Uniforms and Supplies Game Expenses
Game Expenses Fund Raising, Marketing and
Fund Raising, Marketing and Promotion Sports Camp Expenses
Sports Camp Expenses Spirit Groups
Spirit Groups Athletic Facilities Debt
Athletic Facilities Debt Service, Leases and Rental Fee Direct Overhead and
Direct Overhead and Administrative Expenses Indirect Institutional Support
Indirect Institutional Support Medical Expenses and
Medical Expenses and Insurance Memberships and Dues
Memberships and Dues Student-Athlete Meals (non-
Student-Athlete Meals (non- travel) Other Operating Expenses
Other Operating Expenses
 Bowl Expenses
Bowl Expenses Total Operating Expenses
Total Operating Expenses Excess (Deficiencies) of Revenues Over (Under) Expenses

Guarantees Coaching Salaries, Benefits
Coaching Salaries, Benefits and Bonuses paid by the University and Related Entities Coaching Salaries, Benefits
Coaching Salaries, Benefits and Bonuses paid by a Third Party Support Staff/Administrative
Support Staff/Administrative Compensation, Benefits and Bonuses paid by the University and Related Entities Support Staff/Administrative
Support Staff/Administrative Compensation, Benefits and Bonuses paid by Third Party Severance Payments
Severance Payments Recruiting
Recruiting Team Travel
Team Travel Sports Equipment, Uniforms
Sports Equipment, Uniforms and Supplies Game Expenses
Game Expenses Fund Raising, Marketing and
Fund Raising, Marketing and Promotion Sports Camp Expenses
Sports Camp Expenses Spirit Groups
Spirit Groups Athletic Facilities Debt
Athletic Facilities Debt Service, Leases and Rental Fee Direct Overhead and
Direct Overhead and Administrative Expenses Indirect Institutional Support
Indirect Institutional Support Medical Expenses and
Medical Expenses and Insurance Memberships and Dues
Memberships and Dues Student-Athlete Meals (non-
Student-Athlete Meals (non- travel) Other Operating Expenses
Other Operating Expenses
 Bowl Expenses
Bowl Expenses
Total Operating Expenses*/
#============================================================================================================================================================
# Author:	   Erika Fonseca
# Create date: 31/03/2020
# Description:	Generates a report with a map of all the answers to surveys by user, having the question in columns.
#               |UserId	|SurveyId	|ANS_Q1	|ANS_Q2	|ANS_Q3	|ANS_Q4 ....
#============================================================================================================================================================

import tools
import sys
import datetime
import subprocess

try:
    import pip
except:
    subprocess.call([sys.executable, "-m", "python", "ensurepip", "--default-pip"])

try:
    import pandas as pd
except ImportError as error_msg:
    tools.install_package("pandas")
    import pandas as pd

def generate_query_survey(SurveyID):
	# Generates an SQL string that retrives a map of which questions are present in a given survey and which are not given an input parameter SurveyID
	query = 'SELECT * FROM (SELECT SurveyId, QuestionId, 1 as InSurvey FROM SurveyStructure WHERE SurveyId = @currentSurveyId UNION SELECT @currentSurveyId as SurveyId, Q.QuestionId, 0 as InSurvey FROM Question as Q WHERE NOT EXISTS (SELECT * FROM SurveyStructure as S WHERE S.SurveyId = @currentSurveyId AND S.QuestionId = Q.QuestionId)) as t ORDER BY QuestionId'
	return query.replace("@currentSurveyId", SurveyID)

def generate_query_map_questions_survey(SurveyID, QuestionID, InSurvey, lastQuestion):
	# Generates a template to retrieve the answers given by an user for a given SurveyID and QuestionID
	# As we are creating a map we need to generate columns for all questions, even when it's not present on the survey
	# So when the question is not in the Survey we generate a column with a NULL value representing the answer otherwise we retrive to answer give by the user
	if InSurvey == 0:
		query = 'NULL AS ANS_Q<QUESTION_ID>'
	else: 
		query = 'COALESCE((SELECT a.Answer_Value FROM Answer as a WHERE a.UserId = u.UserId AND a.SurveyId = <SURVEY_ID> AND a.QuestionId = <QUESTION_ID>), -1) AS ANS_Q<QUESTION_ID>'
	query = query.replace("<SURVEY_ID>", SurveyID)
	query = query.replace("<QUESTION_ID>", QuestionID)
	if lastQuestion == False: 
		query = query + ', '
	else:
		query = query + ' '
	return query 

def generate_query_map_questions_answers_survey(SurveyID, DynamicColumns, lastSurvey):
	# Generates the full query to retrieve the final map with all the answers to surveys by user having the question in columns
	# It creates one SQL statement for each SurveyID
	query = 'SELECT UserId, <SURVEY_ID> as SurveyId, <DYNAMIC_QUESTION_ANSWERS> FROM [User] as u WHERE EXISTS (SELECT * FROM Answer as a WHERE u.UserId = a.UserId AND a.SurveyId = <SURVEY_ID>)'
	query = query.replace("<SURVEY_ID>", SurveyID)
	query = query.replace("<DYNAMIC_QUESTION_ANSWERS>", DynamicColumns)
	if lastSurvey == False: query = query + ' UNION '
	return query 

sql_conn = tools.connect_SQL() 

# Retrieve the current structure from the database
query = 'SELECT * FROM [Survey_Sample_A18].[dbo].[SurveyStructure]'
df_CurrentStructure = pd.read_sql(query, sql_conn)
# Retrieve the last structure saved for the python application
df_PreviousStructure = tools.read_structure()

# Check if there was any change on the SurveyStructure, and if so update the view 
if (df_CurrentStructure.equals(df_PreviousStructure))==False:
	
	# Save the new structure
	tools.save_report(df_CurrentStructure, "config", "structure")

	# Check all the surveys on the data base
	surveyListQuery = 'SELECT SurveyId FROM Survey ORDER BY SurveyId'
	df_Surveys = pd.read_sql(surveyListQuery, sql_conn)
	# Collect the information: SurveyId, QuestionId and InSurvey (0 means that the question is not in the structure of the survey, 1 that it is)
	df_Surveys['Query_String'] = df_Surveys.apply (lambda row: generate_query_survey(str(row.SurveyId)), axis=1)
	lastSurvey = df_Surveys['SurveyId']._values[-1]

	# In this context we need to create or update the view, because the structure is out-of-date
	FullQuery ="CREATE OR ALTER VIEW vw_AllSurveyData AS ("
	for i in range(df_Surveys.shape[0]):
		query = df_Surveys['Query_String']._values[i]
		SurveyID = df_Surveys['SurveyId']._values[i]
		df_SurveyQuestionsMap = pd.read_sql_query(query, sql_conn)
		lastQuestion = df_SurveyQuestionsMap['QuestionId']._values[-1]
		# For each survey generate the appropriate columns configured according to the characteristic of the survey
		# remark: if a question is not present in the survey it will appear with the NULL value
		df_SurveyQuestionsMap['Query_String'] = df_SurveyQuestionsMap.apply (lambda row: generate_query_map_questions_survey(str(row.SurveyId), 
																			str(row.QuestionId), row.InSurvey, row.QuestionId==lastQuestion) , axis=1)
		new_df = pd.DataFrame(df_SurveyQuestionsMap['Query_String'])
		# Generate the final query to retrive all answers for a given survey
		DynamicColumns = new_df.transpose().to_string(header=False, index= False, index_names = False)
		FullQuery = FullQuery + generate_query_map_questions_answers_survey(str(SurveyID), DynamicColumns, SurveyID==lastSurvey)

	FullQuery = FullQuery + ')'	
	try:
		with sql_conn.cursor() as cursor:
			cursor.execute(FullQuery)
	except:
		print('Attention: error trying to update view on database! Contact the support to check.')
		sys.exit("Fail to update view on DB")
		
query = "SELECT * FROM vw_AllSurveyData ORDER BY SurveyId, UserId"
try:
	df_AllSurveyData = pd.read_sql(query, sql_conn)
except:
	print('Attention: error trying to retrieve data from view vw_AllSurveyData on database! Contact the support to check.')
	sys.exit("Fail to retrievew view data from DB")

today = datetime.date.today()
tools.save_report(df_AllSurveyData, "report", "Survey_Data_"+str(today))
print("Report successfully processed and saved as: ", "Survey_Data_"+str(today))
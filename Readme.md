# Generate Survey Report
Generates a report with a map of all the answers to surveys by user, having the question in columns.

# Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Prerequisites
1- SQL Server database with the following structure:
    - dbo.Answer

    - dbo.Question

    - dbo.Survey

    - dbo.SurveyStructure

    - dbo.User   

If you don't have the database create one and use the following script to have the proper structure:
```
CREATE TABLE [dbo].[Answer](
	[QuestionId] [int] NOT NULL,
	[SurveyId] [int] NOT NULL,
	[UserId] [int] NOT NULL,
	[Answer_Value] [int] NULL,
 CONSTRAINT [PK_Answer] PRIMARY KEY CLUSTERED 
(
	[QuestionId] ASC,
	[SurveyId] ASC,
	[UserId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Question]    Script Date: 4/8/2020 7:20:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Question](
	[QuestionId] [int] IDENTITY(1,1) NOT NULL,
	[Question_Text] [nvarchar](max) NULL,
 CONSTRAINT [PK_Question] PRIMARY KEY CLUSTERED 
(
	[QuestionId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Survey]    Script Date: 4/8/2020 7:20:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Survey](
	[SurveyId] [int] IDENTITY(1,1) NOT NULL,
	[SurveyDescription] [nvarchar](100) NULL,
	[Survey_UserAdminId] [int] NULL,
 CONSTRAINT [PK_Survey] PRIMARY KEY CLUSTERED 
(
	[SurveyId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[SurveyStructure]    Script Date: 4/8/2020 7:20:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SurveyStructure](
	[SurveyId] [int] NOT NULL,
	[QuestionId] [int] NOT NULL,
	[OrdinalValue] [int] NULL,
 CONSTRAINT [PK_SurveyStructure] PRIMARY KEY CLUSTERED 
(
	[SurveyId] ASC,
	[QuestionId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[User]    Script Date: 4/8/2020 7:20:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[User](
	[UserId] [int] IDENTITY(1,1) NOT NULL,
	[User_Name] [nvarchar](100) NULL,
	[User_Email] [nvarchar](100) NULL,
 CONSTRAINT [PK_User] PRIMARY KEY CLUSTERED 
(
	[UserId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Answer]  WITH CHECK ADD  CONSTRAINT [FK_Answer_Question] FOREIGN KEY([QuestionId])
REFERENCES [dbo].[Question] ([QuestionId])
GO
ALTER TABLE [dbo].[Answer] CHECK CONSTRAINT [FK_Answer_Question]
GO
ALTER TABLE [dbo].[Answer]  WITH CHECK ADD  CONSTRAINT [FK_Answer_Survey] FOREIGN KEY([SurveyId])
REFERENCES [dbo].[Survey] ([SurveyId])
GO
ALTER TABLE [dbo].[Answer] CHECK CONSTRAINT [FK_Answer_Survey]
GO
ALTER TABLE [dbo].[Answer]  WITH CHECK ADD  CONSTRAINT [FK_Answer_User] FOREIGN KEY([UserId])
REFERENCES [dbo].[User] ([UserId])
GO
ALTER TABLE [dbo].[Answer] CHECK CONSTRAINT [FK_Answer_User]
GO
ALTER TABLE [dbo].[Survey]  WITH CHECK ADD  CONSTRAINT [FK_Survey_UserAdmin] FOREIGN KEY([Survey_UserAdminId])
REFERENCES [dbo].[User] ([UserId])
GO
ALTER TABLE [dbo].[Survey] CHECK CONSTRAINT [FK_Survey_UserAdmin]
GO
ALTER TABLE [dbo].[SurveyStructure]  WITH CHECK ADD  CONSTRAINT [FK_SurveyStructure_Question] FOREIGN KEY([QuestionId])
REFERENCES [dbo].[Question] ([QuestionId])
GO
ALTER TABLE [dbo].[SurveyStructure] CHECK CONSTRAINT [FK_SurveyStructure_Question]
GO
ALTER TABLE [dbo].[SurveyStructure]  WITH CHECK ADD  CONSTRAINT [FK_SurveyStructure_Survey] FOREIGN KEY([SurveyId])
REFERENCES [dbo].[Survey] ([SurveyId])
GO
ALTER TABLE [dbo].[SurveyStructure] CHECK CONSTRAINT [FK_SurveyStructure_Survey]
GO

```

2- Python interpreter to run the script
3- Folder with write permission to save reports
4- Folder with write permission to save configurations

## Installing
- Put the generateSurveyReport.py and Config.ini at the same folder
- Configure the ini file to set the database location, and the folders to store configuration and reports files

## Running the Tests
Running the generateSurveyReport.py and check if it ran successfully, if not check the error messages

```
Remark: the access to the database is made using Windows authentication, so make sure the user running the code has 
privilleges to log in the SQL Server and access the database and its content.
```

# Authors
Erika Fonseca - Initial work - Data Wrangling Assignment

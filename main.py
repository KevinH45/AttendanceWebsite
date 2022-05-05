import streamlit as st
import pandas as pd
import gspread
import plotly.express as px

def top5(dictScoreList):

    dictScoreList = sorted(dictScoreList,key=lambda x:x.get("Total Hours"),reverse=True)
    
    try: 
        top5 = [[str(x.get("Name")),x.get("Total Hours")] for x in dictScoreList[:5]]
    except IndexError:
        return None

    return top5


st.set_page_config(page_icon=":bar_chart",page_title="888 Attendance Stats", layout="centered")
print("Set Page Config")



if "gc" or "gsheet" not in st.session_state:

    try: 
        with st.spinner("Collecting our data..."):

            # Idk if secure or not
            st.session_state.gc = gspread.service_account_from_dict(
                {
                    "type": st.secrets["type"],
                    "project_id": st.secrets["project_id"],
                    "private_key_id": st.secrets["private_key_id"],
                    "private_key": st.secrets["private_key"],
                    "client_email": st.secrets["client_email"],
                    "client_id": st.secrets["client_id"],
                    "auth_uri": st.secrets["auth_uri"],
                    "token_uri": st.secrets["token_uri"],
                    "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
                    "client_x509_cert_url": st.secrets["client_x509_cert_url"]
                }
            )
            print("Connected to sheet")

            st.session_state.gsheet =  st.session_state.gc.open_by_url("https://docs.google.com/spreadsheets/d/1_PnLrJySYRYBcNr_CdNmgOnXjARtGAc4wrznlw5Ee2A/edit#gid=0")
            print("Downloaded sheet")
    except Exception as e:
        print(e)
        st.error(e)
        st.stop()


st.title("Team 888's Attendance")

df = pd.DataFrame(st.session_state.gsheet.sheet1.get_all_records())
print("Converted to DataFrame")


# Bar chart of attendance

totalHourFig = px.bar(df, x="Name", y="Total Hours")
print("Created Bar Chart")

st.plotly_chart(totalHourFig)
print("Displayed Bar Chart")

# Stats
# Blank expander + already expanded makes it look like a box
with st.expander("", expanded=True):
    st.subheader("Quick stats")
    
    col1,col2,col3 = st.columns(3)


    try: 
        col1.metric("Mean Hours",round(df["Total Hours"].mean(skipna=True),2))
        col1.metric("Number of members", int(df.count()["Name"]))

        col2.metric("Median Hours", round(df["Total Hours"].median(skipna=True),2))
        col2.metric("Members actively working", int(df['Logged In?'].value_counts()["yes"]))

        col3.metric("Standard Deviation", round(df["Total Hours"].std(skipna=True),2))

    except TypeError:
        st.error("Data is poorly formatted. Cannot load stats")

# Attendance Leaderboard

# with st.sidebar:
#     st.header ("888 Attendance Leaderboard")
#     leaderboard = top5(st.session_state.gsheet.sheet1.get_all_records())

#     if leaderboard is not None:
#         st.success("1st Place: " + leaderboard[0][0]+" with "+str(leaderboard[0][1])+" hours")
#         st.warning("2nd Place: " + leaderboard[1][0]+" with "+str(leaderboard[1][1])+" hours")
#         st.info("3rd Place: " + leaderboard[2][0]+ " with "+str(leaderboard[2][1])+" hours")
#         st.error("4th Place: " + leaderboard[3][0]+ " with "+str(leaderboard[3][1])+" hours")
#         st.error("5th Place: " + leaderboard[4][0]+" with "+str(leaderboard[4][1])+" hours")
#     else:
#         st.error("No data found or data failed to load") 






import streamlit as st
import pandas as pd

USERINFO = 'data/UserInfo.csv'
IDEA_TABLE = 'data/Idea_table.csv'
def Check_User(USERINFO_,ID,PW):
    df = pd.read_csv(USERINFO_)
    df_part = df[df['ID'] == ID]
    df_part = df_part.values.tolist()[0]
    #print(df_part)
    #print(f"df_part:{df_part[1]}-------{df_part[2]}")
    return df_part[1] == PW, df_part[2]    #PWと管理者


def CSV_insert_data(CSVfile, *args, columns=['ID','Idea']):
    df = pd.read_csv(CSVfile)
    new_row = pd.DataFrame([list(args)], columns)
    newdf = pd.concat([df,new_row])
    newdf.to_csv(CSVfile)


if 'flag' not in st.session_state:
    st.session_state.flag = False
if st.session_state.flag ==False:
    st.session_state.User = [False, None, None, False]
    #st.session_state.

try:
    TF = isLogined   #意味の無いコード
    #print("try")
except NameError:
    isLogined = False
    ID = None
    #print("except")


#if isLogined:

#st.title("Idea入力画面")
#st.caption(f"{ID}さん、Ideaを入力してください")
#with st.form(key='Idea_form'):
#    Idea = st.text_input('Idea')
#    submit_btn = st.form_submit_button('送信')
#   cancel_btn = st.form_submit_button('キャンセル')

#    if submit_btn:
#        db_cursor = conn.cursor()
#        Add_Idea_query = f"INSERT INTO Idea_table (ID, Idea) VALUES ('{ID}', '{Idea}')"
#        db_cursor.execute(Add_Idea_query)
#        st.text(f"{Idea}：を追加できました！")


#else:
st.title("Login画面")
st.caption("IDとPasswordを設定してください")
with st.form(key='Login_form'):
    ID = st.text_input('ID')
    PW = st.text_input('Password')
    submit_btn = st.form_submit_button('送信')
    cancel_btn = st.form_submit_button('キャンセル')

    if submit_btn:
        isLogined, isAdmin = Check_User(USERINFO,ID,PW)
        #print(isLogined)
        if not isLogined:
            st.error("ログインに失敗しました")
        else:
            st.session_state.User = [True, ID, PW, isAdmin]
            st.session_state.flag = True
            #print("session")
    if cancel_btn:
        st.session_state.flag = False

#print(f"isLogined={isLogined}")
isLogined,ID,PW, isAdmin = st.session_state.User
#print(f"ID={ID},PW={PW}")
if isLogined:
    st.success("ログインに成功しました")
    st.header("Idea入力画面")
    st.caption(f"{ID}さん、Ideaを入力してください")
    with st.form(key='Idea_form'):
        Idea = st.text_input('Idea')
        submit_btn = st.form_submit_button('送信')
        cancel_btn = st.form_submit_button('キャンセル')

        if submit_btn:
            CSV_insert_data(IDEA_TABLE, ID, Idea)
            st.success(f"{Idea}：を追加できました！")
    
    df = pd.read_csv(IDEA_TABLE)
    if not isAdmin:
        st.dataframe(df["Idea"])
    else:
        st.dataframe(df[["ID","Idea"]])

        with st.form(key='Admin_form'):
            st.header('メンバー追加')
            newID = st.text_input('New Member ID')
            newPW = st.text_input('New Member Password')
            ID_add_btn = st.form_submit_button('追加')

            if ID_add_btn and not newPW=="":
                CSV_insert_data(USERINFO,newID,newPW,False,columns = ['ID','PW','管理者'])
                st.success(f"{newID}：を追加できました！")

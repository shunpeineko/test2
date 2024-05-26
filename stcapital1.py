import streamlit as st
import sys, glob
import pandas as pd
import time
import random
import os,base64
import gtts, playsound

def soundautoplay(audiofile):
    audio_placeholder = st.empty()
    with open(audiofile, "rb") as f:
        contents = f.read()
    audioS = "data:audio/ogg;base64,%s"%(base64.b64encode(contents).decode())
    audio_html = """<audio autoplay=True>
                    <source src="%s" type="audio/ogg"></audio>"""%audioS
    #audio_placeholder.empty()
    time.sleep(0.5)             # need this
    audio_placeholder.markdown(audio_html, unsafe_allow_html=True)

def speaktext(txt, lang='ja'):
    tmpaudiofile = '_tmp.mp3'
    gtts.gTTS(txt, lang=lang).save(tmpaudiofile)
    soundautoplay(tmpaudiofile)
    #st.audio(tmpaudiofile)

def gonext():
    st.session_state.idx += 1
    ask()

def checkans():
    idx, ans = st.session_state.idx, st.session_state.ans
    if inp := st.session_state.txt:
        if inp == ans:
            msg2 = msg = f'正解! {ans}です。'
            st.write(msg)
            speaktext(msg2)
            st.session_state.point += 1
        else:
            msg2 = msg = f'不正解。  答えは{ans}です,{inp}じゃないです。'
            st.write(msg)
            speaktext(msg2)
        st.session_state.txt  = ''  # to clear text_input box
        if idx % 10 == 9: st.balloons()
    else:
        st.write(f'{idx}: This is "{ans}"')
    st.button("Next", on_click=gonext)
    st.write(f'Score: {st.session_state.point} / {idx+1}')

def ask():
    r = random.randint(0,len(st.session_state.ND2)-1)
    r2 = st.session_state.D3[r]
    st.session_state.ans = D2[r2]
    msg = f"{r2}の首都は？"
    speaktext(msg)
    st.text_input(msg, '', key='txt', on_change=checkans)

if "D" not in st.session_state: 
    st.session_state.D = {}
    file1 = 'リスト3.xlsx'
    df = pd.read_excel(file1, skiprows=1,index_col="国名")
    df = df[:189]
    #print(df.columns)
    D = df.to_dict(orient='index')
    ND = df.to_dict()
    D2 = ND["首都"]
    st.session_state.D3 = df.index.tolist()        #国名
    st.session_state.ND2 = list(D2)
    st.session_state.point = st.session_state.idx = 0
    speaktext("始めます。")
    ask()



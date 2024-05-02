import streamlit as st

st.set_page_config(
    page_title="台電秘管家",
    page_icon="👋",
)

st.write("# 歡迎使用 台電秘管家! 👋")

st.sidebar.success("")

st.markdown(
    """
    台電秘管家 是專門提供台灣電力公司總管理處各種公共空間附加服務的平台
    **👈 可以從側邊欄位選擇你所需要的服務！**
    ### 有不清楚的地方嗎？
    - 大樓清潔及餐廳 **6394**
    - 會議室管理及公共空間借用 **6393/6396**
    - 自行車/機車/汽車 停車申請 **6395**
    ### 有其他問題想反應
    - 請點 [有話想說](https://docs.google.com/forms/d/e/1FAIpQLSfIxoPxykSdL_OI3sKiHVGKlDIPsuOXb5nzkHSFTyx6EaG72A/viewform)
"""
)

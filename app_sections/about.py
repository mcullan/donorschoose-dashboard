def app():
    import streamlit as st


    overview = """
**DonorsChoose** is an organization that matches donors to school fundraisers. These fundraisers, called **projects**, are shared on the site and promoted to subscribers.
* Each project has a specific **funding goal**. The project is open for donations until that goal is met, or until it *expires*.
* Donors are asked to give an optional **15% contribution** (of their donation amount) to support operations at DonorsChoose.


This **marketing dashboard** tracks metrics, identify areas that need attention, and provides lists of suitable donors for specific projects. It addresses the following problems:

"""


    objectives="""
### Track growth, success rates, and revenue
* Which project categories are underperforming? Are there any trends?
* How does current revenue compare to historical?

    See **Monthly Report** page.


### Find and intervene with underperforming projects
* At any point in time, which projects are at-risk of failing to meet the funding goal?
* To improve our *funding success rate*, who should we promote these projects to?

    See **Weekly Performance** page.



### Characterize and predict high-value donors
* What does a high-value donor look like?
* How quickly can we identify them?

    See **Donors Analysis** page.

"""

    note_data = """#### The Data
The organization published an historical (2013-2018) data set on Kaggle, comprising  Donations, Unique donors, Projects, Schools, Teachers. Examples can be found on the **Data Source** page."""


    st.markdown("## Overview")
    col1, col2 = st.beta_columns((9, 3))

    with col1:
        st.markdown(overview)
    with col2:
        st.markdown(note_data)

    st.markdown(objectives)




if __name__=='__main__':
    import streamlit as st
    st.title("DonorsChoose Dashboard")
    st.sidebar.markdown("sidebar placeholder")
    app()

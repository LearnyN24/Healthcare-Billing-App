import streamlit as st

def show_contacts_page():
    st.header("Contact Information")
    
    # Create a container for contact information with custom styling
    st.markdown(
        """
        <div style="
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        ">
            <h3 style="color: #1f77b4;">Developer Contact</h3>
            <p><strong>Name:</strong> AB</p>
            <p><strong>Phone:</strong> <a href="tel:+263787081371">+263 78 708 1371</a></p>
            <p><strong>Role:</strong> Application Developer</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Add a contact form
    st.subheader("Send a Message")
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        subject = st.text_input("Subject")
        message = st.text_area("Message")
        submit = st.form_submit_button("Send Message")
        
        if submit:
            st.success("Thank you for your message! We will get back to you soon.") 
import requests
from requests.auth import HTTPBasicAuth
import streamlit as st
from datetime import datetime
import base64


st.set_page_config(
    page_title="Best Jyotish Kundali",
    page_icon="🔮",
    # layout="wide",
    initial_sidebar_state="expanded",
)


st.image(
    "https://static.joonsite.com/storage/46059/media/2412111658443829.png",
    width=320,
    use_container_width=True,
)

st.markdown(
    """
    <div style="text-align: center; color: #444; font-size: 1.1rem; margin-bottom: 2rem;">
        <em>More Than Astrology, a Guiding Hand.</em>
    </div>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    st.header("🔑 API Credentials")
    api_username = st.text_input("API User Name", value="4545")
    api_key = st.text_input(
        "API Key", value="ByVOIaODH57QRVi6CqswHXGlcpDvj7tZBRoorY", type="password"
    )
    st.markdown("---")
    st.markdown(
        """
        <small>
        <b>Contact:</b> support@bestjyotish.com<br>
        <b>Phone:</b> +91 9911251511
        </small>
        """,
        unsafe_allow_html=True,
    )


api_username = "4545"
api_key = "ByVOIaODH57QRVi6CqswHXGlcpDvj7tZBRoorY"

if not api_username and api_key:
    # Show some warning to the user
    pass


AUTH = HTTPBasicAuth(api_username, api_key)
HEADERS = {"Content-Type": "application/json"}

COMMON_CONFIG = {
    "language": "hi",
    "tzone": 5.5,
    "chart_style": "NORTH_INDIAN",
    "footer_link": "bestjyotish.com",
    "logo_url": "https://static.joonsite.com/storage/46059/media/2412111658443829.png",
    "company_name": "Best Jyotish",
    "company_info": "Best Jyotish - More Than Astrology, a Guiding Hand. We walk with you through life’s journey—offering personal Kundli insights, dosha remedies, and puja guidance by experienced astrologers and pandits. From relationships to career and finances, we provide honest, practical advice rooted in tradition. Trusted by thousands worldwide, Best Jyotish is your spiritual family—online or offline, always just a call away.",
    "domain_url": "https://bestjyotish.com",
    "company_email": "support@bestjyotish.com",
    "company_landline": "+91 9911251511",
    "company_mobile": "+91 9911251511",
}

BASE_URL = "https://pdf.astrologyapi.com/v1/basic_horoscope_pdf"


def create_download_link(pdf_url, filename):
    """Create a download link for the PDF"""
    try:
        # Fetch the PDF content
        pdf_response = requests.get(pdf_url)
        if pdf_response.status_code == 200:
            # Encode PDF content to base64
            pdf_content = pdf_response.content
            b64_pdf = base64.b64encode(pdf_content).decode()

            # Create download link
            href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{filename}" class="download-btn">📥 Download Your Kundali PDF</a>'
            return href
        else:
            return None
    except Exception as e:
        st.error(f"Error preparing download: {e}")
        return None


st.markdown("### Kundali Details")


#         # hour_24 = birth_hour % 12
#         # if am_pm == "PM":
#         #     hour_24 += 12

#     else:
#         st.info("Please enter your API credentials above to use the form.")

with st.form("kundali_form"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 👤 Personal Information")

        name = st.text_input("Full Name", placeholder="Enter your full name")
        gender = st.selectbox("Gender", ["Male", "Female"])
        birth_date = st.date_input(
            "Birth Date",
            value=datetime.today(),
            min_value=datetime(1950, 1, 1),
            max_value=datetime.today(),
            format="YYYY/MM/DD",
        )

    with col2:
        st.markdown("#### 🕐 Birth Time & Location")

        birth_hour = st.selectbox("Birth Hour", list(range(0, 24)), index=0)
        birth_minute = st.selectbox("Birth Minute", list(range(0, 60)), index=0)

        coordinates = st.text_input(
            "Coordinates (lat,lon)",
            placeholder="28.6139,77.2090",
        )

        place = st.text_input("Birth Place", placeholder="City, State, Country")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        submit = st.form_submit_button("🔮 Generate Kundali", use_container_width=True)

    if submit:
        if not name or not coordinates or not place:
            st.warning("Please fill all the details.")

        else:
            lat, lon = map(float, coordinates.split(","))

            payload = {
                "name": name,
                "gender": gender.lower(),
                "hour": birth_hour,
                "min": birth_minute,
                "place": place,
                "day": birth_date.day,
                "month": birth_date.month,
                "year": birth_date.year,
                "lat": lat,
                "lon": lon,
            }

            payload.update(COMMON_CONFIG)
            print(payload)

            try:
                with st.spinner("🔮 Generating your personalized Kundali PDF..."):
                    response = requests.post(
                        BASE_URL,
                        json=payload,
                        headers=HEADERS,
                        auth=AUTH,
                    )

                if response.status_code == 200:
                    data = response.json()

                    if data.get("status") and data.get("pdf_url"):
                        st.markdown(
                            '<div class="success-message">✅ Your Kundali has been generated successfully!</div>',
                            unsafe_allow_html=True,
                        )

                        filename = f"{name.replace(' ', '_')}_Kundali_{birth_date.strftime('%Y%m%d')}.pdf"

                        download_link = create_download_link(data["pdf_url"], filename)

                        if download_link:
                            st.markdown(
                                f"""
                                <div style="text-align:center; margin: 2rem 0;">
                                    {download_link}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        else:
                            st.markdown(
                                f"""
                                <div style="text-align:center; margin: 2rem 0;">
                                    <a href="{data['pdf_url']}" target="_blank" class="download-btn">
                                        📥 Open Kundali PDF
                                    </a>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        st.info(
                            "💡 Your personalized Kundali PDF is ready. Click the button above to download it directly to your device."
                        )

                    else:
                        st.error(f"❌ {data.get('msg', 'Failed to generate Kundali.')}")

                else:
                    st.error(
                        f"❌ API call failed with status code: {response.status_code}"
                    )

                    if response.text:
                        st.code(response.text)

            except Exception as e:
                st.error(f"❌ Error: {e}")

    else:
        st.info("Please enter your details and click 'Generate Kundali'.")


# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #888; font-size: 0.9rem; padding: 2rem;">
        Made with ❤️ by <a href="https://bestjyotish.com" target="_blank" style="color: #7B3F00;">Best Jyotish</a><br>
        &copy; 2025 Best Jyotish - Your Trusted Astrology Partner
    </div>
    """,
    unsafe_allow_html=True,
)

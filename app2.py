import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# RapidAPI endpoint for nudity detection
RAPIDAPI_URL = "https://nudity-filter.p.rapidapi.com/nudity"

# Set your RapidAPI key here
RAPIDAPI_KEY = "YOUR_RAPIDAPI_KEY"

# Streamlit app
def main():
    st.title("Nudity Detection and Image Filter App")

    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "jfif"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

        # Perform nudity detection
        result = perform_nudity_detection(uploaded_file)

        if result:
            st.warning("Nudity Detected! Applying Filter...")
            # Apply a filter to the image
            filtered_image = apply_filter(uploaded_file)
            st.image(filtered_image, caption="Filtered Image.", use_column_width=True)

            # Download button for filtered image
            st.markdown(get_image_download_link(filtered_image), unsafe_allow_html=True)

        else:
            st.success("No Nudity Detected.")

# Nudity detection function
def perform_nudity_detection(image):
    headers = {
        "X-RapidAPI-Host": "nudity-filter.p.rapidapi.com",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
    }

    files = {"image": image.getvalue()}
    response = requests.post(RAPIDAPI_URL, files=files, headers=headers)

    if response.ok:
        data = response.json()
        return data.get("is_nude", False)

    return False

# Apply a simple filter to the image (e.g., grayscale)
def apply_filter(image):
    img = Image.open(image)
    img = img.convert("L")  # Convert to grayscale
    return img

# Function to create a download link for the filtered image
def get_image_download_link(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/jpg;base64,{img_str}" download="filtered_image.jpg">Download Filtered Image</a>'
    return href

if __name__ == "__main__":
    main()

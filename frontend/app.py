import streamlit as st
from streamlit_drawable_canvas import st_canvas
import io
import base64
from PIL import Image, ImageOps
from config import NUM_COLUMNS
from product import products
from testNe import test_loading, diffusion_image

# Streamlit layout (wide mode)
st.set_page_config(layout="wide")

# Hide Streamlit menu and footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Load external CSS file for styling
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Initialize session state
if "search_query" not in st.session_state:
    st.session_state["search_query"] = ""
if "saved_canvas_images" not in st.session_state:
    st.session_state["saved_canvas_images"] = []
if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0

# Increase uploader key
def increase_uploader_key():
    st.session_state["uploader_key"] += 1

# Define the function to show the canvas in a modal dialog
@st.dialog("Canvas Dialog", width="large")
def canvas_dialog():
    increase_uploader_key()
    st.write("Draw something in the canvas below:")
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=2,
        stroke_color="#000000",
        background_color="#ffffff",
        update_streamlit=True,
        height=200,
        width=700,
        drawing_mode="freedraw",
        key="canvas",
    )
    if st.button("Save"):    
        if canvas_result.image_data is not None:
            img = Image.fromarray(canvas_result.image_data.astype("uint8"), "RGBA")
            st.session_state["saved_canvas_images"].append(img)
            st.rerun()

# Function to display product details in a pop-up
@st.dialog("Product Details", width="large")
def product_details(product):
    # Product title
    st.write(f"### {product.title}")

    # Main product image
    st.markdown(f"""
                    <div class="product-card-detail">
                        <img src="{product.thumbnailImage}" class="product-image-detail" alt="{product.title}"/>
                    </div>
                """
                , unsafe_allow_html=True)

    # Display additional images in a horizontal row
    cols = st.columns(len(product.galleryThumbnail))
    for idx, image_url in enumerate(product.galleryThumbnail):
        with cols[idx]:
            st.image(image_url, use_container_width=True)

    # Product details
    st.markdown(f"""
                    <div class="product-card-detail-2">
                        <p class="product-price"><span style="font-size: 20px;">Price: ${product.price:.2f}🪙</span></p>
                        <p class="product-rating"><span style="font-size: 20px;">Rating: {product.rating}⭐</span></p>
                        <a href="{product.url}" target="_blank" class="product-link">
                            View Product on Website
                        </a>
                    </div>
                """, unsafe_allow_html=True)

# Function to input text to diffusion model
@st.dialog("Input text to Diffusion Model", width="large")
def diffusion_dialog():
    input_to_diffusion = st.text_input("Input", label_visibility="collapsed")
    if st.button("Submit"):
        with st.spinner('Wait for Diffusion Model...'):
            test_loading()
        try:
            st.session_state["saved_canvas_images"].append(diffusion_image)
            st.rerun()
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Function to clear all canvas
def clear_canvas():
    increase_uploader_key()
    if "saved_canvas_images" in st.session_state:
        st.session_state.pop("saved_canvas_images")

# Function to retrieve from product list
def products_retrieval(products):
    filtered_products = [product for product in products if st.session_state["search_query"].lower() in product.title.lower()]
    return filtered_products

# Left and Right Column layout
col1, col2 = st.columns([1, 4])

# Search bar on the left (col1)
with col1:
    st.session_state["search_query"] = st.text_input("Search", placeholder="Type product name or description...", label_visibility="collapsed", on_change=increase_uploader_key)
    
    st.button("Open Canvas", use_container_width=True, on_click=canvas_dialog)

    st.button("Prompt Diffusion", use_container_width=True, on_click=diffusion_dialog)

    uploaded_file = st.file_uploader("Upload image", label_visibility="collapsed", key=st.session_state["uploader_key"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image = ImageOps.exif_transpose(image)
        st.session_state["saved_canvas_images"].append(image)

    # Show saved canvas images if any
    if st.session_state["saved_canvas_images"]:
        for saved_img in st.session_state["saved_canvas_images"]:
            buffered = io.BytesIO()
            saved_img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            img_html = f'<img class="canvas-image" src="data:image/png;base64,{img_str}" alt="Canvas Drawing"/>'
            st.markdown(img_html, unsafe_allow_html=True)

    cols = st.columns(2)
    with cols[0]:
        st.button("Clear Canvas", on_click=clear_canvas, icon=":material/delete:", use_container_width=True)
    with cols[1]:
        st.button("Search", icon = ":material/search:", use_container_width=True)

# Filter products based on search query and images
filtered_products = products_retrieval(products)

# Display the filtered products in the right column (col2)
with col2:
    # If no products match the search, display a message
    if not filtered_products:
        st.write("No products found. Please try a different search.")
    else:
        # Create a grid layout with 3 columns per row
        cols = st.columns(NUM_COLUMNS) 

        # Display the products in a grid
        for i in range(0, len(filtered_products), NUM_COLUMNS):
            for j in range(NUM_COLUMNS):
                if i + j < len(filtered_products):
                    product = filtered_products[i + j]
                    with cols[j]:
                        
                         # Display each product inside a block
                        st.markdown(f"""
                            <div class="product-card">
                                <img src="{product.thumbnailImage}" class="product-image" alt="{product.title}"/>
                                <p class="product-title">{product.title}</p>
                                <p class="product-price">Price: ${product.price}</p>
                                <p class="product-rating">Rating: {product.rating} ⭐</p>
                                <a href="{product.url}" class="product-link" target="_blank">View Product</a>
                            </div>
                        """, unsafe_allow_html=True)

                        button_placeholder = st.container()
                        with button_placeholder:
                            st.markdown('<div class="small-centered-button">', unsafe_allow_html=True)
                            if st.button(
                                label="View Details",
                                key=f"view_details_{i}_{j}",
                                on_click=increase_uploader_key
                            ):
                                product_details(product)
                            st.markdown('</div>', unsafe_allow_html=True)

            # After displaying a row of products, update columns for the next row
            cols = st.columns(NUM_COLUMNS)  # Create new set of columns 
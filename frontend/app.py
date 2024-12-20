import streamlit as st
from streamlit_drawable_canvas import st_canvas
import io
import base64
from PIL import ImageOps, Image
from frontend.config import NUM_COLUMNS
from frontend.button_handler.diffusion_submit import get_image_from_diffusion
from frontend.button_handler.search_products import get_products
from frontend.components.product_card import render_product_card
from frontend.components.product_detail_card import render_product_detail_card

def run():
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
    with open("frontend/style.css", "r", encoding="utf-8") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    # Initialize session state
    if "search_query" not in st.session_state:
        st.session_state["search_query"] = ""
    if "saved_canvas_images" not in st.session_state:
        st.session_state["saved_canvas_images"] = []
    if "uploader_key" not in st.session_state:
        st.session_state["uploader_key"] = 0
    if "search_activate" not in st.session_state:
        st.session_state["search_activate"] = False
    if "search_image_results" not in st.session_state:
        st.session_state["search_image_results"] = []

    # Increase uploader key
    def increase_uploader_key():
        st.session_state["uploader_key"] += 1

    # Function to activate search
    def activate_search():
        st.session_state["search_activate"] = True

    # Function to deactivate search
    def deactivate_search():
        st.session_state["search_activate"] = False

    def view_details():
        increase_uploader_key()
        deactivate_search()

    def search():
        increase_uploader_key()
        activate_search()

    # Define the function to show the canvas in a modal dialog
    @st.dialog("Canvas Dialog", width="large")
    def canvas_dialog():
        increase_uploader_key()
        deactivate_search()
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
                img = img.convert("RGB")
                st.session_state["saved_canvas_images"].append(img)
                st.rerun()

    # Function to clear all canvas
    def clear_canvas():
        increase_uploader_key()
        deactivate_search()
        if "saved_canvas_images" in st.session_state:
            st.session_state.pop("saved_canvas_images")

    # Function to input text to diffusion model
    @st.dialog("Input text to Diffusion Model", width="large")
    def diffusion_dialog():
        increase_uploader_key()
        deactivate_search()
        input_to_diffusion = st.text_input("Input", label_visibility="collapsed")
        if st.button("Submit"):
            with st.spinner("Wait for Diffusion Model..."):
                image = get_image_from_diffusion(input_to_diffusion)
                print(image)
            if image is not None:
                st.session_state["saved_canvas_images"].append(image)
                st.rerun()
            else:
                st.error(
                    "Failed to generate image from Diffusion Model. Please try again."
                )


    # Left and Right Column layout
    col1, col2 = st.columns([1, 4])

    # Search bar on the left (col1)
    with col1:
        st.session_state["search_query"] = st.text_input(
            "Search",
            placeholder="Type product name or description...",
            label_visibility="collapsed",
            on_change=increase_uploader_key,
        )

        st.button("Open Canvas", use_container_width=True, on_click=canvas_dialog)

        st.button(
            "Prompt Diffusion", use_container_width=True, on_click=diffusion_dialog
        )

        uploaded_file = st.file_uploader(
            "Upload image",
            label_visibility="collapsed",
            on_change = deactivate_search,
            key=st.session_state["uploader_key"],
        )
        print("UPLOADED FILE:", uploaded_file)
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
            st.button(
                "Clear Canvas",
                on_click=clear_canvas,
                icon=":material/delete:",
                use_container_width=True,
            )
        with cols[1]:
            st.button(
                "Search",
                on_click=search,
                icon=":material/search:",
                use_container_width=True
            )

    # Filter products based on search query and images
    search_term = st.session_state["search_query"] if len(st.session_state["search_query"]) > 0 else None
    search_img = st.session_state["saved_canvas_images"][-1] if st.session_state["saved_canvas_images"] else None

    filtered_products = get_products(search_term, search_img) if (st.session_state["search_activate"]) else st.session_state["search_image_results"]
    print("TEXT DE SEARCH:", search_term)
    print("ANH DE SEARCH:", search_img)
    print("TIM RA:", filtered_products)
    st.session_state["search_image_results"] = filtered_products

    # Display the filtered products in the right column (col2)
    with col2:
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
                            render_product_card(product)

                            button_placeholder = st.container()
                            with button_placeholder:
                                st.markdown(
                                    '<div class="small-centered-button">',
                                    unsafe_allow_html=True,
                                )
                                if st.button(
                                    label="View Details",
                                    key=f"view_details_{i}_{j}",
                                    on_click= view_details,
                                ):
                                    render_product_detail_card(product)
                                st.markdown("</div>", unsafe_allow_html=True)

                # After displaying a row of products, update columns for the next row
                cols = st.columns(NUM_COLUMNS)  # Create new set of columns

import streamlit as st

# Function to display product details in a pop-up
@st.dialog("Product Details", width="large")
def render_product_detail_card(product):
    def truncate_description(description, word_limit=50):
        words = description.split()
        if len(words) > word_limit:
            return " ".join(words[:word_limit]) + "..."
        return description

    # Product title
    if product.title:
        st.write(f"### {product.title}")

    # Main product image
    if product.thumbnailImage:
        st.markdown(
            f"""
            <div class="product-card-detail">
                <img src="{product.thumbnailImage}" class="product-image-detail" alt="{product.title or 'Product'}"/>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Display additional images in a horizontal row
    if product.galleryThumbnail:
        cols = st.columns(len(product.galleryThumbnail))
        for idx, image_url in enumerate(product.galleryThumbnail):
            with cols[idx]:
                st.image(image_url, use_container_width=True)

    # Product details
    details_html = '<div class="product-card-detail-2">'
    if product.price is not None:
        details_html += f'<p class="product-price"><span style="font-size: 20px;">Price: ${product.price:.2f}🪙</span></p>'
    if product.rating is not None:
        details_html += f'<p class="product-rating"><span style="font-size: 20px;">Rating: {product.rating}⭐</span></p>'
    if product.description is not None:
        details_html += f'<p class="product-description"><span style="font-size: 20px;">Description: {truncate_description(product.description)}</span></p>'
    # if product.url:
    #     details_html += f'<a href="{product.url}" target="_blank" class="product-link">View Product on Website</a>'
    details_html += '</div>'

    st.markdown(details_html, unsafe_allow_html=True)
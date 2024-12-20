import streamlit as st


def render_product_card(product):
    card_content = '<div class="product-card">'
    product.thumbnailImage = product.thumbnailImage.strip()
    # Conditionally add fields if they are not None
    if product.thumbnailImage:
        card_content += f'<img src="{product.thumbnailImage}" class="product-image" alt="{product.title or "Product"}"/>'
    if product.title:
        card_content += f'<p class="product-title">{product.title}</p>'
    if product.price is not None:
        card_content += f'<p class="product-price">Price: ${product.price}</p>'
    if product.rating is not None:
        card_content += f'<p class="product-rating">Rating: {product.rating} ⭐</p>'
    if product.url:
        card_content += f'<a href="{product.url}" class="product-link" target="_blank">Go to Amazon Page</a>'
    card_content += "</div>"

    # Render the content with Streamlit
    st.markdown(card_content, unsafe_allow_html=True)

from dataclasses import dataclass

@dataclass
class Product:
    title: str            # Product title (e.g., "Echo Dot (4th Gen)")
    url: str              # Product URL (e.g., "https://amazon.com/echo-dot")
    thumbnailImage: str   # URL or path to the product thumbnail image
    price: float          # Price of the product (e.g., 49.99)
    rating: float         # Rating of the product (e.g., 4.5 out of 5)
    galleryThumbnail: list[str]

# Create some example products
products = [
    Product(
        title="TOZO Hybrid Active Noise Cancelling Wireless Earbuds, 6 Mics Smart Noise Cancelling 55H Playtime, 32 Preset EQs via APP, Bluetooth 5.3 ENC AI Call, IPX8 Waterproof Headphones with SmartPow LED Display",
        url="https://www.amazon.com/dp/B0DGKWQMSM",
        thumbnailImage="https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
        price=36.99,
        rating=4.5,
        galleryThumbnail=["https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                        "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg"]
    ),
    Product(
        title="Wireless Earbuds, Bluetooth 5.3 Headphones in Ear with 4 ENC Noise Cancelling Mic, HiFi Stereo Deep Bass Wireless Earphones 40H Playtime, in-Ear Earbud Bluetooth Dual LED Display IP7 Waterproof, USB-C",
        url="https://www.amazon.com/dp/B0DD34PZDB",
        thumbnailImage="https://m.media-amazon.com/images/I/71bLnsMjdaL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
        price=29.99,
        rating=4.8,
        galleryThumbnail=["https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                        "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg"]
    ),
    Product(
        title="TOZO Hybrid Active Noise Cancelling Wireless Earbuds, 6 Mics Smart Noise Cancelling 55H Playtime, 32 Preset EQs via APP, Bluetooth 5.3 ENC AI Call, IPX8 Waterproof Headphones with SmartPow LED Display",
        url="https://www.amazon.com/dp/B0DGKWQMSM",
        thumbnailImage="https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
        price=36.99,
        rating=4.5,
        galleryThumbnail=["https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                        "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg"]
    ),
    Product(
        title="Wireless Earbuds, Bluetooth 5.3 Headphones in Ear with 4 ENC Noise Cancelling Mic, HiFi Stereo Deep Bass Wireless Earphones 40H Playtime, in-Ear Earbud Bluetooth Dual LED Display IP7 Waterproof, USB-C",
        url="https://www.amazon.com/dp/B0DD34PZDB",
        thumbnailImage="https://m.media-amazon.com/images/I/71bLnsMjdaL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
        price=29.99,
        rating=4.8,
        galleryThumbnail=["https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                        "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg"]
    ),
    Product(
        title="TOZO Hybrid Active Noise Cancelling Wireless Earbuds, 6 Mics Smart Noise Cancelling 55H Playtime, 32 Preset EQs via APP, Bluetooth 5.3 ENC AI Call, IPX8 Waterproof Headphones with SmartPow LED Display",
        url="https://www.amazon.com/dp/B0DGKWQMSM",
        thumbnailImage="https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
        price=36.99,
        rating=4.5,
        galleryThumbnail=["https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                        "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg"]
    ),
    Product(
        title="Wireless Earbuds, Bluetooth 5.3 Headphones in Ear with 4 ENC Noise Cancelling Mic, HiFi Stereo Deep Bass Wireless Earphones 40H Playtime, in-Ear Earbud Bluetooth Dual LED Display IP7 Waterproof, USB-C",
        url="https://www.amazon.com/dp/B0DD34PZDB",
        thumbnailImage="https://m.media-amazon.com/images/I/71bLnsMjdaL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
        price=29.99,
        rating=4.8,
        galleryThumbnail=["https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                        "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg"]
    ),
    Product(
        title="TOZO Hybrid Active Noise Cancelling Wireless Earbuds, 6 Mics Smart Noise Cancelling 55H Playtime, 32 Preset EQs via APP, Bluetooth 5.3 ENC AI Call, IPX8 Waterproof Headphones with SmartPow LED Display",
        url="https://www.amazon.com/dp/B0DGKWQMSM",
        thumbnailImage="https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
        price=36.99,
        rating=4.5,
        galleryThumbnail=["https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                        "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg"]
    ),
    Product(
        title="Wireless Earbuds, Bluetooth 5.3 Headphones in Ear with 4 ENC Noise Cancelling Mic, HiFi Stereo Deep Bass Wireless Earphones 40H Playtime, in-Ear Earbud Bluetooth Dual LED Display IP7 Waterproof, USB-C",
        url="https://www.amazon.com/dp/B0DD34PZDB",
        thumbnailImage="https://m.media-amazon.com/images/I/71bLnsMjdaL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
        price=29.99,
        rating=4.8,
        galleryThumbnail=["https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                        "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg"]
    ),
    Product(
        title="TOZO Hybrid Active Noise Cancelling Wireless Earbuds, 6 Mics Smart Noise Cancelling 55H Playtime, 32 Preset EQs via APP, Bluetooth 5.3 ENC AI Call, IPX8 Waterproof Headphones with SmartPow LED Display",
        url="https://www.amazon.com/dp/B0DGKWQMSM",
        thumbnailImage="https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
        price=36.99,                    
        rating=4.5,
        galleryThumbnail=["https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                        "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg"]
    ),
    Product(
        title="Wireless Earbuds, Bluetooth 5.3 Headphones in Ear with 4 ENC Noise Cancelling Mic, HiFi Stereo Deep Bass Wireless Earphones 40H Playtime, in-Ear Earbud Bluetooth Dual LED Display IP7 Waterproof, USB-C",
        url="https://www.amazon.com/dp/B0DD34PZDB",
        thumbnailImage="https://m.media-amazon.com/images/I/71bLnsMjdaL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
        price=29.99,
        rating=4.8,
        galleryThumbnail=["https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                        "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg"]
    ),
]

for i in range(10):
    products.append(
        Product(
        title="Wireless Earbuds, Bluetooth 5.3 Headphones in Ear with 4 ENC Noise Cancelling Mic, HiFi Stereo Deep Bass Wireless Earphones 40H Playtime, in-Ear Earbud Bluetooth Dual LED Display IP7 Waterproof, USB-C",
        url="https://www.amazon.com/dp/B0DD34PZDB",
        thumbnailImage="https://m.media-amazon.com/images/I/71bLnsMjdaL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
        price=29.99,
        rating=4.8,
        galleryThumbnail=["https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                        "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg",
                          "https://m.media-amazon.com/images/I/71oPmXN6NdL.__AC_SX300_SY300_QL70_FMwebp_.jpg"]
    )
    )
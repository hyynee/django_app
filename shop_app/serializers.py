from rest_framework import serializers
from .models import Product,Cart,CartItem



# chuyển đổi dữ liệu python qua JSON/XML (RESTFULL API)
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'image', 'description', 'category', 'price']

class ProductDetailSerializer(serializers.ModelSerializer):
    similar_products = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'image', 'description', 'category', 'price', 'similar_products']

    def get_similar_products(self, prod):
        similar_products = Product.objects.filter(category=prod.category).exclude(id=prod.id)[:4]
        serializers = ProductSerializer(similar_products, many=True)
        return serializers.data
    

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'cart_code', 'created_at', 'modified_at']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    cart = CartSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']
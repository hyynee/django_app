from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, ProductDetailSerializer, CartItemSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
@api_view(['GET'])
def products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def product_detail(request, id):
    product = Product.objects.get(id=id)
    serializers = ProductDetailSerializer(product)
    return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_product_to_cart(request):
    """
    Thêm sản phẩm mới vào giỏ hàng
    Nếu sản phẩm đã tồn tại thì tăng số lượng
    """
    try:
        cart_code = request.data.get('cart_code')
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        # Tạo hoặc lấy cart
        cart, created = Cart.objects.get_or_create(cart_code=cart_code)
        
        # Kiểm tra product có tồn tại không
        product = Product.objects.get(id=product_id)

        # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, 
            product=product,
            defaults={'quantity': quantity}  # Chỉ set quantity nếu tạo mới
        )

        if not created:
            # Nếu sản phẩm đã tồn tại, tăng số lượng
            cart_item.quantity += quantity
            cart_item.save()
            message = "Product quantity updated in cart"
        else:
            message = "Product added to cart successfully"

        # Trả về toàn bộ cart sau khi thêm/cập nhật
        cart_items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cart_items, many=True)
        
        return Response({
            "data": serializer.data,
            "message": message,
            "status": status.HTTP_200_OK
        })

    except Product.DoesNotExist:
        return Response({
            "message": "Product not found",
            "status": status.HTTP_404_NOT_FOUND
        })
    except Exception as e:
        return Response({
            "message": str(e),
            "status": status.HTTP_400_BAD_REQUEST
        })


    
@api_view(['GET'])
def view_cart(request):
    cart_code = request.GET.get('cart_code')  # Lấy cart_code từ query string
    if not cart_code:
        return Response({
            "message": "cart_code is required",
            "status": status.HTTP_400_BAD_REQUEST
        })
    try:
        cart = Cart.objects.get(cart_code=cart_code)
        cart_items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response({
            "data": serializer.data,
            "message": "Cart retrieved successfully.",
            "status": status.HTTP_200_OK
        })
    except Cart.DoesNotExist:
        return Response({
            "message": "Cart not found.",
            "status": status.HTTP_404_NOT_FOUND
        })
    except Exception as e:
        print(f"Error: {str(e)}") 
        return Response({
            "message": str(e),
            "status": status.HTTP_400_BAD_REQUEST
        })
    
@api_view(['PATCH'])
def update_cart_item_quantity(request):
    try:
        cart_code = request.data.get('cart_code')
        product_id = request.data.get('product_id')
        action = request.data.get('action')  # 'increment' hoặc 'decrement'
        quantity = request.data.get('quantity')  # hoặc set số lượng cụ thể
        # Lấy cart
        cart = Cart.objects.get(cart_code=cart_code)
        # Lấy cart item
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        old_quantity = cart_item.quantity
        if action:
            if action == 'increment':
                cart_item.quantity += 1
            elif action == 'decrement':
                cart_item.quantity -= 1
            else:
                return Response({
                    "message": "Invalid action. Use 'increment' or 'decrement'",
                    "status": status.HTTP_400_BAD_REQUEST
                })
        elif quantity is not None:
            if quantity < 0:
                return Response({
                    "message": "Quantity cannot be negative",
                    "status": status.HTTP_400_BAD_REQUEST
                })
            cart_item.quantity = quantity
        else:
            return Response({
                "message": "Either 'action' or 'quantity' is required",
                "status": status.HTTP_400_BAD_REQUEST
            })
        if cart_item.quantity <= 0:
            cart_item.delete()
            message = "Item removed from cart (quantity = 0)"
        else:
            cart_item.save()
            message = "Quantity updated successfully"
        # Trả về toàn bộ cart sau khi cập nhật
        cart_items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response({
            "data": serializer.data,
            "message": message,
            "status": status.HTTP_200_OK
        })

    except Cart.DoesNotExist:
        return Response({
            "message": "Cart not found",
            "status": status.HTTP_404_NOT_FOUND
        })
    except CartItem.DoesNotExist:
        return Response({
            "message": f"Product with ID {product_id} not found in cart",
            "status": status.HTTP_404_NOT_FOUND
        })
    except Exception as e:
        return Response({
            "message": str(e),
            "status": status.HTTP_400_BAD_REQUEST
        })

@api_view(['DELETE'])    
def delete_item(request):
    try:
        cart_item_id = request.data.get('item_id')
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()
        # Trả về toàn bộ cart sau khi xóa
        cart_items = CartItem.objects.filter(cart=cart_item.cart)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response({
            "data": serializer.data,
            "message": "Item deleted successfully.",
            "status": status.HTTP_200_OK
        })
    except CartItem.DoesNotExist:
        return Response({
            "message": "Cart item not found.",
            "status": status.HTTP_404_NOT_FOUND
        })
    except Exception as e:
        return Response({
            "message": str(e),
            "status": status.HTTP_400_BAD_REQUEST
        })
    

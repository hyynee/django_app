from django.db import models
from django.utils.text  import slugify
from django.conf import settings
# Create your models here.
class Product(models.Model):
    CATEGORY = (('Electronics', 'Electronics'),
                ('Groceries', 'Groceries'),
                ('Clothing', 'Clothing'),
                )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True)
    image = models.ImageField(upload_to='img')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY,blank=True, null=True)

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)
            unique_slug = self.slug
            counter = 1
            if(Product.objects.filter(slug=unique_slug).exists()):
                unique_slug= f"{self.slug}-{counter}"
                counter += 1
            self.slug = unique_slug

        super().save(*args, **kwargs)

# Mục đích của hàm:
# Tạo slug tự động từ tên sản phẩm:
# Nếu slug chưa được thiết lập (if not self.slug), hàm sẽ chuyển đổi tên sản phẩm (self.name) thành dạng slug bằng hàm slugify() (ví dụ: "iPhone 15 Pro" → "iphone-15-pro").
# Slug giúp URL dễ đọc, SEO-friendly và thường được dùng trong các đường dẫn chi tiết sản phẩm.
# Đảm bảo slug là duy nhất:
# Nếu slug đã tồn tại trong cơ sở dữ liệu (Product.objects.filter(slug=unique_slug).exists()), hàm sẽ thêm một số đếm vào cuối slug (ví dụ: iphone-15-pro-1, iphone-15-pro-2, ...) cho đến khi tạo được slug không trùng lặp.
# Lưu đối tượng:
# Sau khi xử lý slug, hàm gọi super().save(*args, **kwargs) để lưu đối tượng vào cơ sở dữ liệu như bình thường.


class Cart(models.Model):
    cart_code = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True,blank=True, null=True)

    def __str__(self):
        return self.cart_code
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity} in cart {self.cart.id}"
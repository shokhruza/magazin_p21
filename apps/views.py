from datetime import timedelta

from django.db.models import F
from django.db.models.functions import ExtractDay, Now
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.forms import CustomUserCreationForm
from apps.models import Product

from django.shortcuts import render
from django.core.paginator import Paginator


class ProductListView(ListView):
    # model = Product
    queryset = Product.objects.all()
    template_name = 'apps/product/product-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.annotate(timedelta=(ExtractDay(Now()) - ExtractDay(F('created_at'))))


class RegisterView(CreateView):
    template_name = 'apps/auth/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('log_out_page')

    def form_invalid(self, form):
        return super().form_invalid(form)

    # def form_valid(self, form):
    #     user = form.save()
    #     generate_link(self.request, user)
    #     text = '<h2>An email has been sent with instructions to verify your email</h2>'
    #     messages.add_message(self.request, messages.SUCCESS, text)
    #     return super().form_valid(form)

    def product_list(request):
        product_list = Product.objects.all()
        paginator = Paginator(product_list, 10)  # Har bir sahifada 10ta mahsulot

        page_number = request.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'apps/product/product-list.html', {'page_obj': page_obj})

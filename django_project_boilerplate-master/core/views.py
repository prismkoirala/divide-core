from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from .models import Item,Order,OrderItem,BillingAddresse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, View, FormView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from .forms import CheckoutForm, SizeForm


# Create your views here.
class HomeView(ListView):
    model = Item
    paginate_by = 4
    template_name = "home.html"

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object' : order,
            }
            return render(self.request, 'order_summary.html', context=context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have active Orders!")
            return redirect("/")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context =  {
            'form' : form
        }
        return render(self.request, "checkout.html", context=context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                state = form.cleaned_data.get('state')
                zip = form.cleaned_data.get('zip')
                #TODO: add functionality for these fields
                #same_shipping_address = form.cleaned_data.get('same_shipping_address')
                #save_info = form.cleaned_data.get('save_info')
                #payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddresse(
                    user = self.request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    state = state,
                    zip = zip,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                messages.success( self.request, "Success Checkout!" )
                return redirect('core:checkout_page')
            messages.warning(self.request, "Failed Checkout")
            return redirect('core:checkout_page')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have active Orders!")
            return redirect("core:order-summary")


class SizeView(UpdateView, SingleObjectMixin, LoginRequiredMixin):

    template_name = "item-size.html"
    form_class = SizeForm
    queryset = Item.objects.all()
    slug_field = 'slug'
    def get_object(self):
        slug_ = self.kwargs.get("slug")
        order_item, created = OrderItem.objects.filter(
            item__in = self.queryset,
            user = self.request.user,
            ordered = False
            )
        order_query = Order.objects.filter(user=self.request.user, ordered=False)
        if order_query.items.filter(slug=self.slug_field).exists():
            size = form.cleaned_data.get('size')
            print(size)
        return get_object_or_404(Item, slug=slug_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)



class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"



@login_required
def add_to_cart(request, slug):

    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
        )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'This Item quantity was updated to your Cart')

        else:
            messages.success(request, 'This Item was added to your Cart')
            order.items.add(order_item)
            return redirect("core:order-summary")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'This Item quantity was updated to your Cart')

    return redirect("core:order-summary")



#add to cart for productpage
@login_required
def add_to_cart_for_product(request, slug):

    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
        )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'This Item quantity was updated to your Cart')
        else:
            messages.success(request, 'This Item was added to your Cart')
            order.items.add(order_item)
            return redirect("core:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'This Item quantity was updated to your Cart')

    return redirect("core:product", slug=slug)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:order-summary")

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)
